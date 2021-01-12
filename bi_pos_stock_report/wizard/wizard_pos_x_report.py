from odoo import fields, models, api, _

class wizard_pos_x_report(models.TransientModel):
    _name = 'wizard.pos.x.report'

    @api.model
    def get_ip(self):
        proxy_ip = self.env['res.users'].browse([self._uid]).company_id.report_ip_address or''
        return proxy_ip

    def print_x_report(self):
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'wizard.pos.x.report'}
        return self.env.ref('bi_pos_stock_report.report_pos_sales_pdf_front').report_action(self, data=datas)

    session_ids = fields.Many2many('pos.session', 'pos_session_wizard_rel', 'x_wizard_id', 'pos_session_id', string="Session(s)")
    report_type = fields.Selection([('thermal', 'Thermal'),
                                    ('pdf', 'PDF')], default='pdf', readonly=True, string="Report Type")
    proxy_ip = fields.Char(string="Proxy IP", default=get_ip)
