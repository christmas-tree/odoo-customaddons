from datetime import datetime

from dateutil import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


def stringify_timedelta(datetime1, datetime2):
    text = ''
    remaining_time = relativedelta.relativedelta(datetime1, datetime2)
    if remaining_time.years > 0:
        text += str(remaining_time.years) + ' years ' if remaining_time.years > 1 else ' year '
    if remaining_time.months > 0:
        text += str(remaining_time.months) + ' months ' if remaining_time.months > 1 else ' month '
    if remaining_time.days > 0:
        text += str(remaining_time.days) + ' days ' if remaining_time.days > 1 else ' day '

    return text


class Product(models.Model):
    _inherit = 'product.template'

    date_to = fields.Datetime('Date To')
    date_from = fields.Datetime('Date From')
    product_warranty = fields.Char('Product Warranty',
                                   compute='_compute_warranty_code',
                                   store=True)
    warranty_text = fields.Char('Warranty left',
                                compute='_compute_warranty_text',
                                store=False)

    @api.depends('date_to', 'date_from')
    def _compute_warranty_code(self):
        for product in self:
            if product.date_to and product.date_from:
                product.product_warranty = 'PWD/' + \
                                           product.date_from.strftime('%y%m%d') + '/' + \
                                           product.date_to.strftime('%y%m%d')
            else:
                product.product_warranty = ''

    @api.depends('date_to', 'date_from')
    def _compute_warranty_text(self):
        for product in self:
            now = datetime.now()

            if product.date_to and product.date_from:
                if product.date_from > now:
                    product.warranty_text = 'Not started'
                    return

                if product.date_to < now:
                    product.warranty_text = 'Expired'
                    return

                product.warranty_text = stringify_timedelta(product.date_to, now)
                return

            if product.date_to and not product.date_from:
                product.warranty_text = stringify_timedelta(product.date_to, now)
                return

            product.warranty_text = 'Lifetime'

    @api.constrains('date_to', 'date_from')
    def _check_warranty_date(self):
        for product in self:
            if product.date_from and product.date_to and product.date_from >= product.date_to:
                raise ValidationError(
                    _('Warranty start date cannot be after the end date.'))
        return True


class WarrantySettings(models.TransientModel):
    _name = 'warranty.warranty_wizard'
    _description = "Wizard: Warranty Mass Update"

    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date To')
    product_warranty = fields.Char('Product Warranty',
                                   compute='_compute_warranty_code',
                                   store=True)

    def mass_update(self):
        selected = self.env['product.template'].browse(self._context['active_ids'])
        for c in selected:
            c.date_from = self.date_from
            c.date_to = self.date_to

    @api.depends('date_to', 'date_from')
    def _compute_warranty_code(self):
        for product in self:
            if product.date_to and product.date_from:
                product.product_warranty = 'PWD/' + \
                                           product.date_from.strftime('%y%m%d') + '/' + \
                                           product.date_to.strftime('%y%m%d')
            else:
                product.product_warranty = ''

    @api.constrains('date_to', 'date_from')
    def _check_warranty_date(self):
        for product in self:
            if product.date_from and product.date_to and product.date_from >= product.date_to:
                raise ValidationError(
                    _('Warranty start date cannot be after the end date.'))
        return True
