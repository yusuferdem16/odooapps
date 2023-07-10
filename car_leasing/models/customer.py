from datetime import date
from odoo import api, fields, models

class LeasingCustomer(models.Model):
    _name ="leasing.customer"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Leasing Customer"

    name = fields.Char(string="Name",tracking=True)
    date_of_birth = fields.Date(string="Date of Birth")
    ref = fields.Char(string="ID:Number",tracking=True)
    age = fields.Integer(string="Age",compute='_compute_age', tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')], string="Gender",tracking=True)
    active = fields.Boolean(string="Active",default=True,tracking=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
       for rec in self:
           today = date.today()
           if rec.date_of_birth:
               rec.age = today.year - rec.date_of_birth.year
           else:
               rec.age = 0
