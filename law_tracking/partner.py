# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class partner(osv.osv):
    """"""
    
    _name = 'res.partner'
    _inherits = {  }
    _inherit = [ 'res.partner' ]



    _columns = {
        'chamber': fields.selection([(u'deputies', u'Deputies'), (u'senators', u'Senators')], string='Chamber'),
        'is_commission': fields.boolean(string='Is Commission?'),
        'chief': fields.many2one('res.partner', string='Chief'),
        'administrative_secretary': fields.many2one('res.partner', string='Administrative Secretary'),
        'meetings': fields.char(string='Meetings'),
        'is_legislator': fields.boolean(string='Is Legislator?'),
        'start_command': fields.date(string='Start Command'),
        'end_command': fields.date(string='End Command'),
        'order': fields.integer(string='Order'),
        'block_id': fields.many2one('law_tracking.block', string='Block'), 
        'commission_detail_ids': fields.one2many('law_tracking.commission_detail', 'commission_id', string='Commission Details', domain=[('legislature_member_id.state','=','active')], ondelete='cascade'), 
        'order_paper_ids': fields.one2many('law_tracking.order_paper', 'commission_id', string='Order Paper'), 
        'legislature_id': fields.many2one('law_tracking.legislature', string='Legislature'), 
        'dep_commission_treatment_ids': fields.one2many('law_tracking.commission_treatment', 'partner_id', string='Deputies Commission Treatment'), 
        'legislature_member_ids': fields.one2many('law_tracking.legislature_member', 'partner_id', string='legislature_member_ids'), 
        'subscription_ids': fields.one2many('law_tracking.subscription', 'partner_id', string='Subscriptions'), 
    }

    _defaults = {
        'commission_detail_ids': lambda self, cr, uid, context=None: context and context.get('commission_detail_ids', False),
    }


    _constraints = [
    ]




partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
