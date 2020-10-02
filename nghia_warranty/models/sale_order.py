from datetime import datetime

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_warranty = fields.Char(string='Product Warranty',
                                   readonly=True,
                                   compute='_product_warranty',
                                   store=False)
    price_warranty_discounted = fields.Monetary(compute='_compute_discount_on_warranty',
                                                string='Discounted Total', store=True)

    @api.depends('price_total')
    def _compute_discount_on_warranty(self):
        for line in self:
            date_to = line.product_id.date_to
            date_from = line.product_id.date_from
            now = datetime.now()

            if date_to and date_from and date_from < now < date_to:
                line.price_warranty_discounted = line.price_total
            else:
                line.price_warranty_discounted = line.price_total * 0.9

    def _product_warranty(self):
        for line in self:
            line.product_warranty = line.product_id.product_warranty


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_estimated = fields.Monetary(compute='_amount_discount',
                                         string='Discount Amount',
                                         store=True)
    calculated_discount_total = fields.Monetary(compute='_amount_discount',
                                                string='Discounted Total',
                                                store=True)

    @api.depends('amount_total', 'order_line')
    def _amount_discount(self):
        for order in self:
            amount_discounted_total = 0.0
            for line in order.order_line:
                amount_discounted_total += line.price_warranty_discounted
            order.update({
                'calculated_discount_total': amount_discounted_total,
                'discount_estimated': order.amount_total - amount_discounted_total,
            })
