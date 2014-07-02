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
from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _

class commission_treatment(osv.osv):
    """Commission Treatment"""
    
    _inherit = 'law_tracking.commission_treatment'

    def _get_name(self, cr, uid, ids, field_names, arg, context=None):
        if context is None:
            context = {}

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            chamber = ''
            if data.partner_id.chamber == 'deputies':
                chamber = _('Deputies')
            else:
                chamber = _('Senators')
            if data.law_project_id:
                res[data.id] = data.law_project_id.name  + ' - ' + chamber + ' - ' + data.partner_id.name
            # elif data.sen_law_project_id:
                # res[data.id] = data.sen_law_project_id.name  + ' - ' + data.partner_id.chamber + ' - ' + data.partner_id.name                
            else:
                res[data.id] = ''            
        return res 

    def _get_has_treatments(self, cr, uid, ids, field_names, arg, context=None):
        if context is None:
            context = {}

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            res[data.id] = False
            if data.treatment_detail_ids:
                res[data.id] = True
        return res              

    _columns = {
        'name': fields.function(_get_name, type='char', string='Name'),
        'has_treatments': fields.function(_get_has_treatments, type='boolean', string='Has Treatments?'),
    }            

    _sql_constraints = [
        ('unique', 'unique(law_project_id, partner_id)', 'Commission must be unique'),
    ]

    def _check_commission(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            for treatment_detail in data.treatment_detail_ids:
                if treatment_detail.order_paper_id.commission_id != data.partner_id:
                    return False
        return True    

    _constraints = [
        (_check_commission, 'Error: All commission treatments should be from the same commission', ['En Comisiones']),
        ]
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
