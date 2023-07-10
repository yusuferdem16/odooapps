from datetime import date, timedelta
from dateutil import relativedelta
from odoo import api, fields, models


class LeasingAppointment(models.Model):
    _name = "leasing.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Leasing Appointment"
    _rec_name = "customer_id"

    car_id = fields.Many2one('leasing.car', string="Car", tracking=True)
    customer_id = fields.Many2one('leasing.customer', string="Customer", tracking=True)
    gender = fields.Selection(tracking=True, related='customer_id.gender')
    ending_day = fields.Date(string="Ending Day", tracking=True, defualt=fields.Date.context_today)
    starting_day = fields.Date(string="Starting Day", tracking=True, default=fields.Date.context_today)
    days_in_total = fields.Integer(string="Days", compute='_compute_days', tracking=True)
    price_total = fields.Integer(string="Total Price", compute='_compute_price_total', tracking=True)
    ref = fields.Char(string="Reference", tracking=True, readonly=True)
    notes = fields.Html(string="Additional Notes")

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        self.ref = self.customer_id.ref

    @api.depends('starting_day', 'ending_day')
    def _compute_days(self):
        for rec in self:
            if rec.ending_day:
                rec.days_in_total = (rec.ending_day - rec.starting_day).days
            else:
                rec.days_in_total = 0

    @api.depends('days_in_total')
    def _compute_price_total(self):
        for rec in self:
            if rec.days_in_total:
                if not rec.days_in_total < 0:
                    rec.price_total = rec.car_id.price_daily * rec.days_in_total
                else:
                    rec.price_total = 0
            else:
                rec.price_total = 0

