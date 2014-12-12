from openerp import models,api

class SessionReport(models.AbstractModel):
    _name= 'report.openacademy.report_session'

    def get_user_email(self):
        if self.env.user:
            return self.env.user.email
    @api.multi
    def render_html(self,data=None):
        report_obj = self.env['report']
        session_obj = self.env['openacademy.session']
        report = report_obj._get_report_from_name('openacademy.report_session')
        session_ids = session_obj.search([])

        docargs = {
            'doc_ids' :session_ids.ids,
            'doc_model' : report.model,
            'docs':session_ids,
            'user_email':self.get_user_email
        }
        
        return report_obj.render('openacademy.report_session',docargs)
    
