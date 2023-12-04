# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    tanggal_dibutuhkan = fields.Date(string='Tanggal Dibutuhkan')


    def get_waktu_hari(self):
        for rec in self:
            waktu_hari = "............"

            if rec.tanggal_dibutuhkan:
                waktu_hari = (rec.tanggal_dibutuhkan - datetime.now().date()).days
            
            return waktu_hari



