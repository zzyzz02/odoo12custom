# -*- coding: utf-8 -*-
from odoo import http

# class StockCardReport(http.Controller):
#     @http.route('/stock_card_report/stock_card_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_card_report/stock_card_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_card_report.listing', {
#             'root': '/stock_card_report/stock_card_report',
#             'objects': http.request.env['stock_card_report.stock_card_report'].search([]),
#         })

#     @http.route('/stock_card_report/stock_card_report/objects/<model("stock_card_report.stock_card_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_card_report.object', {
#             'object': obj
#         })