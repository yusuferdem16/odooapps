from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CarLogServices(models.Model):
    _name = 'car.log.services'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Services for vehicles'

    active = fields.Boolean(default=True)
    car_id = fields.Many2one('leasing.car', string='Vehicle', required=True)
    customer_id = fields.Many2one('leasing.customer', string='Customer', store=True)
    odometer_id = fields.Many2one('fleet.vehicle.odometer', 'Odometer',
                                  help='Odometer measure of the vehicle at the moment of this log')
    odometer = fields.Float(
        compute="_get_odometer", inverse='_set_odometer', string='Odometer Value',
        help='Odometer measure of the vehicle at the moment of this log')
    date = fields.Date(help='Date when the cost has been executed', default=fields.Date.context_today)
    notes = fields.Text()

    def _get_odometer(self):
        self.odometer = 0
        for record in self:
            if record.odometer_id:
                record.odometer = record.odometer_id.value

    def _set_odometer(self):
        for record in self:
            if not record.odometer:
                raise UserError(_('Emptying the odometer value of a vehicle is not allowed.'))
            odometer = self.env['fleet.vehicle.odometer'].create({
                'value': record.odometer,
                'date': record.date or fields.Date.context_today(record),
                'vehicle_id': record.vehicle_id.id
            })
            self.odometer_id = odometer

    @api.model_create_multi
    def create(self, vals_list):
        for data in vals_list:
            if 'odometer' in data and not data['odometer']:
                del data['odometer']
        return super(CarLogServices, self).create(vals_list)
