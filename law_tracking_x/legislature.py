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
from openerp import SUPERUSER_ID, tools

class legislature(osv.osv):
    """Legislatures"""
    
    _inherit = 'law_tracking.legislature'
    _order = 'name'

    def _has_image(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = obj.image != False
        return result    

    # def _get_blocks(self, cr, uid, ids, name, args, context=None):
    #     legislature_member_obj = self.pool.get('law_tracking.legislature_member')
    #     block_obj = self.pool.get('law_tracking.block')
    #     res = {}
    #     for legislature in self.browse(cr, SUPERUSER_ID, ids, context=context):
    #         legislature_member_ids = legislature_member_obj.search(cr, uid, [('legislature_id','=',legislature.id),('state','=','active')], context=context)
    #         tmp = []
    #         for legislature_member in legislature_member_obj.browse(cr, uid, legislature_member_ids, context=context):
    #             if legislature_member.partner_id.block_id.id not in tmp:
    #                 tmp.append(legislature_member.partner_id.block_id.id)
    #         res[legislature.id] =  tmp
    #     return res

    _columns = {
        # 'block_ids': fields.function(_get_blocks, type='one2many', relation='law_tracking.block', string='Blocks', readonly=True,),
        'senators_commission_ids': fields.one2many('res.partner', 'legislature_id', string='Commissions', context={'default_is_commission':True,'default_chamber':'senators','from_other':True}, domain=[('is_commission','=',True),('chamber','=','senators')],), 
        # 'senator_ids': fields.one2many('res.partner', 'legislature_id', string='Senators', context={'default_is_legislator':True,'default_chamber':'senators'}, domain=[('is_legislator','=',True),('chamber','=','senators')],), 
        # 'deputy_ids': fields.one2many('res.partner', 'legislature_id', string='Deputies', context={'default_is_legislator':True,'default_chamber':'deputies'}, domain=[('is_legislator','=',True),('chamber','=','deputies')],), 
        'has_image': fields.function(_has_image, type="boolean"),
        'sen_legislature_member_ids': fields.one2many('law_tracking.legislature_member', 'legislature_id', string='Senators', context={'default_chamber':'senators'}, domain=[('state','=','active'),('chamber','=','senators')]), 
    }

    _defaults = {
    }
    
    def onchange_state(self, cr, uid, ids, state_id, context=None):
        if state_id:
            country_id = self.pool['res.country.state'].browse(cr, uid, state_id, context).country_id.id
            return {'value':{'country_id':country_id}}
        return {}




legislature()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
