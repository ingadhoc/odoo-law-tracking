# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class log(osv.osv):
    """"""
    
    _name = 'law_tracking.log'
    _description = 'log'



    _columns = {
        'date': fields.date(string='Date', required=True),
        'user_id': fields.many2one('res.users', string='User', required=True),
        'name': fields.char(string='Description', required=True),
        'law_project_id': fields.many2one('law_tracking.law_project', string='law_project_id', ondelete='cascade', required=True), 
    }

    _defaults = {
        'law_project_id': lambda self, cr, uid, context=None: context and context.get('law_project_id', False),
    }

    _order = "date desc"

    _constraints = [
    ]




log()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
