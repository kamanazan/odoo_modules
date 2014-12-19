{
	'name': 'Day-off Planning',
	'version': "1.0",
	'author': "ezee-it team",
	'summary': 'Day-off planning',	
    'category': 'addons',
	'description': """
    This Module can:
* Define planning for a leave type
* Allocate leave time by employee or employee tag
* Modify planning
* Delete planning
	""",
	'depends': ['base','hr_holidays',],
	'data': ['views/holiday_planning_view.xml','views/holiday_planning_workflow.xml'],	
    'css': [],
	'website': 'www.odoo.com',
	'installable': True
}
