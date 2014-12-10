import re
from openerp import netsvc
from datetime import datetime, date, timedelta
import time
from openerp.osv import osv, fields
from dateutil import relativedelta
from openerp import SUPERUSER_ID, tools
from openerp.tools.translate import _
from urllib import urlencode
import pytz
from urlparse import urljoin
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

_PROJECT_STATE = [('draft', 'New'),('open', 'In Progress'),('pending', 'Pending'), ('done', 'Done'), ('cancelled', 'Cancelled')]
class law_tracking_stage(osv.osv):
    _name = 'law_tracking.stage'
    _description = 'Law Project Stage'
    _order = 'sequence'
    _columns = {
        'name': fields.char('Stage Name', required=True, size=64, translate=True),
        'description': fields.text('Description'),
        'sequence': fields.integer('Sequence'),
        'state': fields.selection(_PROJECT_STATE, 'Related Status', required=True,
                        help="The status of your document is automatically changed regarding the selected stage. " \
                            "For example, if a stage is related to the status 'Close', when your document reaches this stage, it is automatically closed."),        
        # Seems that we are no longer using this field
        # 'case_default': fields.boolean('Default for New Projects',
                        # help="If you check this field, this stage will be proposed by default on each new project. It will not assign this stage to existing projects."),
        'law_project_ids': fields.many2many('law_tracking.project.type', 'law_project_stage_type_relation', 'stage_id', 'type_id', 'Law Projects'),
        'fold': fields.boolean('Folded in Kanban View',
                               help='This stage is folded in the kanban view when'
                               'there are no records in that stage to display.'),
    }

    _defaults = {
        'sequence': 1,
        # 'law_project_ids': lambda self, cr, uid, ctx=None: self.pool['law_tracking.law_project']._get_default_project_id(cr, uid, context=ctx),
    }

class law_tracking_project_type(osv.osv):
    _name = 'law_tracking.project.type'
    _description = 'Law Project Type'
    _columns = {
        'name': fields.char('Name', required=True, size=64, translate=True),
        'stage_ids': fields.many2many('law_tracking.stage', 'law_project_stage_type_relation', 'type_id', 'stage_id', 'Tasks Stages',),
        'unicameral': fields.boolean('Unicameral?',),     
        # TODO use this for filtering presenter on chamber
        # 'entrance_chamber': fields.selection([(u'deputies', u'Deputies'), (u'senators', u'Senators')], string='Entrance Chamber', required=True),
    }


