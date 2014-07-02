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
    
    _name = 'law_tracking.block'
    _description = 'Block'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'image': fields.binary(string='Image'),
        'partner_ids': fields.one2many('res.partner', 'block_id', string='Partners', context={'default_is_legislator': True}, domain=[('is_legislator', '=', True)]), 
    }

    _defaults = {
    }


    _constraints = [
    ]




block()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
