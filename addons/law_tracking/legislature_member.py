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

class legislature_member(osv.osv):
    """"""
    
    _name = 'law_tracking.legislature_member'
    _description = 'legislature_member'

    _states_ = [
        # State machine: untitle
        ('active','Active'),
        ('finish','Finish'),
        ('cancelled','Cancelled'),
    ]
    _columns = {
        'entrance_date': fields.date(string='Entrance Date'),
        'exit_date': fields.date(string='Exit Date'),
        'chamber': fields.selection([(u'deputies', u'Deputies'), (u'senators', u'Senators')], string='Chamber', required=True),
        'state': fields.selection(_states_, "State"),
        'commission_detail_ids': fields.one2many('law_tracking.commission_detail', 'legislature_member_id', string='Commission Details'), 
        'legislature_id': fields.many2one('law_tracking.legislature', string='Legislature', ondelete='cascade', required=True), 
        'law_project_ids': fields.one2many('law_tracking.law_project', 'presenter_id', string='law_project_ids'), 
        'partner_id': fields.many2one('res.partner', string='Legislator', required=True, context={'default_is_legislator':True}, domain=[('is_legislator','=',True)]), 
    }

    _defaults = {
        'state': 'active',
    }


    _constraints = [
    ]


    def action_wfk_set_active(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'active'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'law_tracking.legislature_member', obj_id, cr)
            wf_service.trg_create(uid, 'law_tracking.legislature_member', obj_id, cr)
        return True



legislature_member()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
