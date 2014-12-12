{
    'name':'OpenAcademy',
    'version': '1.1',
    'author' : 'odoo',
    'summary': 'odoo training',
    'description' : '''
        well a training module
        - etcetera
        - etcetera
    ''',
    'category':'Extra Tool',
    'depends':['base','mail','website'],
    'data':['wizard/wiz_openacademy_view.xml',
            'views/openacademy_view.xml',
            'views/res_partner_view.xml',
            'views/openacademy_workflow.xml',
            'views/openacademy_templates.xml',
            'views/report_session.xml',
            'security/openacademy_security.xml',
            'security/ir.model.access.csv'],

    'website': 'super-odoo.com',
    'installable':True
}
