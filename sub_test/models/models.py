

from odoo import models, fields, api
import datetime
from datetime import timedelta

class HrLeave(models.Model):
    _inherit='hr.leave'
    
    test = fields.Char(string='Test')
    attendance_ids=fields.Char()
        
    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ Returns a float equals to the timedelta between two dates given as string."""
        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            return employee._get_work_days_data_batch(date_from, date_to)[employee.id]

        today_hours = self.env.company.resource_calendar_id.get_work_hours_count(
            datetime.combine(date_from.date(), time.min),
            datetime.combine(date_from.date(), time.max),
            False)
        if (self.holiday_status_id != "Sick Time Off"):
            hours = self.env.company.resource_calendar_id.get_work_hours_count(date_from, date_to)
        else:
            hours = self.env.company.resource_calendar_offone.get_work_hours_count(date_from, date_to)
        return {'days': hours / (today_hours or HOURS_PER_DAY), 'hours': hours}