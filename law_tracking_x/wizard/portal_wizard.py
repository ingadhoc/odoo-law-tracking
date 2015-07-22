# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
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

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import email_re
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class wizard_user(osv.osv_memory):

    _name = 'portal.wizard.user'
    _inherit = 'portal.wizard.user'

    def _send_email(self, cr, uid, wizard_user, context=None):
        """ send notification email to a new portal user
            @param wizard_user: browse record of model portal.wizard.user
            @return: the id of the created mail.mail record
        """
        res_partner = self.pool.get('res.partner')
        # user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context).partner_id.id
        # aunque no necesito this user porque no tengo firmar
        # this_user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context)

        if not context:
            context = {}

        template = False
        try:
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'law_tracking_x', 'set_password_email')
        except ValueError:
            pass
        mail_obj = self.pool.get('mail.mail')
        assert template._name == 'email.template'

        user = self._retrieve_user(cr, SUPERUSER_ID, wizard_user, context)
        context = dict(context or {}, lang=user.lang)
        ctx_portal_url = dict(context, signup_force_type_in_url='')
        portal_url = res_partner._get_signup_url_for_action(cr, uid,
                                                            [user.partner_id.id],
                                                            context=ctx_portal_url)[user.partner_id.id]
        res_partner.signup_prepare(cr, uid, [user.partner_id.id], context=context)    
        context = dict(context, base_url=self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url', 'False'))    

        mail_id = self.pool.get('email.template').send_mail(cr, SUPERUSER_ID, template.id, user.id, True, context=context)
        mail_state = mail_obj.read(cr, uid, mail_id, ['state'], context=context)
        if mail_state and mail_state['state'] == 'exception':
            raise osv.except_osv(_("Cannot send email: no outgoing email server configured.\nYou can configure it under Settings/General Settings."), user.name)
        else:
            return True




        # # determine subject and body in the portal user's language
        # user = self._retrieve_user(cr, SUPERUSER_ID, wizard_user, context)
        # context = dict(this_context or {}, lang=user.lang)
        # ctx_portal_url = dict(context, signup_force_type_in_url='')
        # portal_url = res_partner._get_signup_url_for_action(cr, uid,
        #                                                     [user.partner_id.id],
        #                                                     context=ctx_portal_url)[user.partner_id.id]
        # res_partner.signup_prepare(cr, uid, [user.partner_id.id], context=context)

        # data = {
        #     'company': this_user.company_id.name,
        #     'portal': wizard_user.wizard_id.portal_id.name,
        #     'welcome_message': wizard_user.wizard_id.welcome_message or "",
        #     'db': cr.dbname,
        #     'name': user.name,
        #     'login': user.login,
        #     'signup_url': user.signup_url,
        #     'portal_url': portal_url,
        # }
        # mail_mail = self.pool.get('mail.mail')
        # mail_values = {
        #     'email_from': this_user.email,
        #     'email_to': user.email,
        #     'subject': _(WELCOME_EMAIL_SUBJECT) % data,
        #     'body_html': '<pre>%s</pre>' % (_(WELCOME_EMAIL_BODY) % data),
        #     'state': 'outgoing',
        #     'type': 'email',
        # }
        # mail_id = mail_mail.create(cr, uid, mail_values, context=this_context)
        # return mail_mail.send(cr, uid, [mail_id], context=this_context)            