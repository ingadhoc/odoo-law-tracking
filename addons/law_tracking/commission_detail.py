# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class commission_detail(osv.osv):
    """Commission Detail"""
    
    _name = 'law_tracking.commission_detail'
    _description = 'Commission Detail'



    _columns = {
        'commission_id': fields.many2one('res.partner', string='Commissions', context={'default_is_commission':True}, domain=[('is_commission','=',True)], required=True), 
        'commission_position_id': fields.many2one('law_tracking.commission_position', string='Position', required=True), 
        'legislature_member_id': fields.many2one('law_tracking.legislature_member', string='Legislature Member', ondelete='cascade', required=True), 
    }

    _defaults = {
        'legislature_member_id': lambda self, cr, uid, context=None: context and context.get('legislature_member_id', False),
    }


    _constraints = [
    ]




commission_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
