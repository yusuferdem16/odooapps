from datetime import date
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.osv import expression


class LeasingCar(models.Model):
    _name = "leasing.car"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Car"
    _rec_name = "plate"

    plate = fields.Char(string="Name", tracking=True)
    model_year = fields.Date(string="Model Year")
    odometer_count = fields.Integer(compute="_compute_count_all", string='Odometer')
    odometer = fields.Float(compute='_get_odometer', inverse='_set_odometer', string='Last Odometer',
                            help='Odometer measure of the vehicle at the moment of this log')
    brand = fields.Selection([('bmw', 'Bmw'), ('mercedes', 'Mercedes')], string="Brand", tracking=True)
    age = fields.Integer(string="Year of Service", compute='_compute_age', tracking=True)
    fuel_type = fields.Selection([('diesel', 'Diesel'), ('electrical', 'Electrical')], string="Type Of Fuel",
                                 tracking=True)
    price_daily = fields.Integer(string="Daily Price", tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)

    @api.depends('model_year')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.model_year:
                rec.age = today.year - rec.model_year.year
            else:
                rec.age = 0

    def _get_odometer(self):
        CarOdometer = self.env['leasing.car.odometer']
        for record in self:
            vehicle_odometer = CarOdometer.search([('car_id', '=', record.id)], limit=1,
                                                           order='value desc')
            if vehicle_odometer:
                record.odometer = vehicle_odometer.value
            else:
                record.odometer = 0


    def _set_odometer(self):
        for record in self:
            if record.odometer:
                date = fields.Date.context_today(record)
                data = {'value': record.odometer, 'date': date, 'car_id': record.id}
                self.env['leasing.car.odometer'].create(data)


    def _compute_count_all(self):
        Odometer = self.env['leasing.car.odometer']
        odometers_data = Odometer.read_group([('car_id', 'in', self.ids)], ['car_id'], ['car_id'])

        mapped_odometer_data = defaultdict(lambda: 0)

        for odometer_data in odometers_data:
            mapped_odometer_data[odometer_data['car_id'][0]] = odometer_data['car_id_count']

        for car in self:
            car.odometer_count = mapped_odometer_data[car.id]

    def return_action_to_open(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:

            res = self.env['ir.actions.act_window']._for_xml_id('fleet.%s' % xml_id)
            res.update(
                context=dict(self.env.context, default_car_id=self.id, group_by=False),
                domain=[('car_id', '=', self.id)]
            )
            return res
        return False