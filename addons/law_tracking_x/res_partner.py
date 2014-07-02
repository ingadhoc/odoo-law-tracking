import re
from openerp import netsvc
from openerp.osv import osv, fields
# Esto era para antes que ibamos a ocultar los estados de eeuu
# class res_country_state(osv.osv):
#     _inherit = 'res.country.state'
#     _columns = {
#         'active': fields.boolean('Active',),
#     }

#     _defaults = {
#         'active': 1,
#     }

class res_partner_category(osv.osv):
    _inherit = 'res.partner.category'
    _name = 'law_tracking.category'
    _order = 'name'
    _columns = {
        'child_ids': fields.one2many('law_tracking.category', 'parent_id', 'Child Categories'),
        'parent_id': fields.many2one('law_tracking.category', 'Parent Category', select=True, ondelete='cascade'),
    }

class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {
        'law_category_ids': fields.many2many('law_tracking.category', 'partner_law_category_rel', id1='partner_id', id2='category_id', string='Categories'),
        'legislature_type': fields.related('legislature_id','type', type='char', string='Legislature Type',),
        'commision_detail_ids': fields.one2many('law_tracking.commission_detail', 'partner_id', string='Commissions', readonly=True, ),
        # In case we want only to show commissions where he is active
        # 'commision_detail_ids': fields.one2many('law_tracking.commission_detail', 'partner_id', string='Commissions', domain=[('legislature_member_id.state','=','active')], readonly=True, ),
        # Hicimos que ahora cada partner
        # 'parent_law_category_ids': fields.related('parent_id', 'law_category_ids', type='many2many', relation='law_tracking.category', string='Categories'),
    }
    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        default = {} if default is None else default.copy()
        partner_rec = self.browse(cr, uid, id, context=context)
        default.update(commission_detail_ids=[])
        default.update(order_paper_ids=[])
        default.update(dep_commission_treatment_ids=[])
        default.update(legislature_member_ids=[])
        default.update(law_project_document_ids=[])
        default.update(subscription_ids=[])
        default.update(image=False)
        return super(res_partner, self).copy(cr, uid, id, default, context=context)

    def onchange_legislature(self, cr, uid, ids, legislature_id, context=None):
        v = {}   
        if context is None:
            context = {}          
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
            v['chamber'] = False
        return {'value': v}     


class res_country(osv.osv):
    _inherit = "res.country"

    _columns = {
        'contratable': fields.boolean(string='Contratable'),
    }