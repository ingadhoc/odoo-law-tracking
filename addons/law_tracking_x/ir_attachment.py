# -*- coding: utf-8 -*-
from openerp.osv import osv


class document_file(osv.osv):
    _inherit = 'ir.attachment'

    # def check(self, cr, uid, ids, mode, context=None, values=None):
    #     """Overwrite check to verify access on directory to validate specifications of doc/access_permissions.rst"""
    #     print '111111111111111111'
    #     print '111111111111111111'
    #     if not isinstance(ids, list):
    #         ids = [ids]

    #     super(document_file, self).check(cr, uid, ids, mode, context=context, values=values)

    #     if ids:
    #         self.pool.get('ir.model.access').check(cr, uid, 'document.directory', mode)

    #         # use SQL to avoid recursive loop on read
    #         cr.execute('SELECT DISTINCT parent_id from ir_attachment WHERE id in %s AND parent_id is not NULL', (tuple(ids),))
    #         self.pool.get('document.directory').check_access_rule(cr, uid, [parent_id for (parent_id,) in cr.fetchall()], mode, context=context)


    # Modificamos esta funcion de ir attachemtn porque da error cuando los usuarios
    # portal quieren acceder a los adjuntos, modificamos la parte del final
    def check(self, cr, uid, ids, mode, context=None, values=None):
        """Restricts the access to an ir.attachment, according to referred model
        In the 'document' module, it is overriden to relax this hard rule, since
        more complex ones apply there.
        """
        res_ids = {}
        require_employee = False
        if ids:
            if isinstance(ids, (int, long)):
                ids = [ids]
            cr.execute('SELECT DISTINCT res_model, res_id FROM ir_attachment WHERE id = ANY (%s)', (ids,))
            for rmod, rid in cr.fetchall():
                if not (rmod and rid):
                    require_employee = True
                    continue
                res_ids.setdefault(rmod,set()).add(rid)
        if values:
            if values.get('res_model') and values.get('res_id'):
                res_ids.setdefault(values['res_model'],set()).add(values['res_id'])

        ima = self.pool.get('ir.model.access')
        for model, mids in res_ids.items():
            # ignore attachments that are not attached to a resource anymore when checking access rights
            # (resource was deleted but attachment was not)
            if not self.pool.get(model):
                require_employee = True
                continue
            existing_ids = self.pool[model].exists(cr, uid, mids)
            if len(existing_ids) != len(mids):
                require_employee = True
            ima.check(cr, uid, model, mode)
            self.pool[model].check_access_rule(cr, uid, existing_ids, mode, context=context)
        # Comentamos esta parte que es la que daria error
        # if require_employee:
            # if not uid == SUPERUSER_ID and not self.pool['res.users'].has_group(cr, uid, 'base.group_user'):
                # raise except_orm(_('Access Denied'), _("Sorry, you are not allowed to access this document."))
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
