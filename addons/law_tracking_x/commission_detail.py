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
from openerp.osv import osv, fields


class commission_detail(osv.osv):

    """Commission Detail"""

    _inherit = 'law_tracking.commission_detail'
    _rec_name = 'commission_id'

    _states_ = [
        # State machine: untitle
        ('active', 'Active'),
        ('finish', 'Finish'),
        ('cancelled', 'Cancelled'),
    ]

    _columns = {
        'partner_id': fields.related('legislature_member_id', 'partner_id', type="many2one", relation="res.partner", string="Partner", readonly=True, store=True),
        'legislature_id': fields.related('legislature_member_id', 'legislature_id', type="many2one", relation="law_tracking.legislature", string="Legislature", readonly=True, ),
        'state': fields.related('legislature_member_id', 'state', type="selection", selection=_states_, string="State", readonly=True, ),
    }

    _defaults = {
    }

    _constraints = [
    ]


commission_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
