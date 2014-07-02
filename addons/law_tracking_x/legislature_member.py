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

class legilsature_member(osv.osv):
    """"""
    
    # _rec_name = 'partner_id'
    _inherit = 'law_tracking.legislature_member'
    _description = 'legilsature_member'

    # def _get_name(self, cr, uid, ids, field_names, arg, context=None):
    #     if context is None:
    #         context = {}

    #     if isinstance(ids, (int, long)):
    #         ids = [ids]

    #     res = {}
    #     for data in self.browse(cr, uid, ids, context=context):
    #         res[data.id] = data.partner_id.name
    #     return res    

    def name_get(self, cr, uid, ids, context=None):
        # always return the full hierarchical name
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = line.partner_id.name      
        return res.items()     

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []    
        ids = set()     
        if name:
            ids.update(self.search(cr, user, args + [('partner_id.name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
            # if not limit or len(ids) < limit:
                # ids.update(self.search(cr, user, args + [('authorization_type_id.name',operator,name)], limit=limit, context=context))
            ids = list(ids)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result    

    def _get_members(self, cr, uid, ids, name, args, context=None):
        legislature_member_obj = self.pool.get('law_tracking.legislature_member')
        block_obj = self.pool.get('law_tracking.block')
        # res = {}

        res = dict((id, dict(total_memebers=0, block_representatives=0)) for id in ids)

        for member in self.browse(cr, SUPERUSER_ID, ids, context=context):
            total_members = legislature_member_obj.search(cr, uid, [('legislature_id','=',member.legislature_id.id),('chamber','=',member.chamber),('state','=','active')], context=context)
            legislature_member_ids = legislature_member_obj.search(cr, uid, [('partner_id.block_id.id','=',member.partner_id.block_id.id),('legislature_id','=',member.legislature_id.id),('chamber','=',member.chamber),('state','=','active')], context=context)
            
            # for legislature_member in legislature_member_obj.browse(cr, uid, legislature_member_ids, context=context):
            #     if legislature_member.partner_id.block_id.id not in tmp:
            #         tmp.append(legislature_member.partner_id.block_id.id)
            if not len(total_members) or len(total_members) == 0:
                res[member.id]['block_representatives_perc'] =  0
            else:
                res[member.id]['block_representatives_perc'] =  (len(legislature_member_ids) * 100.0) / len(total_members) 
            res[member.id]['block_representatives'] =  len(legislature_member_ids)
            res[member.id]['total_members'] =  len(total_members)
            # res[member.id] =  
        return res        

    _columns = {
        # 'name': fields.function(_get_name, type='char', string='Name'),
        'block_id': fields.related('partner_id', 'block_id', relation='law_tracking.block', type='many2one', string='Block'),
        'block_representatives_perc': fields.function(_get_members, string='Block Rep. %%', multi='_get_members'),
        # 'block_representatives_perc': fields.function(_get_members, string='Block Representatives', readonly=True, multi='_get_members'),
        'block_representatives': fields.function(_get_members, type='integer', string='Block Rep.', help='Block Representatives', readonly=True, multi='_get_members'),
        'total_members': fields.function(_get_members, type='integer', string='Blocks Total', readonly=True, multi='_get_members'),        
    }

legilsature_member()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
