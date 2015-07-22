# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class block(osv.osv):
    """Block"""
    
    _name = 'law_tracking.block'
    _description = 'Block'



    _columns = {
        'name': fields.char(string='Name', required=True),
        'image': fields.binary(string='Image'),
        'partner_ids': fields.one2many('res.partner', 'block_id', string='Partners', context={'default_is_legislator': True}, domain=[('is_legislator', '=', True)]), 
    }

    _defaults = {
    }


    _constraints = [
    ]




block()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
