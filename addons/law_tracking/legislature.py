# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class legislature(osv.osv):
    """Legislatures"""
    
    _name = 'law_tracking.legislature'
    _description = 'Legislatures'



    _columns = {
        'name': fields.char(string='Name', required=True),
        'state_id': fields.many2one('res.country.state', string='State'),
        'type': fields.selection([(u'unicameral', u'Unicameral'), (u'bicameral', u'Bicameral')], string='Type', required=True),
        'image': fields.binary(string='Image'),
        'country_id': fields.many2one('res.country', string='Country', required=True),
        'law_project_ids': fields.one2many('law_tracking.law_project', 'legislature_id', string='Law Projects'), 
        'order_paper_ids': fields.one2many('law_tracking.order_paper', 'legislature_id', string='Order Paper'), 
        'deputies_commission_ids': fields.one2many('res.partner', 'legislature_id', string='Commissions', context={'default_is_commission':True,'default_chamber':'deputies','from_other':True}, domain=[('is_commission','=',True),('chamber','=','deputies')]), 
        'dep_legislature_member_ids': fields.one2many('law_tracking.legislature_member', 'legislature_id', string='Deputies', context={'default_chamber':'deputies'}, domain=[('state','=','active'),('chamber','=','deputies')]), 
    }

    _defaults = {
    }


    _constraints = [
    ]




legislature()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
