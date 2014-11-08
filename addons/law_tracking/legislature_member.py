# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class legislature_member(osv.osv):
    """"""
    
    _name = 'law_tracking.legislature_member'
    _description = 'legislature_member'

    _states_ = [
        # State machine: untitle
        ('active','Active'),
        ('finish','Finish'),
        ('cancelled','Cancelled'),
    ]


    _columns = {
        'entrance_date': fields.date(string='Entrance Date'),
        'exit_date': fields.date(string='Exit Date'),
        'chamber': fields.selection([(u'deputies', u'Deputies'), (u'senators', u'Senators')], string='Chamber', required=True),
        'state': fields.selection(_states_, "State"),
        'commission_detail_ids': fields.one2many('law_tracking.commission_detail', 'legislature_member_id', string='Commission Details'), 
        'legislature_id': fields.many2one('law_tracking.legislature', string='Legislature', ondelete='cascade', required=True), 
        'law_project_ids': fields.one2many('law_tracking.law_project', 'presenter_id', string='law_project_ids'), 
        'partner_id': fields.many2one('res.partner', string='Legislator', required=True, context={'default_is_legislator':True}, domain=[('is_legislator','=',True)]), 
    }

    _defaults = {
        'state': 'active',
        'legislature_id': lambda self, cr, uid, context=None: context and context.get('legislature_id', False),
    }


    _constraints = [
    ]


    def action_wfk_set_active(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'active'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'law_tracking.legislature_member', obj_id, cr)
            wf_service.trg_create(uid, 'law_tracking.legislature_member', obj_id, cr)
        return True



legislature_member()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
