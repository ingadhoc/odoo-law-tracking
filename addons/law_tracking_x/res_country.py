# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class CountryState(osv.osv):
    _inherit = 'res.country.state'
    _order = 'name'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

