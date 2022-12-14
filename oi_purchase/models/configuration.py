from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class PurchaseOrderType(models.Model):
    _name = 'purchase.order.type'
    _description = 'Purchase Order Type'
    
    name = fields.Char("Name")  
    # approver_ids = fields.One2many('po.order.type.approver', 'purchase_order_type_id', string="Approvers")
    company_id = fields.Many2one('res.company', "Company", copy=False, required=True, index=True, default=lambda s: s.env.company)
    escalation_days = fields.Integer("Escalation Days")
    from_email = fields.Char("From Email")
    to_email = fields.Char("To Email")
    type = fields.Selection([('appliance', 'Appliance/CT'), ('imports', 'Imports'), ('domestic','Domestic'),('consumbles','Consumbles')], string="Type")

# class POOrderTypeApprover(models.Model):    
#     _name = 'po.order.type.approver'
#     _description = 'Order Type Approver'
#
#     from_amount = fields.Float("From Amount")
#     to_amount = fields.Float("To Amount")
#     purchase_order_type_id = fields.Many2one('purchase.order.type', string='Type', ondelete='cascade', required=True)
#     company_id = fields.Many2one('res.company', related='purchase_order_type_id.company_id')
#     user_id = fields.Many2one('res.users', string='User', ondelete='cascade', required=True,
#         check_company=True, domain="[('company_ids', 'in', company_id)]")
#     required = fields.Boolean(default=False)
#     existing_user_ids = fields.Many2many('res.users')
#
#


    