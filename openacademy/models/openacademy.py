from openerp import models, fields, api, _
from openerp.exceptions import Warning

class openacademy_course(models.Model):
	_name = 'openacademy.course'
	_description = 'course'

	@api.one
	@api.depends('session_ids.attendee_ids')
	def get_attendee_count(self):
		attendee_count = 0
		for session in self.session_ids:
			attendee_count += len(session.attendee_ids)
		self.attendee_count = attendee_count

	name = fields.Char(string="Title", required=True)
	responsible_id = fields.Many2one('res.users', string="Responsible", ondelete="cascade")
	description = fields.Text()
	session_ids = fields.One2many('openacademy.session', 'course_id', string='Session')
	attendee_count = fields.Integer(compute='get_attendee_count', string="No of Attendees", store=True)
	image = fields.Binary()
	
	@api.one
	@api.constrains('name','description')
	def _check_name_description(self):
		if self.name == self.description:
			raise Warning(_('Error!, Name and description cannot be same!!'))


	_sql_constraints = [('name_unique', 'unique(name)', _('Name must be unique!!'))]
#for old api
#	_constraints = [(_check_descritiption, 'name and description cannot be same',
				# ['name', 'description'])]
	@api.multi
	def name_get(self):
		res = []
		name = ''
		for course in self:
			if course.responsible_id:
				name = course.name + "(" + course.responsible_id.name + ")"
			res.append((course.id,name))
		#[(1,name), (2,name)]
		return res

class openacademy_session(models.Model):
	_name = 'openacademy.session'
	_description = 'Session'
	_inherit = ['mail.thread','ir.needaction_mixin']

	@api.one
	@api.depends('attendee_ids')
	def get_attendee_count(self):
		self.attendee_count = len(self.attendee_ids)

	@api.one
	@api.depends('seats', 'attendee_ids')
	def get_remaining_seats(self):
		self.remaining_seats =  self.seats and (100*(self.seats - len(self.attendee_ids)))/self.seats or 0.0


	#old api		
# 	def get_attendee_count(self, cr, uid, ids, fields_name, args, context=None):
# 		res = {}
# 		for session in self.browse(cr, uid, ids, context=context)
		
# 			res[session.id] = len(session.attendee_ids)
# #{1: 12}
# 		return res


	name = fields.Char(string='Session Name', required=True)
	course_id = fields.Many2one('openacademy.course', string='course', ondelete='cascade', track_visibility='always')
	active = fields.Boolean(default=True)
	duration = fields.Float()
	instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor','=',True)], track_visibility='always')
	seats = fields.Integer(string="Seats")
	start_date = fields.Date(string="Start Date", default=fields.Date.today())
	state = fields.Selection([('draft','Draft'), 
		                      ('confirm','Confirm'),
		                      ('delay','Delay'),
		                      ('done','Done'),
		                      ('cancel','Cancel')], string="State", default='draft', track_visibility='onchange')
	attendee_ids = fields.One2many('openacademy.attendee', 'session_id', string="Attendee")
	attendee_count = fields.Integer(compute='get_attendee_count', string="No of Attendees", store=True)
	remaining_seats = fields.Float(compute='get_remaining_seats', string="Remaining Seats", store=True)
	partner_email = fields.Char(related='instructor_id.email', string="Partner Email")
	color = fields.Integer(string="Color Index",default=0)
	
	@api.one
	@api.constrains('instructor_id','attendee_ids')
	def _check_instructor_attendee(self):
		if self.instructor_id.id in [attendee.partner_id.id for attendee in self.attendee_ids]:
			raise Warning(_('Error!, instructor cannot be Attendee!!'))

	@api.onchange('seats','attendee_ids')
	def onchange_seats_attendee(self):
		print "self",self
		self.remaining_seats = self.seats and (100*(self.seats - len(self.attendee_ids)))/self.seats or 0.0

	@api.model
	def create(self, values): #def create(self, cr, uid, values, context=None)
		print "valuesss",values
		return super(openacademy_session,self).create(values)

	@api.multi
	def write(self, values):# def write(self, cr, uid, ids, values, context=None)
		print "valuesss",values
		return super(openacademy_session,self).write(values)

	@api.one
	def copy(self, default):#def copy(self, cr, uid, id, default=None, context=None)
		default['name'] = "Copy of %s"% self.name
		default['instructor_id'] = False
		return super(openacademy_session, self).copy(default)

	@api.multi
	def unlink(self):# def unlink(self, cr, uid, ids, context=None)
		return super(openacademy_session, self).unlink()

	@api.one
	def action_confirm(self):
		self.message_post(body=_("Session is <b>Confirmed</b>"))
		self.state = 'confirm'

	@api.one
	def action_cancel(self):
		self.state = 'cancel'
	@api.one
	def action_delay(self):
		self.state = 'delay'
	@api.one
	def action_done(self):
		self.state = 'done'

	@api.model
	def _needaction_domain_get(self):
		return [('state','=','confirm')]


class openacademy_attendee(models.Model):
	_name = 'openacademy.attendee'
	_description = 'Attendee'
	_rec_name = 'partner_id'

	partner_id = fields.Many2one('res.partner', string='Attendee')
	session_id = fields.Many2one('openacademy.session', string="Session")

	_sql_constraints = [('partner_session_unique', 'unique(partner_id,session_id)','Attendee must be unique for one session!!')]