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
    
    _inherit = 'law_tracking.law_project_document'

    _columns = {
        'attachment_ids': fields.many2many('ir.attachment', 'law_project_doc_attachment_rel','law_project_document_id', 'attachment_id', 'Attachemnts'),
    }

    _defaults = {
    }


    _constraints = [
    ]




law_project_document()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
