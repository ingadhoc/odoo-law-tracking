# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class commission_treatment(osv.osv):
    """Deputies Commission Treatment"""
    
    _name = 'law_tracking.commission_treatment'
    _description = 'Deputies Commission Treatment'
    _inherits = {  }
    _inherit = [ 'mail.thread' ]

    _states_ = [
        # State machine: commission_treatment
        ('on_treatment','On Treatment'),
        ('approved','Approved'),
        ('disapproved','Disapproved'),
    ]
    _track = {
        'state': {
            'law_tracking.commission_treatment_on_treatment': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'on_treatment',
            'law_tracking.commission_treatment_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'approved',
            'law_tracking.commission_treatment_disapproved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'disapproved',
        },
    }


    _columns = {
        'state': fields.selection(_states_, "State"),
        'law_project_id': fields.many2one('law_tracking.law_project', string='Law Project', ondelete='cascade', required=True), 
        'partner_id': fields.many2one('res.partner', string='Commission', context={'default_is_commission':1}, domain=[('is_commission','=',True)], required=True), 
        'treatment_detail_ids': fields.one2many('law_tracking.treatment_detail', 'commission_treatment_id', string='Detail'), 
    }

    _defaults = {
        'state': 'on_treatment',
        'law_project_id': lambda self, cr, uid, context=None: context and context.get('law_project_id', False),
    }


    _constraints = [
    ]




commission_treatment()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
