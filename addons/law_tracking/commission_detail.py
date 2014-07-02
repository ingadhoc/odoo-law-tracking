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

class commission_detail(osv.osv):
    """Commission Detail"""
    
    _name = 'law_tracking.commission_detail'
    _description = 'Commission Detail'

    _columns = {
        'commission_id': fields.many2one('res.partner', string='Commissions', context={'default_is_commission':True}, domain=[('is_commission','=',True)], required=True), 
        'commission_position_id': fields.many2one('law_tracking.commission_position', string='Position', required=True), 
        'legislature_member_id': fields.many2one('law_tracking.legislature_member', string='Legislature Member', ondelete='cascade', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




commission_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
