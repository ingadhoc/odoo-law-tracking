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

class commission_treatment(osv.osv):
    """Deputies Commission Treatment"""
    
    _name = 'law_tracking.commission_treatment'
    _description = 'Deputies Commission Treatment'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _states_ = [
        # State machine: commission_treatment
        ('on_treatment','On Treatment'),
        ('approved','Approved'),
        ('disapproved','Disapproved'),
    ]
    _track = {
        'state': {
            'law_tracking.commission_treatment_on_treatment': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'on_treatment',
            'law_tracking.commission_treatment_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'approved',
            'law_tracking.commission_treatment_disapproved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'disapproved',
        },
    }
    _columns = {
        'state': fields.selection(_states_, "State"),
        'law_project_id': fields.many2one('law_tracking.law_project', string='Law Project', ondelete='cascade', required=True), 
        'partner_id': fields.many2one('res.partner', string='Commission', context={'default_is_commission':1}, domain=[('is_commission','=',True)], required=True), 
        'treatment_detail_ids': fields.one2many('law_tracking.treatment_detail', 'commission_treatment_id', string='Detail'), 
    }

    _defaults = {
        'state': 'on_treatment',
    }


    _constraints = [
    ]




commission_treatment()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
