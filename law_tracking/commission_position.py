# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class commission_position(osv.osv):
    """Commission Position"""
    
    _name = 'law_tracking.commission_position'
    _description = 'Commission Position'



    _columns = {
        'name': fields.char(string='Label', required=True),
        'commission_detail_ids': fields.one2many('law_tracking.commission_detail', 'commission_position_id', string='commission_detail_ids'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




commission_position()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
