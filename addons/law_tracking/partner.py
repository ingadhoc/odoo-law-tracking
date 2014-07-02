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

class partner(osv.osv):
    """"""
    
    _name = 'res.partner'
    _inherits = {  }
    _inherit = [ 'res.partner' ]

    _columns = {
        'chamber': fields.selection([(u'deputies', u'Deputies'), (u'senators', u'Senators')], string='Chamber'),
        'is_commission': fields.boolean(string='Is Commission?'),
        'chief': fields.many2one('res.partner', string='Chief'),
        'administrative_secretary': fields.many2one('res.partner', string='Administrative Secretary'),
        'meetings': fields.char(string='Meetings'),
        'is_legislator': fields.boolean(string='Is Legislator?'),
        'start_command': fields.date(string='Start Command'),
        'end_command': fields.date(string='End Command'),
        'order': fields.integer(string='Order'),
        'block_id': fields.many2one('law_tracking.block', string='Block'), 
        'commission_detail_ids': fields.one2many('law_tracking.commission_detail', 'commission_id', string='Commission Details', domain=[('legislature_member_id.state','=','active')], ondelete='cascade'), 
        'order_paper_ids': fields.one2many('law_tracking.order_paper', 'commission_id', string='Order Paper'), 
        'legislature_id': fields.many2one('law_tracking.legislature', string='Legislature'), 
        'contracted_country_ids': fields.many2many('res.country', 'law_tracking___contracted_country_ids_rel', 'partner_id', 'country_id', string='Contracted Countries', context={'default_contratable':True}, domain=[('contratable','=',True)]), 
        'dep_commission_treatment_ids': fields.one2many('law_tracking.commission_treatment', 'partner_id', string='Deputies Commission Treatment'), 
        'legislature_member_ids': fields.one2many('law_tracking.legislature_member', 'partner_id', string='legislature_member_ids'), 
        'subscription_ids': fields.one2many('law_tracking.subscription', 'partner_id', string='Subscriptions'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
