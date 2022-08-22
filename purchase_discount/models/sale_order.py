# Copyright 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# Copyright 2015-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount = fields.Float(string="Discount (%)", digits="Discount")

    @api.depends("discount")
    def compute_discount(self):
        for line in self.order_line:
            if line.apply_discount == True and self.discount > 0:
                line.update({'discount':self.discount})
            else:
                line.update({'discount':0})
                
    # def action_confirm(self):
    #     result = super(SaleOrder, self).action_confirm()
    #     for rec in self:
    #         for res in rec.order_line:
    #             if res.product_id.website_id.khazana == True:
    #                 if res.product_id.intransit:
    #                     res.product_id.product_tmpl_id.sold_units += res.product_uom_qty
    #                     res.product_id.out_of_stock_message = str(res.product_id.product_tmpl_id.po_units) + ' ' + str(res.product_id.uom_po_id.name)+ " In Transit" + ' ' + str(res.product_id.product_tmpl_id.sold_units) + ' ' + str(res.product_id.uom_id.name) +  ' Sold'    
    #                     if res.product_id.product_tmpl_id.sold_units >= res.product_id.product_tmpl_id.po_units:
    #                         res.product_id.product_tmpl_id.allow_out_of_stock_order = False
    #             if res.product_id.website_id.khazana == False:
    #                 if res.product_id.intransit:
    #                     res.product_id.product_tmpl_id.sold_units += res.product_uom_qty
    #                     res.product_id.out_of_stock_message = str(res.product_id.product_tmpl_id.po_units) + ' ' + str(res.product_id.uom_po_id.name)+ " In Transit" + ' ' + str(res.product_id.product_tmpl_id.sold_units) + ' ' + str(res.product_id.uom_id.name) +  ' Sold'    
    #                     if res.product_id.product_tmpl_id.sold_units >= res.product_id.product_tmpl_id.po_units:
    #                         res.product_id.product_tmpl_id.allow_out_of_stock_order = False
    #                         # res.product_id.out_of_stock_message = ''
    #     return result



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    apply_discount = fields.Boolean('Apply Discount',default=True)
    
    # @api.model
    # def create(self, vals):
    #     res = super(SaleOrderLine, self).create(vals)
    #     if res.product_id.website_id.khazana == True:
    #         if res.product_id.intransit:
    #             print(res.product_id.sold_units, "res.product_id.sold_units------")
    #             res.product_id.sold_units += res.product_uom_qty
    #             print(res.product_id.sold_units, "res.product_id.sold_units---3333---")
    #             res.product_id.out_of_stock_message = str(res.product_id.po_units) + ' ' + str(res.product_id.uom_po_id.name)+ " In Transit" + ' ' + str(res.product_id.sold_units) + ' ' + str(res.product_id.uom_id.name) +  ' Sold'    
    #             if res.product_id.sold_units >= res.product_id.po_units:
    #                 res.product_id.product_tmpl_id.allow_out_of_stock_order = False
    #     return res
    
    
    
    # @api.model
    # def write(self, vals):
    #     result = super(SaleOrderLine, self).write(vals)
    #     for res in self:
    #         if 'product_uom_qty' in vals:
    #             if res.product_id.website_id.khazana == True:
    #                 if res.product_id.intransit:
    #                     print(res.product_id.sold_units, "res.product_id.sold_units------")
    #                     res.product_id.sold_units += res.product_uom_qty
    #                     print(res.product_id.sold_units, "res.product_id.sold_units---3333---")
    #                     res.product_id.out_of_stock_message = str(res.product_id.po_units) + ' ' + str(res.product_id.uom_po_id.name)+ " In Transit" + ' ' + str(res.product_id.sold_units) + ' ' + str(res.product_id.uom_id.name) +  ' Sold'    
    #                     if res.product_id.sold_units >= res.product_id.po_units:
    #                         res.product_id.product_tmpl_id.allow_out_of_stock_order = False
    #     return result
    
    def _timesheet_create_project(self):
        """ Generate project for the given so line, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        self.ensure_one()
        values = self._timesheet_create_project_prepare_values()
        if self.product_id.project_template_id:
            values['name'] = "%s - %s - %s" % (values['name'], self.product_id.project_template_id.name, self.order_id.partner_id.name)
            project = self.product_id.project_template_id.copy(values)
            project.tasks.write({
                'sale_line_id': self.id,
                'partner_id': self.order_id.partner_id.id,
                'email_from': self.order_id.partner_id.email,
            })
            # duplicating a project doesn't set the SO on sub-tasks
            project.tasks.filtered(lambda task: task.parent_id != False).write({
                'sale_line_id': self.id,
                'sale_order_id': self.order_id,
            })
        else:
            project = self.env['project.project'].create(values)

        # Avoid new tasks to go to 'Undefined Stage'
        if not project.type_ids:
            project.type_ids = self.env['project.task.type'].create({'name': _('New')})

        # link project as generated by current so line
        self.write({'project_id': project.id})
        return project

