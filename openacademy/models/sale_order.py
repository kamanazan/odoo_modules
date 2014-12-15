from openerp import models,fields

class sale_order(models.Model):
    _inherit = 'sale.order'

    email = fields.Char(related='partner_id.email')
