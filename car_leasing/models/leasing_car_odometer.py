# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class CarOdometer(models.Model):
    _name = 'leasing.car.odometer'
    _description = 'Odometer log for a vehicle'
    _order = 'date desc'

    customer_id = fields.Many2one('leasing.customer', string="Customer", tracking=True)
    name = fields.Char(compute='_compute_vehicle_log_name', store=True)
    date = fields.Date(default=fields.Date.context_today)
    value = fields.Float('Odometer Value', group_operator="max")
    car_id = fields.Many2one('leasing.car', 'Vehicle', required=True)

