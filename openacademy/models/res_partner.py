from openerp import models,fields,api,_

class res_partner(models.Model):
	_inherit = 'res.partner'

	instructor = fields.Boolean(string="Instructor",default=False)

