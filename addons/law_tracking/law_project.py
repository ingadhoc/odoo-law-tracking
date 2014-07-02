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

class law_project(osv.osv):
    """Law Project"""
    
    _name = 'law_tracking.law_project'
    _description = 'Law Project'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _track = {
    }
    _columns = {
        'reference': fields.char(string='Reference', required=True),
        'name': fields.char(string='Name', required=True),
        'summary': fields.text(string='Summary', required=True),
        'entrance_chamber': fields.selection([(u'deputies', u'Deputies'), (u'senators', u'Senators')], string='Entrance Chamber', readonly=True),
        'entry_date': fields.date(string='Entry Date', required=True),
        'last_update': fields.date(string='Last Update'),
        'law_number': fields.char(string='Law Number'),
        'legislature_id': fields.many2one('law_tracking.legislature', string='Legislature', required=True, ondelete='cascade'), 
        'subscription_ids': fields.one2many('law_tracking.subscription', 'law_project_id', string='Subscriptions'), 
        'presenter_id': fields.many2one('law_tracking.legislature_member', string='Presenter', required=True), 
        'law_project_document_ids': fields.one2many('law_tracking.law_project_document', 'law_project_id', string='Documents'), 
        'dep_commission_treatment_ids': fields.one2many('law_tracking.commission_treatment', 'law_project_id', string='Deputies Commission Treatment', required=True, domain=[('partner_id.chamber','=','deputies')]), 
        'deputies_treatment_detail_ids': fields.one2many('law_tracking.enclosure_treatment_detail', 'law_project_id', string='Order Papers', domain=[('order_paper_id.chamber','=','deputies')]), 
        'log_ids': fields.one2many('law_tracking.log', 'law_project_id', string='log_ids'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




law_project()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
