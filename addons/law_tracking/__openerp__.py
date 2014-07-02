# -*- coding: utf-8 -*-
##############################################################################
#
#    Law Follow Up
#    Copyright (C) 2014 Sistemas ADHOC
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
    'demo_xml': [],
    'depends': [u'mail', u'contacts'],
    'description': u'Law Follow Up',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Law Follow Up',
    'test': [],
    'update_xml': [   u'security/law_tracking_group.xml',
                      u'view/legislature_view.xml',
                      u'view/treatment_detail_view.xml',
                      u'view/commission_treatment_view.xml',
                      u'view/commission_position_view.xml',
                      u'view/log_view.xml',
                      u'view/law_project_document_view.xml',
                      u'view/enclosure_treatment_detail_view.xml',
                      u'view/order_paper_view.xml',
                      u'view/law_project_view.xml',
                      u'view/legislature_member_view.xml',
                      u'view/commission_detail_view.xml',
                      u'view/partner_view.xml',
                      u'view/block_view.xml',
                      u'view/subscription_view.xml',
                      u'view/law_tracking_menuitem.xml',
                      u'data/legislature_properties.xml',
                      u'data/treatment_detail_properties.xml',
                      u'data/commission_treatment_properties.xml',
                      u'data/commission_position_properties.xml',
                      u'data/log_properties.xml',
                      u'data/law_project_document_properties.xml',
                      u'data/enclosure_treatment_detail_properties.xml',
                      u'data/order_paper_properties.xml',
                      u'data/law_project_properties.xml',
                      u'data/legislature_member_properties.xml',
                      u'data/commission_detail_properties.xml',
                      u'data/partner_properties.xml',
                      u'data/block_properties.xml',
                      u'data/subscription_properties.xml',
                      u'data/legislature_track.xml',
                      u'data/treatment_detail_track.xml',
                      u'data/commission_treatment_track.xml',
                      u'data/commission_position_track.xml',
                      u'data/log_track.xml',
                      u'data/law_project_document_track.xml',
                      u'data/enclosure_treatment_detail_track.xml',
                      u'data/order_paper_track.xml',
                      u'data/law_project_track.xml',
                      u'data/legislature_member_track.xml',
                      u'data/commission_detail_track.xml',
                      u'data/partner_track.xml',
                      u'data/block_track.xml',
                      u'data/subscription_track.xml',
                      u'workflow/commission_treatment_workflow.xml',
                      u'workflow/order_paper_workflow.xml',
                      u'workflow/legislature_member_workflow.xml',
                      u'workflow/subscription_workflow.xml',
                      'security/ir.model.access.csv'],
    'version': u'1.1',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