class law_project(osv.osv):
    """"""
    
    _inherit = 'law_tracking.law_project'
    _order = 'entry_date desc'

    def _get_default_project_id(self, cr, uid, context=None):
        """ Gives default section by checking if present in the context """
        return (self._resolve_project_id_from_context(cr, uid, context=context) or False)


    def _resolve_project_id_from_context(self, cr, uid, context=None):
        """ Returns ID of project based on the value of 'default_project_id'
            context key, or None if it cannot be resolved to a single
            project.
        """
        if context is None:
            context = {}
        if type(context.get('default_project_id')) in (int, long):
            return context['default_project_id']
        if isinstance(context.get('default_project_id'), basestring):
            project_name = context['default_project_id']
            project_ids = self.pool.get('law_tracking.law_project').name_search(cr, uid, name=project_name, context=context)
            if len(project_ids) == 1:
                return project_ids[0][0]
        return None        
  

    def get_subscriber(self, cr, uid, user_id, context=None):
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, user_id, context=context)           
        partner_ids = []
        if user.partner_id.is_company == True:
            partner_ids = [user.partner_id.id]
        elif user.partner_id.parent_id:
            partner_ids = [user.partner_id.parent_id.id]
        return partner_ids

    def _get_subscritors(self, cr, uid, ids, name, arg, context=None):
        subscription_obj = self.pool.get('law_tracking.subscription')

        partner_ids = self.get_subscriber(cr, SUPERUSER_ID, uid, context)

        subscription_ids = subscription_obj.search(cr, SUPERUSER_ID, [('law_project_id', 'in', ids), ('state','=','subscribed')])

        res = dict((id, dict(subscriptor_ids=[], user_is_subscriptor=False, has_subscriptors=False)) for id in ids)

        for subscription in subscription_obj.browse(cr, SUPERUSER_ID, subscription_ids):
            res[subscription.law_project_id.id]['subscriptor_ids'].append(subscription.partner_id.id)
            res[subscription.law_project_id.id]['has_subscriptors'] = (True)
            # If user is subscriptor or is employee we say True!
            if partner_ids and subscription.partner_id.id == partner_ids[0]:
                res[subscription.law_project_id.id]['user_is_subscriptor'] =  True
        return res

    def _user_is_employee(self, cr, uid, ids, name, arg, context=None):
        res = {}
        # We check if user is employee
        user_obj = self.pool.get('res.users')
        user_group_ids = user_obj.read(cr, SUPERUSER_ID, uid, fields=['groups_id'], context=context)      
        m  = self.pool.get('ir.model.data')
        employee_group_id = m.get_object(cr, SUPERUSER_ID, 'base', 'group_user').id       
        is_employee = False

        if employee_group_id in user_group_ids['groups_id']:
            is_employee = True

        for i in ids:
            res[i] = is_employee
        return res

    def _search_subscriptors(self, cr, uid, obj, name, args, context):

        sub_obj = self.pool.get('law_tracking.subscription')
        res = []
        for field, operator, value in args:
            assert field == name
            # TOFIX make it work with not in
            assert operator != "not in", "Do not search message_follower_ids with 'not in'"
            sub_ids = sub_obj.search(cr, SUPERUSER_ID, [('partner_id', operator, value), ('state','=','subscribed')])
            # sub_ids = sub_obj.search(cr, SUPERUSER_ID, [('res_model', '=', self._name), ('partner_id', operator, value)])
            res_ids = [sub.law_project_id.id for sub in sub_obj.browse(cr, SUPERUSER_ID, sub_ids)]
            res.append(('id', 'in', res_ids))
        return res  

    def _search_user_is_subscriptor(self, cr, uid, obj, name, args, context):

        res = []
        for field, operator, value in args:
            assert field == name
            partner_ids = self.get_subscriber(cr, SUPERUSER_ID, uid, context=context)
            
            if (operator == '=' and value) or (operator == '!=' and not value):  # is a follower
                law_project_ids = self.search(cr, SUPERUSER_ID, [('subscriptor_ids', 'in', partner_ids)], context=context)
            else:  # is not a follower or unknown domain
                aux_ids = self.search(cr, SUPERUSER_ID, [('subscriptor_ids', 'in', partner_ids)], context=context)
                law_project_ids = self.search(cr, SUPERUSER_ID, [('id', 'not in', aux_ids)], context=context)            
            res.append(('id', 'in', law_project_ids))
        return res      

    def _search_has_subscriptors(self, cr, uid, obj, name, args, context):
        res = []
        sub_obj = self.pool.get('law_tracking.subscription')
        for field, operator, value in args:
            assert field == name
            project_ids = []
            if (operator == '=' and value) or (operator == '!=' and not value):  # has subscriptors
                sub_ids = sub_obj.search(cr, SUPERUSER_ID, [('state','=','subscribed')])
                for sub in sub_obj.browse(cr, SUPERUSER_ID, sub_ids):
                    project_ids.append(sub.law_project_id.id)                
            else:  # is not a follower or unknown domain
                aux_ids = sub_obj.search(cr, SUPERUSER_ID, [('state','=','subscribed')], context=context)
                for sub in sub_obj.browse(cr, SUPERUSER_ID, aux_ids):
                    project_ids.append(sub.law_project_id.id)                
                project_ids = self.search(cr, SUPERUSER_ID, [('id', 'not in', project_ids)], context=context)  

            res.append(('id', 'in', project_ids))
        return res        

    # def _get_full_name(self, cr, uid, ids, prop, args, context=None):
    #     res = {}
    #     for line in self.browse(cr, uid, ids):
    #         res[line.id] = line.name + ' (' + line.reference + ') ' + ' - ' + line.legislature_id.name
    #     return res

    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = line.name + ' - ' + line.legislature_id.name        
            # res[line.id] = line.name + ' (' + line.reference + ') ' + ' - ' + line.legislature_id.name        
        # res = self._get_full_name(cr, uid, ids, 'full_name', None, context=context)
        return res.items()     

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []    
        ids = set()     
        if name:
            ids.update(self.search(cr, user, args + [('name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
            if not limit or len(ids) < limit:
                ids.update(self.search(cr, user, args + [('reference',operator,name)], limit=limit, context=context))
            if not limit or len(ids) < limit:
                ids.update(self.search(cr, user, [('legislature_id.name','ilike',name)]+ args, limit=limit, context=context))
            ids = list(ids)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result

    def _get_user_subscription(self, cr, uid, ids, name, args, context=None):
        subscription_obj = self.pool.get('law_tracking.subscription')
        partner_ids = self.get_subscriber(cr, SUPERUSER_ID, uid, context)
        subscription_ids = subscription_obj.search(cr, SUPERUSER_ID, [('law_project_id', 'in', ids), ('partner_id','in',partner_ids)])

        res = {}
        subscription_id = False
        subscription_state = False
        if subscription_ids:
            subscription_id = subscription_ids[0]
            subscription_state = subscription_obj.browse(cr, uid, subscription_ids[0], context).state

        res = dict((id, dict(user_subscription_id=subscription_id, user_subscription_state=subscription_state)) for id in ids)
        return res


    _columns = {
        'block_id': fields.related('presenter_id', 'partner_id', 'block_id', relation='law_tracking.block', type='many2one', string='Block', readonly=True),
        'block_representatives_perc': fields.related('presenter_id','block_representatives_perc', string='Block Rep. %%',),
        'block_representatives': fields.related('presenter_id','block_representatives', type='integer', string='Block Rep.', help='Block Representatives', readonly=True, ),
        'total_members': fields.related('presenter_id','total_members', type='integer', string='Blocks Total.', readonly=True, ),             
        # 'block_id': fields.related('presenter_id', 'partner_id', 'block_id', relation='law_tracking.block', type='many2one', string='Block', readonly=True),
        # 'full_name': fields.function(_get_full_name, type='char', string='Full Name', readonly=True), 
        'user_subscription_id': fields.function(_get_user_subscription, type='many2one', relation='law_tracking.subscription', string='Subscription', readonly=True, multi='_get_user_subscription'),
        'user_subscription_state': fields.function(_get_user_subscription, type='selection', selection=[
            # State machine: basic
            ('required','Required'),
            ('subscribed','Subscribed'),
            ('unsubscribed','Unsubscribed'),
            ('cancelled','Cancelled'),
            ],
            string='Subscription State', multi='_get_user_subscription'),
        'subscriptor_ids': fields.function(_get_subscritors, readonly=True, 
            fnct_search=_search_subscriptors, type='many2many',
            obj='res.partner', string='Subscriptors', multi='_get_subscritors'),
        'user_is_subscriptor': fields.function(_get_subscritors, type='boolean', string='User Is a Subscriptor', fnct_search=_search_user_is_subscriptor,  multi='_get_subscritors'),   
        'user_is_employee': fields.function(_user_is_employee, type='boolean', string='User Is a Employee', method=True, readonly=False),   
        'has_subscriptors': fields.function(_get_subscritors, type='boolean', string='Has Subscriptors', fnct_search=_search_has_subscriptors, multi='_get_subscritors'),   
        'open': fields.boolean('Active', track_visibility='onchange'),
        'law_category_ids': fields.many2many('law_tracking.category', 'project_law_category_rel', id1='law_project_id', id2='category_id', string='Categories', required=True,),
        'law_category_ids_copy': fields.related('law_category_ids', type="many2many", relation='law_tracking.category', string="Categories", readonly=True, ),
        'senators_treatment_detail_ids': fields.one2many('law_tracking.enclosure_treatment_detail', 'law_project_id', domain=[('order_paper_id.chamber','=','senators')], string='Order Papers'), 
        'enclosure_treatment_detail_ids': fields.one2many('law_tracking.enclosure_treatment_detail', 'law_project_id', string='Order Papers'), 
        'sen_commission_treatment_ids': fields.one2many('law_tracking.commission_treatment', 'law_project_id', string='Senators Commission Treatment', required=True, domain=[('partner_id.chamber','=','senators')]), 
        # 'filtered_message_ids': fields.one2many('mail.message', 'res_id',
        #     domain=lambda self: [('model', '=', self._name),('type','=','notification')],
        #     auto_join=True,
        #     string='Messages',
        #     help="Messages and communication history"),
        'sequence': fields.integer('Sequence'),
        'legislature_type': fields.related('legislature_id','type', type='char', ),
        'law_project_type_id': fields.many2one('law_tracking.project.type', 'Entrance Chamber', domain="[('unicameral','=',False)]", ondelete='set null', ),
        # Should change the domain when statusbar widget form trunk relase (folded shown differently)
        'copy_stage_id': fields.related('stage_id', type="many2one", relation='law_tracking.stage', string='Stage', readonly=True, domain="['&', ('fold', '=', False), ('law_project_ids', '=', law_project_type_id)]"),
        'stage_id': fields.many2one('law_tracking.stage', 'Stage',
                        domain="[('law_project_ids', '=', law_project_type_id)]", track_visibility="onchange"),
        'presented_by': fields.selection([
            ('legislator', 'Legislator'),
            ('executive', 'Executive'),
            ('judiciary', 'Judiciary'),
            ('popular_initiative', 'Popular Initiative'),
            ('other', 'Otro'),
            ], string='Presented By',
            required=True,),
    }

    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        default = {} if default is None else default.copy()
        law_project_rec = self.browse(cr, uid, id, context=context)
        # default.update(reference=_("%s (copy)") % (law_project_rec['reference'] or ''))
        default.update(reference=_("(copy)"))
        default.update(name=_("(copy)"))
        default.update(enclosure_treatment_detail_ids=[])
        default.update(log_ids=[])
        default.update(sen_commission_treatment_ids=[])
        default.update(dep_commission_treatment_ids=[])
        default.update(law_project_document_ids=[])
        default.update(subscription_ids=[])
        # default.update(reference=False)
        # default.update(name=False)
        return super(law_project, self).copy(cr, uid, id, default, context=context)

# Not implemented yet
# we supose that 'folded' is same as not active
    def check_parlamentary_status_lost(self, cr, uid, ids=None, context=None):
        if context is None:
            context = {}
        # date = time.strftime(DEFAULT_SERVER_DATE_FORMAT) 
        date = (datetime.now() - relativedelta.relativedelta(years=2)).strftime("%Y-%m-%d")
        # date = time.strftime(DEFAULT_SERVER_DATE_FORMAT) 
        # new_date = datetime.now() + timedelta(months=2)
         # + timedelta(days=365))
# datetime.strftime(datetime.now() + timedelta, tools.DEFAULT_SERVER_DATE_FORMAT)
        # wf_service = netsvc.LocalService("workflow")
        # ids = self.search(cr, uid, [('expiration_date','<=',date)])

        ids = self.search(cr, uid, [('stage_id.state','=', 'open'),('entry_date','<=',date)])
        # for record in self.browse(cr, uid, ids, context):
        stage_ids = self.pool.get('law_tracking.stage').search(cr, uid, [('state','=','pending')])
        if ids and stage_ids:
            # stage
            vals = {'stage_id': stage_ids[0]}
            self.write(cr, uid, ids, vals, context=context)
            # wf_service.trg_validate(uid, 'nautical.contract', record.id, 'sgn_expired', cr)                          
        #     print record.craft_id.id
        #     wf_service.trg_validate(uid, 'nautical.craft', record.craft_id.id, 'sgn_expired', cr)                          
        return True
        # return res

    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('law_tracking.stage')
        order = stage_obj._order
        access_rights_uid = access_rights_uid or uid
        if read_group_order == 'stage_id desc':
            order = '%s desc' % order
        search_domain = []
        project_id = self._resolve_project_id_from_context(cr, uid, context=context)
        if project_id:
            search_domain += ['|', ('law_project_ids', '=', project_id)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(cr, uid, search_domain, order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        fold = {}
        for stage in stage_obj.browse(cr, access_rights_uid, stage_ids, context=context):
            fold[stage.id] = stage.fold or False
        return result, fold

    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }        

# We make this default because on creation employee should see all the fields
    _defaults = {
        'user_is_employee':True,
        'presented_by': 'legislator',
        }

    _sql_constraints = [
        ('reference_uniq', 'unique(reference)', 'Reference must be unique'),
    ]

    def stage_find(self, cr, uid, cases, section_id, domain=[], order='sequence', context=None):
        """ Override of the base.stage method
            Parameter of the stage search taken from the lead:
            - section_id: if set, stages must belong to this section or
              be a default stage; if not set, stages must be default
              stages
        """
        if isinstance(cases, (int, long)):
            cases = self.browse(cr, uid, cases, context=context)
        # collect all section_ids
        section_ids = []
        if section_id:
            section_ids.append(section_id)
        for task in cases:
            if task.project_id:
                section_ids.append(task.project_id.id)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('law_project_ids', '=', section_id))
        search_domain += list(domain)
        
        stage_ids = self.pool.get('law_tracking.stage').search(cr, uid, search_domain, order=order, context=context)
        if stage_ids:
            return stage_ids[0]
        return False

    def onchange_presenter(self, cr, uid, ids, presenter_id, context=None):
        v = {}   
        if context is None:
            context = {}             
        if presenter_id:
            legislature_member_obj = self.pool.get('law_tracking.legislature_member')
            legislature_member = legislature_member_obj.browse(cr, uid, presenter_id, context=context)
            
            if not legislature_member:
                return {'value': v}
            
            if isinstance(legislature_member, list):
                legislature_member = legislature_member[0]
            v['block_id'] = legislature_member.block_id.id
            v['block_representatives_perc'] = legislature_member.block_representatives_perc
            v['total_members'] = legislature_member.total_members
            v['block_representatives'] = legislature_member.block_representatives
            # project_type_unicameral = self.pool.get('law_tracking.project.type').search(cr,uid,[('unicameral','=',True)])

        else:
            v['block_id'] = False
            v['block_representatives_perc'] = False
            v['total_members'] = False
            v['block_representatives'] = False
        return {'value': v}     

    def onchange_legislature(self, cr, uid, ids, legislature_id, context=None):
        v = {}   
        if context is None:
            context = {}             
        if legislature_id:
            legislature_obj = self.pool.get('law_tracking.legislature')
            legislature = legislature_obj.browse(cr, uid, legislature_id, context=context)
            
            if not legislature:
                return {'value': v}
            
            if isinstance(legislature, list):
                legislature = legislature[0]
            v['legislature_type'] = legislature.type
            project_type_unicameral = self.pool.get('law_tracking.project.type').search(cr,uid,[('unicameral','=',True)])
            if legislature.type == 'unicameral' and project_type_unicameral:
                v['law_project_type_id'] = project_type_unicameral[0]
            else:
                v['law_project_type_id'] = False

        else:
            v['legislature_type'] = False
            v['law_project_type_id'] = False
        return {'value': v}     

    def onchange_type(self, cr, uid, ids, law_project_type_id, context=None):
        v = {}   

        if context is None:
            context = {}             
        if law_project_type_id:
            law_project_type_obj = self.pool.get('law_tracking.project.type')
            law_project_type = law_project_type_obj.browse(cr, uid, law_project_type_id, context=context)
            if not law_project_type:
                return {'value': v}
            
            if isinstance(law_project_type, list):
                law_project_type = law_project_type[0]

            order='sequence'
            stage_ids = self.pool.get('law_tracking.stage').search(cr, uid, [('law_project_ids', '=', law_project_type.id)], order=order, context=context)
            v['stage_id'] = stage_ids[0] or False
        else:
            v['stage_id'] = False
        return {'value': v}      

    def check_suggestions(self, cr, uid, ids, context=None):
        if not context:
            context = {}        
        partner_obj = self.pool.get('res.partner')
        company_obj = self.pool.get('res.company').browse(cr, uid, 1, context)
        template = False
        try:
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'law_tracking_x', 'project_suggestion_mail')
        except ValueError:
            raise

        for law_project in self.browse(cr, uid, ids, context=context):       
            partner_match_ids = []
            partner_ids  = partner_obj.search(cr, uid, [('id','not in',[x.id for x in law_project.subscriptor_ids])])
            for partner in partner_obj.browse(cr, uid, partner_ids, context=context):
                partner_categ_ids = [x.id for x in partner.law_category_ids]
                for law_categ in law_project.law_category_ids:
                    if law_categ.id in partner_categ_ids:
                        partner_match_ids.append(partner.id)
                        break
            try:
                ctx_partner_ids = ', '.join(str(x) for x in partner_match_ids)
                context = dict(context, partner_ids=ctx_partner_ids)
                context = dict(context, company_obj=company_obj)
                self.pool.get('email.template').send_mail(cr, uid, template.id, law_project.id, force_send=True, raise_exception=True, context=context)
            except Exception:
                raise                
            break

        partner_names = ''
        for partner in partner_obj.browse(cr, uid, partner_match_ids, context=context):
            partner_names += partner.name + ', '
        return self.pool.get('warning_box').info(cr, uid, title=_('Suggestions Sent'), message=_('Suggestions has been sent to: ' + partner_names))   


    def require_more_information(self, cr, uid, ids, context=None):
        uid = 1 #porque este mail lo mandan usuarios portal y si no da error
        if not context:
            context = {}
        # partner_obj = self.pool.get('res.partner')
        # company_obj = self.pool.get('res.company').browse(cr, uid, 1, context)
        template = False
        try:
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'law_tracking_x', 'law_project_more_information_request')
        except ValueError:
            raise

        for law_project in self.browse(cr, uid, ids, context=context):       
            try:
                self.pool.get('email.template').send_mail(cr, uid, template.id, law_project.id, force_send=True, raise_exception=True, context=context)
            except Exception:
                raise                
        return self.pool.get('warning_box').info(cr, uid, title=_('Information Requested'), message=_('More information has been requested.'))   
    # def check_suggestions_old_modified(self, cr, uid, ids, context=None):
    #     if not context:
    #         context = {}        
    #     partner_obj = self.pool.get('res.partner')
    #     template = False
    #     signature_template = False
    #     # New for using partner to send email. TODO: improove this!! is horrible!
    #     partner_obj = self.pool.get('res.partner')
    #     try:
    #         template = self.pool.get('ir.model.data').get_object(cr, uid, 'law_tracking_x', 'project_suggestion_mail')
    #         signature_template = self.pool.get('ir.model.data').get_object(cr, uid, 'law_tracking_x', 'company_signature')
    #     except ValueError:
    #         raise
    #     user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
    #     signature_mail = self.pool.get('email.template').generate_email(cr, uid, signature_template.id, user.company_id.id, context=context)

    #     for law_project in self.browse(cr, uid, ids, context=context):       
    #         partner_match_ids = []
    #         partner_ids  = partner_obj.search(cr, uid, [('id','not in',[x.id for x in law_project.subscriptor_ids])])
    


    #         for partner in partner_obj.browse(cr, uid, partner_ids, context=context):
    #             partner_categ_ids = [x.id for x in partner.law_category_ids]
    #             for law_categ in law_project.law_category_ids:
    #                 if law_categ.id in partner_categ_ids:
    #                     data = {
    #                             'partner_id': partner.id,
    #                             'law_project_id': law_project.id,
    #                         }
    #                     partner_match_ids.append(partner.id)
    #                     # New for using partner to send email. TODO: improove this!! is horrible!                
    #                     try:
    #                         mail = self.pool.get('email.template').generate_email(cr, uid, template.id, law_project.id, context=context)
    #                         subtype = 'mail.mt_comment'
    #                         body_html = mail['body_html']
    #                         body_html = tools.append_content_to_html(mail['body_html'], signature_mail['body_html'], plaintext=False, container_tag='div')
    #                         # partner_obj.message_post(cr, uid, [partner.id], subject=mail['subject'],
    #                            # body=body_html, type='comment', subtype=subtype, context=context, partner_ids = [partner.id])
    #                         # context.update['recipient_ids'] = [partner.id]
    #                         self.pool.get('email.template').send_mail(cr, uid, template.id, law_project.id, force_send=True, raise_exception=True, context=context)
    #                     except Exception:
    #                         raise                
    #                     break
    #         # wE REPLACE THIW FOR THE "NEW"
    #         ## We write a notification and send this partner in context to notify them
    #         # context = dict(context, partner_match_ids=partner_match_ids)
    #         # res = self.write_comment(cr, uid, [law_project.id], 'law_tracking_x', 'project_suggestion_mail', context=context)
    #     # TODO el mensaje de a quien se le envio tendria que tener en cuenta si hay mas de un proyecto en el bucle del for
    #     partner_names = ''
    #     for partner in partner_obj.browse(cr, uid, partner_match_ids, context=context):
    #         partner_names += partner.name + ', '
    #     return self.pool.get('warning_box').info(cr, uid, title=_('Suggestions Sent'), message=_('Suggestions has been sent to: ' + partner_names))   

    def write_comment(self, cr, uid, ids, module, rec_id, context=None):
        """ write comment and send email """
        if not context:
            context = {}
        
        # With this option we disable the signature on the email of the user that is sending the email. It also changes the footer from:
        # Sent by Law Tracking using OpenERP. Access your messages and documents through our Customer Portal
        # to
        # Access your messages and documents through our Customer Portal
        context = dict(context, mail_notify_user_signature=False)
        # context = dict(context, lang='es_ES')
        
        template = False
        signature_template = False
        try:
            template = self.pool.get('ir.model.data').get_object(cr, uid, module, rec_id)
            signature_template = self.pool.get('ir.model.data').get_object(cr, uid, 'law_tracking_x', 'company_signature')
        except ValueError:
            raise
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if 'lang' not in context:
            if user.lang:
                context = dict(context, lang=user.lang)   
        signature_mail = self.pool.get('email.template').generate_email(cr, uid, signature_template.id, user.company_id.id, context=context)
        
        partner_match_ids = context.get('partner_match_ids', [])

        for law_project in self.browse(cr, uid, ids, context):
            try:
                mail = self.pool.get('email.template').generate_email(cr, uid, template.id, law_project.id, context=context)
                subtype = 'mail.mt_comment'
                body_html = mail['body_html']
                body_html = tools.append_content_to_html(mail['body_html'], signature_mail['body_html'], plaintext=False, container_tag='div')
                self.message_post(cr, uid, [law_project.id], subject=mail['subject'],
                   body=body_html, type='comment', subtype=subtype, context=context, partner_ids = partner_match_ids)
            except Exception:
                raise              

    def get_selection_item(self, cr, uid, ids, obj=None, model=None, field=None, context=None):
        if context == None:
            context = {}
        ret = ''
        if obj and field and model:
            field_val = getattr(obj, field)
            try:
                ret =  dict(self.pool.get(model).fields_get(cr, uid, allfields=[field], context=context)[field]['selection'])[field_val]
            except Exception:
                return ''
        return ret

    def get_treatment(self, cr, uid, ids, example_id=False, context=None):
        if not context:
            context = {}

        order_paper_ids = context.get('order_paper_ids', False)
        order_paper_obj = self.pool.get('law_tracking.order_paper')
        treatment_detail_obj = self.pool.get('law_tracking.treatment_detail')
        enclosure_treatment_detail_obj = self.pool.get('law_tracking.enclosure_treatment_detail')
        ret = False

        if not order_paper_ids and example_id:
            order_paper_ids = example_id
        if order_paper_ids:
            order_paper = order_paper_obj.browse(cr, uid, order_paper_ids, context=context)[0]
            if order_paper.type == 'commission':
                treatment_detail_ids = treatment_detail_obj.search(cr, uid, [('order_paper_id','in', order_paper_ids),('law_project_id','in',ids)], context=context)
                if treatment_detail_ids:
                    # There should be only one treatment for an order paper and a law_project
                    ret = treatment_detail_obj.browse(cr, uid, treatment_detail_ids, context=context)[0]
            elif order_paper.type == 'enclosure':
                eclosure_treatment_detail_ids = enclosure_treatment_detail_obj.search(cr, uid, [('order_paper_id','in', order_paper_ids),('law_project_id','in',ids)], context=context)
                if eclosure_treatment_detail_ids:
                    # There should be only one treatment for an order paper and a law_project
                    ret = enclosure_treatment_detail_obj.browse(cr, uid, eclosure_treatment_detail_ids, context=context)[0]
        return ret        

    def require_subscription(self, cr, uid, ids, context=None):
        if not context:
            context = {}        
        subscription_obj = self.pool.get('law_tracking.subscription')
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, uid, context=context)
        partner_ids = self.get_subscriber(cr, SUPERUSER_ID, uid, context)
        if not partner_ids:
            raise osv.except_osv(_('No partner type "is company" related for current user!'),_('User must belong to a partner tipe "Is Company"'))

        ret = []
        wf_service = netsvc.LocalService("workflow")
        for law_project in self.browse(cr, uid, ids, context=context):
            subscription_data = {
                'price': 0,
                'law_project_id': law_project.id,
                'partner_id': partner_ids[0],
            }
            if not law_project.user_subscription_id:
                # we create it with admin user so it can add subscriptors
                # subscription_id =  subscription_obj.create(cr, 1, subscription_data, context=context)
                subscription_id =  subscription_obj.create(cr, uid, subscription_data, context=context)
            else:
                subscription_id = law_project.user_subscription_id.id
            wf_service.trg_validate(uid, 'law_tracking.subscription', subscription_id, 'sgn_require', cr)
            ret.append(subscription_id)
        return ret

    def unsubscribe(self, cr, uid, ids, context=None):
        if not context:
            context = {}        
        subscription_obj = self.pool.get('law_tracking.subscription')
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, uid, context=context)

        partner_ids = []
        if user.partner_id.is_company == True:
            partner_ids.append(user.partner_id.id)
            for x in user.partner_id.child_ids:
                partner_ids.append(x.id)
        elif user.partner_id.parent_id:
            partner_ids.append(user.partner_id.parent_id.id)
            for x in user.partner_id.parent_id.child_ids:
                partner_ids.append(x.id)            

        wf_service = netsvc.LocalService("workflow")
        self.message_unsubscribe(cr, SUPERUSER_ID, ids, partner_ids, context=context)
        subscription_ids = self.pool.get('law_tracking.subscription').search(cr, uid, [('law_project_id','in',ids), ('partner_id', 'in', partner_ids), ('state','=','subscribed')])
        for subscription in subscription_ids:
            wf_service.trg_validate(SUPERUSER_ID, 'law_tracking.subscription', subscription, 'sgn_unsubscribe', cr)
        return True

    def format_date(self, cr, uid, ids, date, format, context):
        # date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        
        format_date = datetime.strftime(datetime.strptime(date, tools.DEFAULT_SERVER_DATE_FORMAT) , format)
        # format_date = datetime.strftime(datetime.strptime(date, tools.DEFAULT_SERVER_DATE_FORMAT) , format)
        return format_date           

    def write(self, cr, uid, ids, vals, context=None):
        if 'stage_id' in vals:
            self.write_log(cr, uid, ids, vals, context=context)         
        ret = super(law_project, self).write(cr, uid, ids, vals, context=context)
        if 'stage_id' in vals:
            self.write_comment(cr, uid, ids, 'law_tracking_x', 'project_status_change_mail', context=context)
        return ret       

    def write_log(self, cr, uid, ids, vals, context=None):
        for law_project in self.browse(cr, uid, ids, context=context):
            new_stage = vals['stage_id']
            date = context.get('log_date', fields.datetime.now())
            new_vals = {
                'user_id': uid,
                'date': date,
                'name': law_project.stage_id.name + '-->' + self.pool.get('law_tracking.stage').browse(cr, uid, new_stage, context=context).name or '',
                'law_project_id': law_project.id,
            }
            self.pool.get('law_tracking.log').create(cr, uid, new_vals, context=context)
        return True

    def get_actual_project_url(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        action = 'portal_law_tracking.action_portal_law_project_unsubscribed_law_projects'
        view_type='form'
        res_id = self.browse(cr, uid, ids[0], context=context).id
        ret = self.get_resource_url(cr, uid, ids, action=action, view_type=view_type, res_id=res_id)
        return ret
    
    def get_resource_url(self, cr, uid, ids, action='login', view_type=None, menu_id=None, res_id=None, model=None, context=None):
        """ generate a signup url for the given partner ids and action, possibly overriding
            the url state components (menu_id, id, view_type) """
        if context is None:
            context= {}
        res = dict.fromkeys(ids, False)
        
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        query = {'db': cr.dbname}
        fragment = {'action': action,}
        if view_type:
            fragment['view_type'] = view_type
        if menu_id:
            fragment['menu_id'] = menu_id
        if model:
            fragment['model'] = model
        if res_id:
            fragment['id'] = res_id

        res = urljoin(base_url, "?%s#%s" % (urlencode(query), urlencode(fragment)))

        return res    