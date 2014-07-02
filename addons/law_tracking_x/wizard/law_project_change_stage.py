# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 OpenERP S.A (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import email_re
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

class law_project_change_stage(osv.osv_memory):

    _name = 'law_tracking.law_project.change_stage'
    _description = 'Law Project Change Stage'

    _columns = {
        'new_stage_id': fields.many2one('law_tracking.stage', string='Stage', required=True, ),
        'date': fields.date(string='Date', required=True, ),
        'law_project_type_id': fields.many2one('law_tracking.project.type', 'Entrance Chamber', ),
    }

    _defaults = {
        'date': fields.date.context_today,
    }

    def change_state(self, cr, uid, ids, context=None):
        """
        """    
        if context is None: context = {}
        active_ids = context.get('active_ids', False)
        if not ids or not active_ids:
            return False
        wizard_id = ids[0]
        wizard = self.browse(cr, uid, wizard_id, context=context)
        context['log_date'] = wizard.date
        vals = {
            'stage_id': wizard.new_stage_id.id,
            # 'date' = wizard.date,
        }
        self.pool['law_tracking.law_project'].write(cr, uid, active_ids, vals, context=context)

        return {'type': 'ir.actions.act_window_close'}
    