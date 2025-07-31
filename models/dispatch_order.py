# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class DispatchOrder(models.Model):
    _name = 'dispatch.order'
    _description = 'Dispatch Order'
    _order = 'date_order desc, name desc'

    name = fields.Char('Order Reference', required=True, copy=False, readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date_order = fields.Datetime('Order Date', required=True, default=datetime.now)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    order_line = fields.One2many('dispatch.order.line', 'order_id', string='Order Lines')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('dispatch.order') or 'New'
        return super(DispatchOrder, self).create(vals)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'


class DispatchOrderLine(models.Model):
    _name = 'dispatch.order.line'
    _description = 'Dispatch Order Line'

    order_id = fields.Many2one('dispatch.order', string='Order Reference', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Text('Description')
    quantity = fields.Float('Quantity', default=1.0, required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
