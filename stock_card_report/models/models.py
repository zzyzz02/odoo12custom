# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class StockCardReportWizard(models.TransientModel):
    _name = 'stock.card.report.wizard'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    penjelasan = fields.Char(string='Penjelasan')
    start_date = fields.Date(string='Start Date', required=True, default=datetime.now().date())
    end_date = fields.Date(string='End Date', required=True, default=datetime.now().date())
    location_id = fields.Many2one(comodel_name="stock.location", string="Location", required=True)


    @api.onchange("location_id","company_id")
    def onchange_location_id(self):
        ids_location = []
        domain = {}
        
        location_ids = self.env['stock.location'].sudo().search([('usage','=','internal'),('company_id','=', self.company_id.id)])
        for location in location_ids:
            ids_location.append(location.id)

        domain['location_id'] = [('id','in', ids_location)]
        return {'domain':domain}

    def _get_data_report(self):

        DATA_REPORT_LINE = []

        beginning_qty = 0

        tmp_start_date = datetime.combine(self.start_date, datetime.min.time())
        tmp_end_date = datetime.combine(self.end_date, datetime.max.time())
        location_id = self.location_id.id
        product = self.product_id


        self._cr.execute(
                """ SELECT sm.id
                        FROM stock_move AS sm
                    WHERE
                        (sm.location_id=%s OR sm.location_dest_id=%s) AND sm.product_id=%s AND sm.date<=%s  AND sm.state='done'
                """, (location_id, location_id, product.id, tmp_end_date.strftime("%Y-%m-%d %H:%M:%S"), ))
        move_ids = self.env['stock.move'].browse([r[0] for r in self._cr.fetchall()])
        for move in move_ids.filtered(lambda mv: mv.date < tmp_start_date):
            if move.location_id.id == location_id:
                beginning_qty -= move.product_uom_qty
            elif move.location_dest_id.id == location_id:
                beginning_qty += move.product_uom_qty

        DATA_REPORT_LINE.append({
            'date'              : tmp_start_date.strftime("%Y-%m-%d %H:%M:%S"),
            'operation'         : 'Beginning Balance',
            'reference'         : 'Beginning Balance',
            'move_in'           : beginning_qty if beginning_qty > 0 else 0,
            'move_out'          : beginning_qty if beginning_qty < 0 else 0,
            'balance_qty'       : beginning_qty,
        })

        balance_qty = beginning_qty
        is_mutation = False
        for move in move_ids.filtered(lambda mv: mv.date >= tmp_start_date and mv.date <= tmp_end_date):
            balance_qty += move.product_uom_qty * -1 if move.location_id.id == location_id else move.product_uom_qty
            is_mutation = True

            DATA_REPORT_LINE.append({
                'date'              : move.date.strftime("%Y-%m-%d %H:%M:%S"),
                'operation'         : move.picking_id.picking_type_id.name if move.picking_id.picking_type_id else '',
                'reference'         : move.picking_id.name if move.picking_id else '',
                'move_in'           : move.product_uom_qty if move.location_dest_id.id == location_id else 0,
                'move_out'          : move.product_uom_qty if move.location_id.id == location_id else 0,
                'balance_qty'       : balance_qty,
            })
        
            
        return DATA_REPORT_LINE





    def print_report(self):
        data = {
            
            'product_name'     : self.product_id.name,
            'product_code'     : self.product_id.default_code,
            'product_uom'      : self.product_id.uom_id.name,
            'penjelasan'       : self.penjelasan,
            'lines'            : self._get_data_report(),
        }

        return self.env.ref('stock_card_report.action_stock_card_report').report_action(self, data=data)