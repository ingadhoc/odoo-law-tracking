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

class treatment_detail(osv.osv):
    """"""
    
    _inherit = 'law_tracking.treatment_detail'
    _rec_name = 'note'


    _columns = {
        'law_project_id': fields.related('commission_treatment_id', 'law_project_id', type="many2one", relation='law_tracking.law_project', string="Law Project", readonly=True, ),
    }

    _defaults = {
    }

    _constraints = [
    ]

    _sql_constraints = [
        ('unique', 'unique(commission_treatment_id, order_paper_id)', 'Record must be unique for an order paper on a commission'),
    ]