# -*- coding: utf-8 -*-
##############################################################################
#
#    Law Follow Up
#    Copyright (C) 2013 Sistemas ADHOC
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import re
from datetime import datetime
from openerp import netsvc
from openerp.osv import osv, fields
from openerp import SUPERUSER_ID, tools
from urllib import urlencode
from urlparse import urljoin
import pytz
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class subscription(osv.osv):
    """Subscription"""
    
    _inherit = 'law_tracking.subscription'

    def _get_to_pay(self, cr, uid, ids, prop, unknow_none,unknow_dict):
        res = {}
        for line in self.browse(cr, uid, ids):
            if line.state == 'subscribed':
                res[line.id] = line.price
            else:
                res[line.id] = 0
        return res    

    def _get_name(self, cr, uid, ids, prop, unknow_none,context=None):
        res = {}
        lang = context.get('lang','en_US')
        lang_obj = self.pool.get('res.lang')
        lang_ids = lang_obj.search(cr, uid, [('code','=',lang)], context=context)
        lang_read = lang_obj.read(cr, uid, lang_ids, ['date_format'], context=context)
        if lang_read:
            date_format = lang_read[0]['date_format']        
        for line in self.browse(cr, uid, ids):
            request_date = ''
            if line.request_date:
                request_date = datetime.strptime(line.request_date,DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            res[line.id] = (request_date) + ' - ' + (line.partner_id.name or '')
        return res    

    _columns = {
        'to_pay': fields.function(_get_to_pay, type='float', string='To Pay',),
        'name': fields.function(_get_name, type='char', string='Name',),
    }

    # _sql_constraints = [
    #     ('subscription_unique',
    #      'unique (partner_id,state,law_project_id)',
    #      'There can not be two subscription of the same partner on the same law project on the same state.')
    # ]

    _sql_constraints = [
        ('subscription_unique',
         'unique (partner_id,law_project_id)',
         'There can not be two subscription of the same partner on the same law project.')
    ]

    # def _check_subscription(self, cr, uid, ids, context=None):        
    #     for record in self.browse(cr, uid, ids, context=context):
    #         print record.state
    #         if record.state == 'subscribed':
    #             print record.state
    #             partner = record.partner_id
    #             partner_subscriptions = self.search(cr, uid, [('partner_id','=',partner.id), ('state','=','subscribed')])
    #             print partner_subscriptions
    #             if len(partner_subscriptions)>1:
    #             # if partner_subscriptions:
    #                 return False
            
    #     return True

    # _constraints = [
    #     (_check_subscription,
    #         'There can not be two subscription of the same partner on the same law project on state "subscribed".',
    #         ['partner_id', 'state', 'law_project_id'])]            

    def format_date(self, cr, uid, ids, date, format, context):
        # date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        
        format_date = datetime.strftime(datetime.strptime(date, tools.DEFAULT_SERVER_DATE_FORMAT) , format)
        # format_date = datetime.strftime(datetime.strptime(date, tools.DEFAULT_SERVER_DATE_FORMAT) , format)
        return format_date   

    def action_unfollow(self, cr, uid, ids, context=None):
        partner_ids = []
        for record in self.browse(cr, uid, ids, context=context):
            if record.partner_id.is_company == True:
                partner_ids.append(record.partner_id.id)
                for x in record.partner_id.child_ids:
                    partner_ids.append(x.id)
            elif record.partner_id.parent_id:
                partner_ids.append(record.partner_id.parent_id.id)
                for x in record.partner_id.parent_id.child_ids:
                    partner_ids.append(x.id)     
            return self.pool.get('law_tracking.law_project').message_unsubscribe(cr, SUPERUSER_ID, [record.law_project_id.id], partner_ids, context=context)

    def action_follow(self, cr, uid, ids, context=None):
        partner_ids = []
        for record in self.browse(cr, uid, ids, context=context):
            if record.partner_id.is_company == True:
                partner_ids.append(record.partner_id.id)
                for x in record.partner_id.child_ids:
                    partner_ids.append(x.id)
            elif record.partner_id.parent_id:
                partner_ids.append(record.partner_id.parent_id.id)
                for x in record.partner_id.parent_id.child_ids:
                    partner_ids.append(x.id)     
            return self.pool.get('law_tracking.law_project').message_subscribe(cr, SUPERUSER_ID, [record.law_project_id.id], partner_ids, context=context)

    def action_complete_request_date(self, cr, uid, ids, context=None, *args):
        if context is None:
            context = {} 
        # project_ids = []
        vals = {
            'request_date': datetime.today(),
        }
        for record in self.browse(cr, uid, ids):
            self.write(cr, uid, [record.id], vals, context=context)
        return True 

    def action_notify_requisition(self, cr, uid, ids, context=None, *args):
        if context is None:
            context = {} 
        # project_ids = []
        for record in self.browse(cr, uid, ids):
            self.write_comment(cr, uid, [record.id], 'law_tracking_x', 'subscription_requisition_mail', context=context)
        return True   

    def get_actual_url(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        action = 'law_tracking.action_law_tracking_subscription_subscriptions'
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

    def action_notify_subscription(self, cr, uid, ids, context=None, *args):
        if context is None:
            context = {} 
        # project_ids = []
        for record in self.browse(cr, uid, ids):
            self.write_comment(cr, uid, [record.id], 'law_tracking_x', 'subscription_confirmation_mail', context=context)
        return True     

    def action_notify_unsubscription(self, cr, uid, ids, context=None, *args):
        if context is None:
            context = {} 
        # project_ids = []
        for record in self.browse(cr, uid, ids):
            self.write_comment(cr, uid, [record.id], 'law_tracking_x', 'subscription_unsubscription_mail', context=context)
        return True             

    def write_comment(self, cr, uid, ids, module, rec_id, context=None):
        """ write comment and send email """

        if not context:
            context = {}
        
        # With this option we disable the signature on the email of the user that is sending the email. It also changes the footer from:
        # Sent by Law Tracking using OpenERP. Access your messages and documents through our Customer Portal
        # to
        # Access your messages and documents through our Customer Portal
        context = dict(context, mail_notify_user_signature=False)
        
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

        for record in self.browse(cr, uid, ids, context):
            try:
                print 'contexttttttttttttttt', context 
                mail = self.pool.get('email.template').generate_email(cr, uid, template.id, record.id, context=context)
                subtype = 'mail.mt_comment'
                body_html = mail['body_html']
                body_html = tools.append_content_to_html(mail['body_html'], signature_mail['body_html'], plaintext=False, container_tag='div')
                self.message_post(cr, uid, [record.id], subject=mail['subject'],
                   body=body_html, type='comment', subtype=subtype, context=context, partner_ids = partner_match_ids)
            except Exception:
                raise           