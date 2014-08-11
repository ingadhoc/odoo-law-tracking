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

class block(osv.osv):
    """Block"""
    
    _inherit = 'law_tracking.block'
    _order = 'name'

    # def _get_members(self, cr, uid, ids, name, args, context=None):
    #     legislature_member_obj = self.pool.get('law_tracking.legislature_member')
    #     block_obj = self.pool.get('law_tracking.block')
    #     res = {}

    #     legislature_member_ids = legislature_member_obj.search(cr, uid, [('legislature_id','=',legislature.id),('state','=','active')], context=context)
    #     for block in self.browse(cr, SUPERUSER_ID, ids, context=context):
    #         # tmp = []
    #         # for legislature_member in legislature_member_obj.browse(cr, uid, legislature_member_ids, context=context):
    #         #     if legislature_member.partner_id.block_id.id not in tmp:
    #         #         tmp.append(legislature_member.partner_id.block_id.id)
    #         # res[legislature.id] =  tmp
    #     return res

    # _columns = {
    #     'block_members': fields.function(_get_members, type='integer', string='Block Members Qty', readonly=True, multi='_get_user_subscription'),
    #     'block_total': fields.function(_get_user_subscription, type='integer', string='Blocks Total', readonly=True, multi='_get_user_subscription'),        
    # }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
