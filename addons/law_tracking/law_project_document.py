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

class law_project_document(osv.osv):
    """"""
    
    _name = 'law_tracking.law_project_document'
    _description = 'law_project_document'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'law_project_id': fields.many2one('law_tracking.law_project', string='law_project_id', ondelete='cascade', required=True), 
        'attachment_ids': fields.many2many('ir.attachment', 'law_tracking_attachment_ids_law_project_document_ids_rel', 'law_project_document_id', 'attachment_id', string='Attachments'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




law_project_document()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
