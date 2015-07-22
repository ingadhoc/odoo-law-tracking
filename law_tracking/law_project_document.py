# -*- coding: utf-8 -*-

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
        'law_project_id': lambda self, cr, uid, context=None: context and context.get('law_project_id', False),
    }


    _constraints = [
    ]




law_project_document()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
