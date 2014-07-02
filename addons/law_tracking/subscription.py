# -*- coding: utf-8 -*-
##############################################################################
#
#    Law Follow Up
#    Copyright (C) 2014 Sistemas ADHOC
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
from openerp import netsvc
from openerp.osv import osv, fields

class subscription(osv.osv):
    """Subscription"""
    
    _name = 'law_tracking.subscription'
    _description = 'Subscription'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _states_ = [
        # State machine: basic
        ('draft','Draft'),
        ('required','Required'),
        ('subscribed','Subscribed'),
        ('unsubscribed','Unsubscribed'),
        ('cancelled','Cancelled'),
    ]
    _track = {
        'state': {
            'law_tracking.subscription_draft': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'draft',
            'law_tracking.subscription_required': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'required',
            'law_tracking.subscription_subscribed': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'subscribed',
            'law_tracking.subscription_unsubscribed': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'unsubscribed',
            'law_tracking.subscription_cancelled': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'cancelled',
        },
    }
    _columns = {
        'price': fields.float(string='Price', required=True),
        'request_date': fields.date(string='Request Date', readonly=True),
        'state': fields.selection(_states_, "State"),
        'law_project_id': fields.many2one('law_tracking.law_project', string='Law Project', required=True, ondelete='cascade'), 
        'partner_id': fields.many2one('res.partner', string='Company', context={'default_is_company':True}, domain=[('is_company','=',True)], required=True), 
    }

    _defaults = {
        'state': 'draft',
    }

    _order = "id desc"

    _constraints = [
    ]


    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'law_tracking.subscription', obj_id, cr)
            wf_service.trg_create(uid, 'law_tracking.subscription', obj_id, cr)
        return True



subscription()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
