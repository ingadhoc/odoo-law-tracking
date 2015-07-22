# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class enclosure_treatment_detail(osv.osv):
    """"""
    
    _name = 'law_tracking.enclosure_treatment_detail'
    _description = 'enclosure_treatment_detail'



    _columns = {
        'note': fields.text(string='Note'),
        'order_paper_id': fields.many2one('law_tracking.order_paper', string='Order Paper', required=True), 
        'law_project_id': fields.many2one('law_tracking.law_project', string='Law Projects', ondelete='cascade', required=True), 
    }

    _defaults = {
        'law_project_id': lambda self, cr, uid, context=None: context and context.get('law_project_id', False),
    }


    _constraints = [
    ]




enclosure_treatment_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
