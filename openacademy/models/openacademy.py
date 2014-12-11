from openerp import models,fields,api,_
from openerp.exceptions import Warning

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
    description = fields.Text()
    #one course has multiple sessions
    session_ids = fields.One2many('openacademy.session','course_id')
    attendee_count = fields.Integer(compute='get_attendee_count',string='No of Attendees',store=True)

    #this is python constraint
    @api.one
    @api.constrains('name','description')
    def _check_name_description(self):
        if self.name == self.description:
            raise Warning(_('Error! Name and description cannot be same'))
    _sql_constraints = [('name_unique','unique(name)',_('Name must be unique'))]#this is postgresql constraint
    #modify what appear in the course dropdown menu
    #ofcourse since we are going to show multiple course we use api.multi
    @api.multi
    def name_get(self):
        res = []
        name = ''
        for course in self:
            if course.responsible_id:
                name = course.name + "(" + course.responsible_id.name + ")"
            res.append((course.id,name))
        return res
    
    
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
    _inherit=['mail.thread','ir.needaction_mixin']
    _name = 'openacademy.session'
    _description = 'Session'
    
    #fields
    name = fields.Char(string='Session Name',required=True)
    
    course_id = fields.Many2one('openacademy.course', string='course')
    
    active = fields.Boolean(default=True)
    
    duration = fields.Float()
    
    instructor_id = fields.Many2one('res.partner',string='Instructor',domain=[('instructor','=',True)],track_visibility='always')
    
    seats = fields.Integer(string='Seats')
    
    start_date = fields.Date(string='Start Date',default=fields.Date.today())
    
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),
        ('delay','Delay'),('done','Done'),('cancel','Cancel')], 
        string='State',default='draft',track_visibility='onchange',
    )
    
    color = fields.Integer() 
    
    attendee_ids = fields.One2many('openacademy.attendee','session_id',string='Attendee')
    attendee_count = fields.Integer(compute='get_attendee_count',string='No of Attendees',store=True)
    remaining_seats = fields.Float(compute='get_remaining_seats',string='Remaining seats',store=True)
    #partner_id = fields.Many2one('res.partner',string='Attendant')
    partner_email = fields.Char(related="instructor_id.email", string="Partner email")
    #relation model in odoo:
    # many2one,one2many
    # many2many
    @api.one
    @api.constrains('instructor_id','attendee_ids')
    def _check_name_description(self):
        if self.instructor_id.id in [attendee.partner_id.id for attendee in self.attendee_ids]:
            raise Warning(_('Error! Instructor cannot be Attendee'))
    @api.onchange('seats','attendee_ids')
    def onchange_seats_attendee(self):
        print "self",self
        self.remaining_seats = self.seats and (100*(self.seats - len(self.attendee_ids)))/self.seats or 0.0

    @api.model
    def create(self,values):
        print "create values",values
        #if not values:
        #    values['name']
        return super(openacademy_session,self).create(values)

    @api.multi
    def write(self,values):
        print "write values",values
        return super(openacademy_session,self).write(values)
    #decide what will happen to the values when we duplicate the record/model/whateveritcalled
    @api.one
    def copy(self,default):
        default['name'] = 'Copy of %s' % self.name
        default['instructor_id'] = False
        return super(openacademy_session,self).create(default)

    #buttons
    @api.one
    def action_confirm(self):
        self.message_post(body=_("session is <b>CONFIRMED</b> brow!"))
        self.state='confirm'
    @api.one
    def action_cancel(self):
        self.state='cancel'
    @api.one
    def action_delay(self):
        self.state='delay'
    @api.one
    def action_done(self):
        self.state='done'
    @api.model
    def _needaction_domain_get(self):
        return [('state','=','confirm')]

#related fields, relate a field to another model
#computed fields, relate a field to a function
class openacademy_attendee(models.Model):
    _name = 'openacademy.attendee'
    _description = 'Attendee'
    _rec_name = 'partner_id'
    partner_id = fields.Many2one('res.partner',string='Attendee',domain=[('instructor','=',False)])
    session_id = fields.Many2one('openacademy.session',string='Session')

    _sql_constraints = [('partner_session_unique','unique(partner_id,session_id)',_('Attendee must be unique for each session!'))]
