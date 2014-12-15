{
	'name': 'OpenAcademy',
	'version': "1.1",
	'author': "odoo S.A.",
	'summary': 'Openacademy Course, Session and Attendees',
	'category': 'Tools',
	'description': """
This Module is Used
* Training Course
* Training Session
* Training Attendees
	""",
	'depends': ['base', 'mail', 'website'],
	'data': ['wizard/wiz_openacademy_view.xml',
	'security/openacademy_security.xml',
	'security/ir.model.access.csv',
	'views/openacademy_view.xml',
		'views/res_partner_view.xml',
		'views/openacademy_workflow.xml',
		'views/openacademy_template.xml','views/report_session.xml'
		],
	'css': ['static/src/css/openacademy.css'],
	'website': 'www.odoo.com',
	'installable': True
}