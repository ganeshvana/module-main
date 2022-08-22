from odoo import api, fields, models, tools, _

class stock_warehouse(models.Model):
    _inherit = "stock.warehouse"


    # image_variant_1920 = fields.Image("Variant Image", max_width=1920, max_height=1920)

    product_image = fields.Binary(string='Image')

    

class stock_picking(models.Model):
    _inherit = "stock.picking"

    # vehicle_number = fields.Char(string="Vehicle No.", copy=False)
    # so_id = fields.Many2one('sale.order','SO',compute='_get_sale')
    date = fields.Many2one('purchase.order','SO',compute='_get_purchase')
    so_id = fields.Many2one('sale.order','SO Number',compute='_get_sale')
    reference_number = fields.Char(string="Reference", copy=False)







    # @api.depends('origin')
    # def _get_sale(self):
    #     for record in self:
    #         record.so_id = ''
    #         if record.origin:
    #             so_obj = self.env['sale.order'].search([('name','=',record.origin)])
    #             if so_obj:
    #                 record.so_id = so_obj.id
    #             else:
    #                 record.so_id = '' 



    @api.depends('origin')
    def _get_purchase(self):
        for record in self:
            record.date = ''
            if record.origin:
                so_obj = self.env['purchase.order'].search([('name','=',record.origin)])
                if so_obj:
                    record.date = so_obj.id
                else:
                    record.date = '' 


    @api.depends('origin')
    def _get_sale(self):
        for record in self:
            record.so_id = ''
            if record.origin:
                so_obj = self.env['sale.order'].search([('name','=',record.origin)])
                if so_obj:
                    record.so_id = so_obj.id
                else:
                    record.so_id = '' 

