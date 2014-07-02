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

class order_paper(osv.osv):
    """Order Paper"""
    
    _name = 'law_tracking.order_paper'
    _description = 'Order Paper'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _states_ = [
        # State machine: untitle
        ('draft','Draft'),
        ('notified','Notified'),
        ('treated','Treated'),
        ('cancelled','Cancelled'),
    ]
    _track = {
        'state': {
            'law_tracking.order_paper_draft': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'draft',
            'law_tracking.order_paper_notified': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'notified',
            'law_tracking.order_paper_treated': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'treated',
            'law_tracking.order_paper_cancelled': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'cancelled',
        },
    }
    _columns = {
        'date': fields.date(string='Date', readonly=True, required=True, states={'draft': [('readonly', False)]}),
        'chamber': fields.selection([(u'deputies', u'Deputies'), (u'senators', u'Senators')], string='Chamber', readonly=True, required=True, states={'draft': [('readonly', False)]}),
        'type': fields.selection([(u'commission', u'Commission'), (u'enclosure', u'Enclosure')], string='Type', readonly=True, required=True, states={'draft': [('readonly', False)]}),
        'state': fields.selection(_states_, "State"),
        'commission_id': fields.many2one('res.partner', string='Commission', readonly=True, states={'draft': [('readonly', False)]}), 
        'legislature_id': fields.many2one('law_tracking.legislature', string='Legislature', readonly=True, states={'draft': [('readonly', False)]}, ondelete='cascade', required=True), 
        'treatment_detail_ids': fields.one2many('law_tracking.treatment_detail', 'order_paper_id', string='Project Treatments'), 
        'enclosure_treatment_detail_ids': fields.one2many('law_tracking.enclosure_treatment_detail', 'order_paper_id', string='Enclosure Treatment Detail', readonly=True, states={'draft': [('readonly', False)],'notified': [('readonly', False)]}), 
    }

    _defaults = {
        'state': 'draft',
    }


    _constraints = [
    ]


    def onchange_type(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def onchange_chamber(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def onchange_commission(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'law_tracking.order_paper', obj_id, cr)
            wf_service.trg_create(uid, 'law_tracking.order_paper', obj_id, cr)
        return True



order_paper()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
