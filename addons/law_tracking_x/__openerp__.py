# -*- coding: utf-8 -*-
##############################################################################
#
#    Saas Manager
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


{   'active': False,
    'author': u'Sistemas ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo': [
          'data/demo/law_categories/law_tracking.category.csv',
          'data/demo/law_categories/res.partner.csv',
          'data/demo/law_tracking.block.csv',
          'data/demo/deputies/res.partner.csv',
          'data/demo/commissions/res.partner.csv',
          'data/demo/commissions/law_tracking.legislature_member.csv',
          'data/demo/commissions/law_tracking.commission_detail.csv',
          'data/demo/res.partner.csv',
          'data/demo/res.users.csv',
          'data/demo/res.company.csv',
          'data/demo/images/res.partner.csv',
          'data/demo/images/res_company.xml',
      ],
    'depends': [u'law_tracking',
      # da error, por lo menos en res_partner_view, busando ΅legislature_member_id' 
      # 'web_m2x_options',
      'help_doc',
      'l10n_ar_states',
      'base_action_rule',
      'cron_run_manually',
      'base_import',
      'user_partner_is_employee',
      'warning_box',
      # 'web_nocreatedb',
      'disable_openerp_online', 
      'portal', 
      # 'web_law_cust', 
      'law_tracking_custom_translations'],
    'description': """
Law Tracking Project
==================== 
Installs all modules of Law Tracking Project

Post installation instrucions
-----------------------------
* Instalar modulo web_nocreatedb 
* Instal es_AR language
* Set default language to es_AR
* Corregir formato fecha en idioma es_AR a d/m/y
* Habilitar "Habilitar restablecimiento de la contraseña desde la página de inicio de sesión"
* Configurar company data
* Configurar cuenta de correo de salida (que no sea localhost si no da error con sendmail)
* Configurar mail catch all (infoleyes@adhocsistemas.com.ar - info2014leyes)
* Configurar usuarios follower por defecto para recibir solicitudes de subscripcion (en acciones automatizadas)
* Borrar provincias de eeuu
* activar país argentino

Projects required:
* lp:~sistemas-adhoc/openerp-l10n-ar-localization/7.0
* lp:server-env-tools/7.0 --> disable_openerp_online
* lp:web-addons/7.0 --> web_nocreatedb,
* lp:adhoc-oerp/7.0 --> modules of documentation
* este lo tenemos en nuestro repo pero originalmente esta en lp:~openerp-community/openobject-addons/whatsapp7.0 --> warning_box
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Law Tracking Project',
    'test': [],
    'data': [   
          'data/mail_data.xml',
          'data/law_tracking.legislature.csv',
          'data/law_tracking.commission_position.csv',
          'data/law_tracking_data.xml',
          'data/res_users.xml',
          'data/law_tracking.stage.csv',
          'data/law_tracking.project.type.csv',
          'data/cron.xml',
          'wizard/law_project_change_stage_view.xml',
          'view/commission_treatment_view.xml',
          'view/views_customizations.xml',
          'view/order_paper_view.xml',
          'view/law_tracking_category.xml',
          'view/res_partner_view.xml',
          'view/law_project_view.xml',
          'view/legislature_view.xml',
          'view/res_users_view.xml',
          'view/enclosure_treatment_detail_view.xml',
          'view/legislature_member_view.xml',
          'view/treatment_detail_view.xml',
          'view/commission_detail_view.xml',
          'view/res_country_view.xml',
          'view/subscription_view.xml',
          'wizard/portal_wizard_view.xml',
          # 'workflow/law_project_workflow.xml',
          'workflow/order_paper_workflow.xml',
          'workflow/subscription_workflow.xml',
          'security/ir.model.access.csv',
          'security/law_tracking_group.xml',
    ],
    'init_xml': [   

    ],    
    'version': u'1.1',
    'css': [
        'static/src/css/note.css',
        'static/src/css/style.css',        
        ],
    'application': True,    
    'website': 'www.sistemasadhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
