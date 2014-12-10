from openerp import models,fields,api,_

class openacademy_course(models.Model):
    @api.one
    @api.depends('session_ids.attendee_ids')
    def get_attendee_count(self):
        attendee_count = 0
        for session in self.session_ids:
            attendee_count += len(session.attendee_ids)
        self.attendee_count = attendee_count
    _name = 'openacademy.course' #openacademy_course
    _description = 'course'
    #_log_acces = False
    #_auto = True
    #_table = 'course'
    #_order = 'name' #default id, ex: _order = 'name desc'
    #_inherit = 'mail.thread'
    #_inherits = {} 
    #_sql_constraint = [('name_unique',unique(name), 'Name must be unique')]
    
    #column fields
    name = fields.Char(string='Name',required=True,default='Test')#by default Char fields has no size
                                                    #limit
    responsible_id = fields.Many2one('res.users',string='Responsible',
        ondelete='cascade'
        )
    description = fields.Html()
    #one course has multiple sessions
    session_ids = fields.One2many('openacademy.session','course_id')
    attendee_count = fields.Integer(compute='get_attendee_count',string='No of Attendees',store=True)
    _sql_constraints = [('name_unique','unique(name)',_('Name must be unique'))]
    #string here represent label
    #copy, wether you want this field value copied when we duplicate the record
    #index, for searching optimization
    #default, when the field left blank default value will be used instead
    #help, a tooltip string
    #readonly, you can't edit this field, then it should've have a default value
    #states, possible values readonly,invisible.
    #   state itself is a dictionary field that must initialized
    #groups, decide which group can see this field
    #translate, whether you can translate this field or not
    #state = fields.Selection([('draft','Draft'),('confirm','Confirm')])
    #partner_id = fields.Many2one('res.partner',string='Attendant')
class openacademy_session(models.Model):
    @api.one
    @api.depends('attendee_ids')
    def get_attendee_count(self):
        self.attendee_count = len(self.attendee_ids)

    @api.one
    @api.depends('seats','attendee_ids')
    def get_remaining_seats(self):
        self.remaining_seats = self.seats and (100*(self.seats - len(self.attendee_ids)))/self.seats or 0.0

    _name = 'openacademy.session'
    _description = 'Session'
    name = fields.Char(string='Session Name',required=True)
    course_id = fields.Many2one('openacademy.course', string='course')
    active = fields.Boolean(default=True)
    duration = fields.Float()
    instructor = fields.Many2one('res.partner',string='Instructor')
    seats = fields.Integer(string='Seats')
    start_date = fields.Date(string='Start Date',default=fields.Date.today())
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('delay','Delay'),('done','Done'),('cancel','Cancel')], string='State',default='draft')
    attendee_ids = fields.One2many('openacademy.attendee','session_id',string='Attendee')
    attendee_count = fields.Integer(compute='get_attendee_count',string='No of Attendees',store=True)
    remaining_seats = fields.Float(compute='get_remaining_seats',string='Remaining seats',store=True)
    #partner_id = fields.Many2one('res.partner',string='Attendant')
    partner_email = fields.Char(related="instructor.email", string="Partner email")
    #relation model in odoo:
    # many2one,one2many
    # many2many
#related fields, relate a field to another model
#computed fields, relate a field to a function
class openacademy_attendee(models.Model):
    _name = 'openacademy.attendee'
    _description = 'Attendee'
    _rec_name = 'partner_id'
    partner_id = fields.Many2one('res.partner',string='Attendee')
    session_id = fields.Many2one('openacademy.session',string='Session')
