import re
from openerp import netsvc
from openerp.osv import osv, fields
# Esto era para antes que ibamos a ocultar los estados de eeuu
# class res_country_state(osv.osv):
#     _inherit = 'res.country.state'
#     _columns = {
#         'active': fields.boolean('Active',),
#     }

#     _defaults = {
#         'active': 1,
#     }

class res_partner_category(osv.osv):
    _inherit = 'res.partner.category'
    _name = 'law_tracking.category'
    _order = 'name'
    _columns = {
        'child_ids': fields.one2many('law_tracking.category', 'parent_id', 'Child Categories'),
        'parent_id': fields.many2one('law_tracking.category', 'Parent Category', select=True, ondelete='cascade'),
    }

class res_partner(osv.osv):
    _inherit = "res.partner"

    # def _search_contract_renewal_due_soon(self, cr, uid, obj, name, args, context):
    #     res = []
    #     for field, operator, value in args:
    #         assert operator in ('=', '!=', '<>') and value in (True, False), 'Operation not supported'
    #         if (operator == '=' and value == True) or (operator in ('<>', '!=') and value == False):
    #             search_operator = 'in'
    #         else:
    #             search_operator = 'not in'
    #         # today = fields.date.context_today(self, cr, uid, context=context)
    #         # datetime_today = datetime.datetime.strptime(today, tools.DEFAULT_SERVER_DATE_FORMAT)
    #         # limit_date = str((datetime_today + relativedelta(days=+15)).strftime(tools.DEFAULT_SERVER_DATE_FORMAT))
    #         # cr.execute('select cost.vehicle_id, count(contract.id) as contract_number FROM fleet_vehicle_cost cost left join fleet_vehicle_log_contract contract on contract.cost_id = cost.id WHERE contract.expiration_date is not null AND contract.expiration_date > %s AND contract.expiration_date < %s AND contract.state IN (\'open\', \'toclose\') GROUP BY cost.vehicle_id', (today, limit_date))
    #         # res_ids = [x[0] for x in cr.fetchall()]
    #         res.append(('id', search_operator, res_ids))
    #     return res


    def _get_inactive(self, cr, uid, ids, name, arg, context=None):
        res = {}
        # res = dict((id, False) for id in ids)
        # partner_id = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
        # notif_obj = self.pool.get('mail.notification')
        # notif_ids = notif_obj.search(cr, uid, [
        #     ('partner_id', 'in', [partner_id]),
        #     ('message_id', 'in', ids),
        #     ('starred', '=', True),
        # ], context=context)
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = True
        return res

    def _inactive_search(self, cr, uid, obj, name, domain, context=None):
        """ Search for starred messages by the current user."""
        # domain = [('state','=','active')]
        domain = [('legislature_member_ids.state','=','active')]
        partner_ids = self.search(
            cr, uid, domain, context=context)
        # member_ids = self.pool['law_tracking.legislature_member'].search(
            # cr, uid, domain, context=context)
        # # ('notification_ids.is_read', '=', not domain[0][2])
        # print 'domain', domain
        return [('id', 'not in', partner_ids)]
        # return [('legislature_member_ids.state', '=', 'active')]
        # return ['&', ('notification_ids.partner_id.user_ids', 'in', [uid]), ('notification_ids.starred', '=', domain[0][2])]

    _columns = {
        'law_category_ids': fields.many2many('law_tracking.category', 'partner_law_category_rel', id1='partner_id', id2='category_id', string='Categories'),
        'legislature_type': fields.related('legislature_id','type', type='char', string='Legislature Type',),
        'commision_detail_ids': fields.one2many('law_tracking.commission_detail', 'partner_id', string='Commissions', readonly=True, ),
        'inactive': fields.function(
            _get_inactive, type='boolean', string='Inactive', fnct_search=_inactive_search,
            help="Inactive Legislators are the ones that doesn't have any legislature function 'active'"),
        # In case we want only to show commissions where he is active
        # 'commision_detail_ids': fields.one2many('law_tracking.commission_detail', 'partner_id', string='Commissions', domain=[('legislature_member_id.state','=','active')], readonly=True, ),
        # Hicimos que ahora cada partner
        # 'parent_law_category_ids': fields.related('parent_id', 'law_category_ids', type='many2many', relation='law_tracking.category', string='Categories'),
    }

    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        default = {} if default is None else default.copy()
        partner_rec = self.browse(cr, uid, id, context=context)
        default.update(commission_detail_ids=[])
        default.update(order_paper_ids=[])
        default.update(dep_commission_treatment_ids=[])
        default.update(legislature_member_ids=[])
        default.update(law_project_document_ids=[])
        default.update(subscription_ids=[])
        default.update(image=False)
        return super(res_partner, self).copy(cr, uid, id, default, context=context)

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
            if legislature.type == 'unicameral':
                v['chamber'] = 'deputies'
        else:
            v['legislature_type'] = False
            v['chamber'] = False
        return {'value': v}     



class res_country(osv.osv):
    _inherit = "res.country"

    _columns = {
        'contratable': fields.boolean(string='Contratable'),
    }