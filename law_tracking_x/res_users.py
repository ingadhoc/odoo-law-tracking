from openerp.osv import fields, osv
import logging
_logger = logging.getLogger(__name__)

class res_users(osv.osv):
    """"""
    
    _inherit = 'res.users'


    def _contracted_countries(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=None):
            if line.partner_id.parent_id:
                res[line.id] = line.partner_id.parent_id.contracted_country_ids
            else:
                res[line.id] = line.partner_id.contracted_country_ids
        return res

    _columns = {
        'partner_contracted_country_ids': fields.function(_contracted_countries, string='Partner Contracted Countries'), 
        }

    _defaults = {
    }

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on notification_email_send
            and alias fields. Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(res_users, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.extend(['law_category_ids','law_category_ids'])
        return init_res    