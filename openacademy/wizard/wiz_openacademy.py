from openerp import models, fields, api, _

class wiz_openacademy(models.TransientModel):
	_name = 'wiz.openacademy'
	_description = 'openacademy'

	session_id = fields.Many2one('openacademy.session', String="Session")
	attendee_ids = fields.One2many('wiz.openacademy.attendee', 'wiz_id', string="Attendee")

	@api.model
	def default_get(self, fields):
		print "self.env.context",self.env.context
		res = super(wiz_openacademy, self).default_get(fields)
		print "Res>>>>>>.",res
		if 'session_id' in fields:
			res['session_id'] = self.env.context.get('active_id')
		return res

	@api.one
	def create_attendee(self):
		attendee_obj = self.env['openacademy.attendee']
		for attendee in self.attendee_ids:
			attendee_obj.create({'partner_id': attendee.partner_id.id, 
				'session_id': self.session_id.id})


class wiz_openacademy_attendee(models.TransientModel):
	_name = "wiz.openacademy.attendee"
	_rec_name = 'partner_id'

	partner_id = fields.Many2one('res.partner', string="Partner")
	wiz_id = fields.Many2one('wiz.openacademy', string="Wizard")
