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

class commission_position(osv.osv):
    """Commission Position"""
    
    _name = 'law_tracking.commission_position'
    _description = 'Commission Position'

    _columns = {
        'name': fields.char(string='Label', required=True),
        'commission_detail_ids': fields.one2many('law_tracking.commission_detail', 'commission_position_id', string='commission_detail_ids'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




commission_position()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
