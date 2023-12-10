# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CaraPembayaran(models.Model):
    _name = 'cara.pembayaran'
    _description = 'Cara Pembayaran'

    name = fields.Char(string='Cara Pembayaran', required=True)
    active = fields.Boolean(string='Active', default=True)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    cara_pembayaran_id = fields.Many2one('cara.pembayaran', string='Cara Pembayaran')


