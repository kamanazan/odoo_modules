from openerp import models,fields,api,_

class holiday_planning(models.Model):
    _name='holiday.planning'
    _description='define leave types and its duration'
    _inherit=['mail.thread','ir.needaction_mixin']

    name = fields.Char(string="Name",required=True)
    GlobalStartPeriod = fields.Datetime()
    GlobalEndPeriod = fields.Datetime()
    DefaultType = fields.Many2one('hr.holidays.status',ondelete='set null',string="Type")
    Status = fields.Char()
    LastApply=fields.Datetime()
    Mode = fields.Selection([('tag','By Employee Tag'),('employee','By Employee Name')],default='tag')
    ModeValue = fields.Char()
    Company = fields.Char()
    EmployeeName = fields.Many2one('hr.employee',string="Employee")
    EmployeeTag = fields.Many2one('hr.employee.category',string="Employee Tag")

class holiday_detail(models.Model):
    _name='holiday.detail'
    _description="details for each leave type"
    description = fields.Text()
    planning_id = fields.Many2one('holiday.planning',ondelete='cascade',string='Planning')
    StartPeriod = fields.Datetime()
    EndPeriod = fields.Datetime()
    LeaveType = fields.Char()
    WorkingDay = fields.Boolean(default=False)
