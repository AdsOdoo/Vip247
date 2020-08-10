# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models,api

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    order_information_in_message = fields.Boolean("Order Information in message?", default=True)
    order_product_detail_in_message = fields.Boolean("Order Product details in messsage?",default=True)
    signature = fields.Boolean("Signature?",default=True)
    display_in_message = fields.Boolean("Display in Chatter Message?",default=True)
    send_pdf_in_message = fields.Boolean("Send Report URL in message?",default=True)
   
    purchase_order_information_in_message = fields.Boolean("Order Information in message?", default=True)
    purchase_product_detail_in_message = fields.Boolean("Order Product details in messsage?",default=True)
    purchase_signature = fields.Boolean("Signature?",default=True)
    purchase_display_in_message = fields.Boolean("Display in Chatter Message?",default=True)
    po_send_pdf_in_message = fields.Boolean("Send Report URL in message?",default=True)
    
    invoice_order_information_in_message = fields.Boolean("Order Information in message?", default=True)
    invoice_product_detail_in_message = fields.Boolean("Order Product details in messsage?",default=True)
    invoice_signature = fields.Boolean("Signature?",default=True)
    invoice_display_in_message = fields.Boolean("Display in Chatter Message?",default=True)
    inv_send_pdf_in_message = fields.Boolean("Send Report URL in message?",default=True)
    
    inventory_information_in_message = fields.Boolean("Order Information in message?", default=True)
    inventory_signature = fields.Boolean("Signature?",default=True)
    inventory_display_in_message = fields.Boolean("Display in Chatter Message?",default=True)
    stock_send_pdf_in_message = fields.Boolean("Send Report URL in message?",default=True)
    
    crm_lead_signature = fields.Boolean("Signature?",default=True)
    crm_lead_display_in_message = fields.Boolean("Display in Chatter Message?",default=True)
    
    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    order_information_in_message = fields.Boolean(related="company_id.order_information_in_message", string="Order Information in message?",readonly=False)
    order_product_detail_in_message = fields.Boolean(related="company_id.order_product_detail_in_message", string="Order Product details in messsage?",readonly=False)
    signature = fields.Boolean(related="company_id.signature", string="Signature?",readonly=False)
    display_in_message = fields.Boolean(related="company_id.display_in_message",string="Display in Chatter Message?",readonly=False)
    send_pdf_in_message = fields.Boolean(related="company_id.send_pdf_in_message",string="Send Report URL in message?",readonly=False)
   
    purchase_order_information_in_message = fields.Boolean(related="company_id.purchase_order_information_in_message", string="Order Information in message?",readonly=False)
    purchase_product_detail_in_message = fields.Boolean(related="company_id.purchase_product_detail_in_message", string="Order Product details in messsage?",readonly=False)
    purchase_signature = fields.Boolean(related="company_id.purchase_signature", string="Signature?",readonly=False)
    purchase_display_in_message = fields.Boolean(related="company_id.purchase_display_in_message",string="Display in Chatter Message?",readonly=False)
    po_send_pdf_in_message = fields.Boolean(related="company_id.po_send_pdf_in_message",string="Send Report URL in message?",readonly=False)
   
    invoice_order_information_in_message = fields.Boolean(related="company_id.invoice_order_information_in_message", string="Order Information in message?",readonly=False)
    invoice_product_detail_in_message = fields.Boolean(related="company_id.invoice_product_detail_in_message", string="Order Product details in messsage?",readonly=False)
    invoice_signature = fields.Boolean(related="company_id.invoice_signature", string="Signature?",readonly=False)
    invoice_display_in_message = fields.Boolean(related="company_id.invoice_display_in_message",string="Display in Chatter Message?",readonly=False)
    inv_send_pdf_in_message = fields.Boolean(related="company_id.inv_send_pdf_in_message",string="Send Report URL in message?",readonly=False)
   
    inventory_information_in_message = fields.Boolean(related="company_id.inventory_information_in_message", string="Order Information in message?",readonly=False)
    inventory_signature = fields.Boolean(related="company_id.inventory_signature", string="Signature?",readonly=False)
    inventory_display_in_message = fields.Boolean(related="company_id.inventory_display_in_message",string="Display in Chatter Message?",readonly=False)
    stock_send_pdf_in_message = fields.Boolean(related="company_id.stock_send_pdf_in_message",string="Send Report URL in message?",readonly=False)
   
    crm_lead_display_in_message = fields.Boolean(related="company_id.crm_lead_display_in_message", string="Display in Chatter Message?",readonly=False)
    crm_lead_signature = fields.Boolean(related="company_id.crm_lead_signature", string="Signature?",readonly=False)
    
    
    
    