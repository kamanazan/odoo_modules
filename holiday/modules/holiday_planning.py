from openerp import models,fields,api,_

class HolidayPlanning(models.Model):
    @api.one
    def get_company_name(self):
        current_user = self.env['res.users']
        name_list = [x for x in current_user if type(x) == str]
        print '============================',name_list
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>",dir(current_user['company_id']['name'])
        self.company = current_user['company_id']
    _name='holiday.planning'
    _description='define leave types and its duration'
    _inherit=['mail.thread']

    name = fields.Char(string="Name",required=True)
    global_start_period = fields.Datetime()
    global_end_period = fields.Datetime()
    default_type = fields.Many2one('hr.holidays.status',ondelete='set null',string="Type")
    detail_ids = fields.One2many('holiday.detail','planning_id',string="Details")
    status = fields.Selection([('draft','Draft'),('apply','Applied')])
    last_apply = fields.Datetime()
    mode_type = fields.Selection([('tag','By Employee Tag'),('employee','By Employee Name')],default='tag')
    mode_value = fields.Char()#should change based on the choosen mode
    #current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
    #print "CURRENT USER",current_user
    company_id = fields.Many2one('res.company','Company',readonly=True)   
    employee_name = fields.Many2one('hr.employee',string="Employee",company_dependent=True)
    employee_tag = fields.Many2one('hr.employee.category',string="Employee Tag",company_dependent=True)
    _defaults = {#WTH??
            'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'sale.shop', context=c),
        }
class holiday_detail(models.Model):
    _name='holiday.detail'
    _description="details for each leave type"
    description = fields.Text(string="Description")
    planning_id = fields.Many2one('holiday.planning',ondelete='cascade',string='Planning')
    start_period = fields.Datetime(string="Start Period")
    end_period = fields.Datetime(string="End Period")
    leave_type = fields.Char()
    working_day = fields.Boolean(string="Working Day")
