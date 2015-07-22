# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class treatment_detail(osv.osv):
    """"""
    
    _name = 'law_tracking.treatment_detail'
    _description = 'treatment_detail'



    _columns = {
        'note': fields.text(string='Note'),
        'order_paper_id': fields.many2one('law_tracking.order_paper', string='Order Paper', required=True), 
        'commission_treatment_id': fields.many2one('law_tracking.commission_treatment', string='Commission treatment', ondelete='cascade', required=True), 
    }

    _defaults = {
        'commission_treatment_id': lambda self, cr, uid, context=None: context and context.get('commission_treatment_id', False),
    }


    _constraints = [
    ]




treatment_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
