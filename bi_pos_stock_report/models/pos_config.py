from odoo import fields,api,models,_


class pos_user(models.Model):
    _inherit = 'pos.config'

    # product summary report
    print_product_summary = fields.Boolean(string="Product Summary Report")
    no_of_product_receipt = fields.Integer(string="No.of Copy Receipt")
    product_current_month_date = fields.Boolean(string="Current Month Date")
    signature = fields.Boolean(string="Signature")

    # order summary report
    enable_order_summary = fields.Boolean(string='Enable Order Summary')
    no_of_order_receipt = fields.Integer(string="No.of Copy Receipt")
    order_current_month_date = fields.Boolean(string="Current Month Date")
    signature = fields.Boolean(string="Signature")

    # payment summary report
    payment_summary = fields.Boolean(string="Payment Summary")
    payment_current_month_date = fields.Boolean(string="Current Month Date")

    # audit report
    print_audit_report = fields.Boolean("Print Stock Report")


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def get_html_report(self, id, report_name):
        report = self._get_report_from_name(report_name)
        document = report.render_qweb_html([id], data={})
        if document:
            return document
        return False
