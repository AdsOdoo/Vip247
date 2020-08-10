# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class sh_send_whatsapp_message(models.TransientModel):
    _name = "sh.send.whatsapp.message.wizard"
    _description = "Send whatsapp message wizard"
    
    
    partner_ids = fields.Many2one("res.partner", string = "Recipients", required=True)
    message = fields.Text("Message", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", 
                                      relation="rel_sh_send_whatsapp_msg_ir_attachments",
                                      string = "Attachments")    
    sale_order_id = fields.Many2one('sale.order',string="Sale Order")
    purchase_order_id = fields.Many2one('purchase.order',string="Purchase Order")
    account_invoice_id = fields.Many2one('account.move',string="Account Invoice")
    stock_picking_id = fields.Many2one('stock.picking',string="Stock Picking")
    account_payment_id = fields.Many2one('account.payment',string="Account Payment")
    
    def action_send_whatsapp_message(self):
        if self:
            for rec in self:
                for partner in rec.partner_ids:
                    active_ids = self.env.context.get('active_ids')
                    active_id = int(active_ids[0])
                    sh_message=""
                    if rec.message:
                        sh_message = str(self.message).replace('*','').replace('_','').replace('%0A','<br/>').replace('%20',' ')
                    #For Sale Order Message Create in Chatter Box.
                    if rec.sale_order_id and rec.sale_order_id.company_id.display_in_message:
                        self.env['mail.message'].create({
                                                        'partner_ids':[(6,0,partner.ids)],
                                                        'model':'sale.order',
                                                        'res_id':active_id,
                                                        'author_id':self.env.user.partner_id.id,
                                                        'body':sh_message or False,
                                                        'message_type':'comment',
                                                    })
                    
                    if rec.purchase_order_id and rec.purchase_order_id.company_id.purchase_display_in_message:
                        self.env['mail.message'].create({
                                                        'partner_ids':[(6,0,partner.ids)],
                                                        'model':'purchase.order',
                                                        'res_id':active_id,
                                                        'author_id':self.env.user.partner_id.id,
                                                        'body':sh_message or False,
                                                        'message_type':'comment',
                                                    })
                        
                    if rec.account_invoice_id and rec.account_invoice_id.company_id.invoice_display_in_message and rec.account_invoice_id.type == 'in_invoice':    
                        self.env['mail.message'].create({
                                                        'partner_ids':[(6,0,partner.ids)],
                                                        'model':'account.move',
                                                        'res_id':active_id,
                                                        'author_id':self.env.user.partner_id.id,
                                                        'body':sh_message or False,
                                                        'message_type':'comment',
                                                    })
                     
                    if rec.account_invoice_id and rec.account_invoice_id.company_id.invoice_display_in_message and rec.account_invoice_id.type == 'out_invoice':    
                        self.env['mail.message'].create({
                                                        'partner_ids':[(6,0,partner.ids)],
                                                        'model':'account.move',
                                                        'res_id':active_id,
                                                        'author_id':self.env.user.partner_id.id,
                                                        'body':sh_message or False,
                                                        'message_type':'comment',
                                                    })
                    
                    if rec.stock_picking_id and rec.stock_picking_id.company_id.inventory_display_in_message and rec.stock_picking_id.picking_type_id.code == "outgoing":  
                        self.env['mail.message'].create({
                                                        'partner_ids':[(6,0,partner.ids)],
                                                        'model':'stock.picking',
                                                        'res_id':active_id,
                                                        'author_id':self.env.user.partner_id.id,
                                                        'body':sh_message or False,
                                                        'message_type':'comment',
                                                    })
                    
                    if rec.stock_picking_id and rec.stock_picking_id.company_id.inventory_display_in_message and rec.stock_picking_id.picking_type_id.code == "incoming":  
                        self.env['mail.message'].create({
                                                        'partner_ids':[(6,0,partner.ids)],
                                                        'model':'stock.picking',
                                                        'res_id':active_id,
                                                        'author_id':self.env.user.partner_id.id,
                                                        'body':sh_message or False,
                                                        'message_type':'comment',
                                                    })
                    
                    if self.account_payment_id and self.account_payment_id.company_id.invoice_display_in_message:  
                        self.env['mail.message'].create({
                                                        'partner_ids':[(6,0,partner.ids)],
                                                        'model':'account.payment',
                                                        'res_id':active_id,
                                                        'author_id':self.env.user.partner_id.id,
                                                        'body':sh_message or False,
                                                        'message_type':'comment',
                                                    })
                        
                    if partner.mobile:
                        return {
                            'type': 'ir.actions.act_url',
                            'url': "https://web.whatsapp.com/send?l=&phone="+partner.mobile+"&text=" + rec.message,
                            'target': 'new',
                            'res_id': rec.id,
                        }
                    
        