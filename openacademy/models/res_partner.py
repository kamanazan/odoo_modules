from  openerp import api,fields,models,_

class res_partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(string='Instructor')
