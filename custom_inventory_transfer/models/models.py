from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from num2words import num2words as n2w
   

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    diminta_oleh = fields.Date(string='Diminta Oleh')
    pelaksana = fields.Many2one('res.partner', string='Pelaksana')

    def get_angka_ke_romawi(self,angka):
        nilai = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        simbol = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        romawi = ""
        i = 0
        while angka > 0:
            if angka >= nilai[i]:
                romawi += simbol[i]
                angka -= nilai[i]
            else:
                i += 1
        return romawi
    
    def get_angka_ke_terbilang(self, angka):
        words = str(float(angka)).split('.')[0]
        words = n2w(float(words), lang='id').title()
        number_to_words = words.replace("Koma Nol", "")
        return number_to_words


class StockMove(models.Model):
    _inherit = 'stock.move'

    keterangan = fields.Text(string='Keterangan')
    display_type = fields.Selection([('line_section', "Section"), ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer("sequence")

    def _action_confirm(self, merge=True, merge_into=False):
        for move in self:
            if move.display_type == 'line_section':
               merge = False
        return super(StockMove, self)._action_confirm(merge, merge_into)
    
    @api.onchange('display_type')
    def _onchange_display_type(self):
        if self.display_type == 'line_section':
            self.state == 'cancel'
            product = self.env.ref('custom_inventory_transfer.display_section_product_product')
            if product:
                self.product_id = product.id
                self.name = product.name
                self.product_uom = product.uom_id.id


    


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def unlink(self):
        for product in self:
            if product.id == self.env.ref('custom_inventory_transfer.display_section_product_product').product_tmpl_id.id:
                raise UserError(_('You can not delete this product because it is used in the system.'))
        return super(ProductProduct, self).unlink()
    

    
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    @api.multi
    def unlink(self):
        for product in self:
            if product.id == self.env.ref('custom_inventory_transfer.display_section_product_product').id:
                raise UserError(_('You can not delete this product because it is used in the system.'))
        return super(ProductProduct, self).unlink()
    
    