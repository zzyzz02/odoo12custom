# -*- coding: utf-8 -*-
from odoo import http

# class CustomInventoryTransfer(http.Controller):
#     @http.route('/custom_inventory_transfer/custom_inventory_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_inventory_transfer/custom_inventory_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_inventory_transfer.listing', {
#             'root': '/custom_inventory_transfer/custom_inventory_transfer',
#             'objects': http.request.env['custom_inventory_transfer.custom_inventory_transfer'].search([]),
#         })

#     @http.route('/custom_inventory_transfer/custom_inventory_transfer/objects/<model("custom_inventory_transfer.custom_inventory_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_inventory_transfer.object', {
#             'object': obj
#         })