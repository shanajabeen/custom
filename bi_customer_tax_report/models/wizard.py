from odoo import api, models, fields,tools, _
from datetime import date
class ProductTaxWiseReport(models.TransientModel):
	_name = 'bi.product.tax'
    
	# product_id = fields.Many2one('product.product', string='Product')
	date_from = fields.Date(string="Date From", default=lambda *a: date.today())
	date_to= fields.Date(string="Date To", default=lambda *a: date.today())
	
	def print_report_xls(self):		
		context = self._context
		datas = {'ids': context.get('active_ids', [])}
		datas['form'] = self.read()[0]
		for field in datas['form'].keys():
			if isinstance(datas['form'][field], tuple):
				datas['form'][field] = datas['form'][field][0]
		return self.env.ref('bi_customer_tax_report.report_cust_tax_id').report_action(self, data=datas,
																							 config=False)

