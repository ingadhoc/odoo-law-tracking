# -*- coding: utf-8 -*-
##############################################################################
#
#    Law Follow Up
#    Copyright (C) 2013 Sistemas ADHOC
#    No email
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


import re
from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime, timedelta
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class order_paper(osv.osv):
    """"""
    
    _inherit = 'law_tracking.order_paper'
    _description = 'order_paper'

    def _get_name(self, cr, uid, ids, field_names, arg, context=None):
        if context is None:
            context = {}

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            chamber = ''
            if data.chamber == 'deputies':
                chamber = _('Deputies')
            else:
                chamber = _('Senators')
            lang = context.get('lang', 'en_US')
            print 'lang', lang 
            lang_reads = self.pool.get('res.lang').search_read(cr, uid, [('code','=',lang)],['date_format'])
            if lang_reads:
                context_lang_format = lang_reads[0].get('date_format','%m/%d/%Y')
            date = datetime.strptime(data.date,DEFAULT_SERVER_DATE_FORMAT).strftime(context_lang_format)
            res[data.id] = date + ' / ' + data.legislature_id.name + ' - ' + chamber
        return res    

    def _get_law_projects(self, cr, uid, ids, field_names, arg, context=None):
        if context is None:
            context = {}

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            project_ids = []
            if record.type == 'commission':
                for treatment in record.treatment_detail_ids:
                    project_ids.append(treatment.commission_treatment_id.law_project_id.reference)
            elif record.type == 'enclosure':              
                for treatment in record.enclosure_treatment_detail_ids:
                    project_ids.append(treatment.law_project_id.reference)
            res[record.id] = ', '.join(str(x) for x in project_ids) 
            # res[record.id] = project_ids
        return res

    _columns = {
        # 'in': fields.function(_get_in, type='char', string='In'),
        'name': fields.function(_get_name, type='char', string='Name'),
        'legislature_type': fields.related('legislature_id','type', type='char', string='Legislature Type',),
        # 'law_project_ids': fields.function(_get_law_project_ids, type='one2many', relation='', string='Law Projects', readonly=True),
        'law_projects': fields.function(_get_law_projects, type='char', string='Law Projects', readonly=True),
    }

    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        default = {} if default is None else default.copy()
        default.update(treatment_detail_ids=[])
        default.update(enclosure_treatment_detail_ids=[])
        return super(order_paper, self).copy(cr, uid, id, default, context=context)    

    def onchange_legislature(self, cr, uid, ids, legislature_id, context=None):
        v = {}   
        if context is None:
            context = {}          
        v['commission_id'] = False
        v['treatment_detail_ids'] =  [(5, 0)]
        v['enclosure_treatment_detail_ids'] =  [(5, 0)]
        v['chamber'] = False
        if legislature_id:
            legislature_obj = self.pool.get('law_tracking.legislature')
            legislature = legislature_obj.browse(cr, uid, legislature_id, context=context)
            
            if not legislature:
                return {'value': v}
            
            if isinstance(legislature, list):
                legislature = legislature[0]
            v['legislature_type'] = legislature.type
            if legislature.type == 'unicameral':
                v['chamber'] = 'deputies'
        else:
            v['legislature_type'] = False
        return {'value': v} 

    def onchange_type(self, cr, uid, ids, treatment_detail_ids, enclosure_treatment_detail_ids, context=None):
        v = {}   
        if context is None:
            context = {}          

        new_lst_treatment = []
        lst = treatment_detail_ids
        for sub_lst in lst:
            if len(sub_lst) > 0 and isinstance(sub_lst[0], int):
                if sub_lst[0] in [1,2,3,4]:
                    new_lst_treatment.append([2, sub_lst[1]]) 

        lst = enclosure_treatment_detail_ids
        for sub_lst in lst:
            if len(sub_lst) > 0 and isinstance(sub_lst[0], int):
                if sub_lst[0] in [1,2,3,4]:
                    new_lst_eclosure_treatment.append([2, sub_lst[1]]) 

        v['commission_id'] = False
        v['treatment_detail_ids'] =  new_lst_treatment
        v['enclosure_treatment_detail_ids'] =  new_lst_eclosure_treatment
        return {'value': v}     

    def onchange_chamber(self, cr, uid, ids, treatment_detail_ids, enclosure_treatment_detail_ids, context=None):
        v = {}   
        if context is None:
            context = {}          

        new_lst_treatment = []
        lst = treatment_detail_ids
        for sub_lst in lst:
            if len(sub_lst) > 0 and isinstance(sub_lst[0], int):
                if sub_lst[0] in [1,2,3,4]:
                    new_lst_treatment.append([2, sub_lst[1]]) 

        new_lst_eclosure_treatment = []
        lst = enclosure_treatment_detail_ids
        for sub_lst in lst:
            if len(sub_lst) > 0 and isinstance(sub_lst[0], int):
                if sub_lst[0] in [1,2,3,4]:
                    new_lst_eclosure_treatment.append([2, sub_lst[1]]) 

        v['commission_id'] = False
        v['treatment_detail_ids'] =  new_lst_treatment
        v['enclosure_treatment_detail_ids'] =  new_lst_eclosure_treatment
        return {'value': v}

    def onchange_commission(self, cr, uid, ids, treatment_detail_ids, context=None):
        v = {}   
        if context is None:
            context = {}   
        new_lst = []
        lst = treatment_detail_ids
        for sub_lst in lst:
            if len(sub_lst) > 0 and isinstance(sub_lst[0], int):
                if sub_lst[0] in [1,2,3,4]:
                    new_lst.append([2, sub_lst[1]])   
        v['treatment_detail_ids'] =  new_lst
        
        return {'value': v}                  

    def action_notify(self, cr, uid, ids, context=None, *args):
        context = dict(context or {})
        context['order_paper_ids'] = ids       
        project_ids = []
        for order_paper in self.browse(cr, uid, ids):
            for treatment in order_paper.treatment_detail_ids:
                project_ids.append (treatment.commission_treatment_id.law_project_id.id)
            for treatment in order_paper.enclosure_treatment_detail_ids:
                project_ids.append (treatment.law_project_id.id)
        self.pool.get('law_tracking.law_project').write_comment(cr, uid, project_ids, 'law_tracking_x', 'project_order_paper_notification_mail', context=context)
        return True      
  
    def action_treated(self, cr, uid, ids, context=None, *args):
        context = dict(context or {})
        context['order_paper_ids'] = ids
        project_ids = []
        for order_paper in self.browse(cr, uid, ids):
            for treatment in order_paper.treatment_detail_ids:
                project_ids.append (treatment.commission_treatment_id.law_project_id.id)
            for treatment in order_paper.enclosure_treatment_detail_ids:
                project_ids.append (treatment.law_project_id.id)
        self.pool.get('law_tracking.law_project').write_comment(cr, uid, project_ids, 'law_tracking_x', 'project_order_paper_treated_mail', context=context)
        return True      
  


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
