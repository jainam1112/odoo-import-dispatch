from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    eway_bill_no = fields.Char(string="E-Way Bill No")
    grn_attachment = fields.Binary(string="Goods Receipt Note")
    grn_filename = fields.Char(string="GRN Filename")
    customer_confirmed = fields.Boolean(string="Customer Confirmed")
