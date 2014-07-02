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

class legislature(osv.osv):
    """Legislatures"""
    
    _name = 'law_tracking.legislature'
    _description = 'Legislatures'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'state_id': fields.many2one('res.country.state', string='State'),
        'type': fields.selection([(u'unicameral', u'Unicameral'), (u'bicameral', u'Bicameral')], string='Type', required=True),
        'image': fields.binary(string='Image'),
        'country_id': fields.many2one('res.country', string='Country', required=True),
        'law_project_ids': fields.one2many('law_tracking.law_project', 'legislature_id', string='Law Projects'), 
        'order_paper_ids': fields.one2many('law_tracking.order_paper', 'legislature_id', string='Order Paper'), 
        'deputies_commission_ids': fields.one2many('res.partner', 'legislature_id', string='Commissions', context={'default_is_commission':True,'default_chamber':'deputies','from_other':True}, domain=[('is_commission','=',True),('chamber','=','deputies')]), 
        'dep_legislature_member_ids': fields.one2many('law_tracking.legislature_member', 'legislature_id', string='Deputies', context={'default_chamber':'deputies'}, domain=[('state','=','active'),('chamber','=','deputies')]), 
    }

    _defaults = {
    }


    _constraints = [
    ]




legislature()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
