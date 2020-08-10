# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api,_
from odoo.exceptions import UserError
import uuid

class AccountInvoice(models.Model):
    _inherit="account.move"
    
    text_message = fields.Text("Message",compute="get_message_detail_so")
    
    report_token = fields.Char("Access Token")
    
    def _get_token(self):
        """ Get the current record access token """
        if self.report_token:
            return self.report_token
        else:
            report_token= str(uuid.uuid4())
            self.write({'report_token':report_token})
            return report_token
    
    def get_download_report_url(self):
        url =''
        if self.id:
            self.ensure_one()
            url = '/download/inv/' + '%s?access_token=%s' % (
                self.id,
                self._get_token()
            )
        return url
    
    @api.depends('partner_id','currency_id','company_id')
    def get_message_detail_so(self):
        if self and self.type == 'out_invoice':
            for inv in self:
                txt_message = ""
                if inv.company_id.invoice_order_information_in_message and inv.partner_id and inv.currency_id and inv.company_id:
                    txt_message +=  "Dear " + str(inv.partner_id.name)+","+"%0A%0A"
                    
                    if inv.name and inv.state != "draft":
                        txt_message +=  "Here is the your invoice "+'*'+str(inv.name)+'*'+""
                    else:    
                        txt_message +=  "Here is the your invoice "+""
                    txt_message += " amounting in "+'*'+str(inv.amount_total)+'*'+""+str(inv.currency_id.symbol)+" from "+inv.company_id.name+"."
                    if inv.state =="paid":
                        txt_message += "This invoice is already paid."+"%0A%0A"
                    else:
                        txt_message += "Please remit payment at your earliest convenience."+"%0A%0A"
                if inv.company_id.invoice_product_detail_in_message:
                    txt_message += "Following is your order details."+"%0A"
                    if inv.invoice_line_ids:
                        for invoices_line in inv.invoice_line_ids:
                            if invoices_line.product_id and invoices_line.quantity and invoices_line.price_unit:
                                txt_message +=  "%0A"+"*"+invoices_line.product_id.name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Price:* "+str(invoices_line.price_unit)+""+str(invoices_line.move_id.currency_id.symbol)+"%0A"
                            else:
                                txt_message +=  "%0A"+"*"+invoices_line.name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Price:* "+str(invoices_line.price_unit)+""+str(invoices_line.move_id.currency_id.symbol)+"%0A"
                            if invoices_line.discount > 0.00:
                                txt_message +=  "*Discount:* "+str(invoices_line.discount)+"%25"+"%0A"
                            txt_message += "________________________"+"%0A"
                    txt_message += "*"+"Total Amount:"+"*"+"%20"+str(inv.amount_total)+""+str(inv.currency_id.symbol)
                
                if inv.company_id.inv_send_pdf_in_message:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                    inv_url = "%0A%0A Click here to download Report : %0A"+base_url+inv.get_download_report_url()
                    txt_message+= inv_url
                if inv.company_id.invoice_signature and inv.env.user.sign:
                    txt_message += "%0A%0A%0A"+str(inv.env.user.sign)
            inv.text_message = txt_message
            
        elif self and self.type == 'in_invoice':
            for inv in self:
                txt_message = ""
                if inv.company_id.invoice_order_information_in_message and inv.partner_id and inv.currency_id and inv.company_id:
                    txt_message +=  "Dear " + str(inv.partner_id.name)+","+"%0A%0A"
                    if inv.name and inv.state != "draft":
                        txt_message +=  "Here is the your invoice "+'*'+str(inv.name)+'*'+""
                    else:    
                        txt_message +=  "Here is the your invoice "+""
                    txt_message += " amounting in "+'*'+str(inv.amount_total)+'*'+""+str(inv.currency_id.symbol)+" from "+inv.company_id.name+"."
                    if inv.state =="paid":
                        txt_message += "This invoice is already paid."+"%0A%0A"
                    else:
                        txt_message += "Please remit payment at your earliest convenience."+"%0A%0A"
                if inv.company_id.invoice_product_detail_in_message:
                    txt_message += "Following is your order details."+"%0A"
                    if inv.invoice_line_ids:
                        for invoices_line in inv.invoice_line_ids:
                            if invoices_line.product_id and invoices_line.quantity and invoices_line.price_unit:
                                txt_message +=  "%0A"+"*"+invoices_line.product_id.name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Price:* "+str(invoices_line.price_unit)+""+str(invoices_line.move_id.currency_id.symbol)+"%0A"
                            else:
                                txt_message +=  "%0A"+"*"+invoices_line.name+"*"+"%0A"+"*Qty:* "+str(invoices_line.quantity)+"%0A"+"*Price:* "+str(invoices_line.price_unit)+""+str(invoices_line.move_id.currency_id.symbol)+"%0A"
                            
                            if invoices_line.discount > 0.00:
                                txt_message +=  "*Discount:* "+str(invoices_line.discount)+"%25"+"%0A"
                            txt_message += "________________________"+"%0A"
                    txt_message += "*"+"Total Amount:"+"*"+"%20"+str(inv.amount_total)+""+str(inv.currency_id.symbol)
                if inv.company_id.inv_send_pdf_in_message:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')   
                    inv_url = "%0A%0A Click here to download Report : %0A"+base_url+inv.get_download_report_url()
                    txt_message+= inv_url
                if inv.company_id.invoice_signature and inv.env.user.sign:
                    txt_message += "%0A%0A%0A"+str(inv.env.user.sign)  
            inv.text_message = txt_message
        else:
            self.text_message = ''
    
    def send_by_whatsapp_direct_to_ci(self):
        if self:
            for rec in self:
                if rec.company_id.invoice_display_in_message:
                    message=''
                    if rec.text_message:
                        message = str(self.text_message).replace('*','').replace('_','').replace('%0A','<br/>').replace('%20',' ')
                    self.env['mail.message'].create({
                                                    'partner_ids':[(6,0,rec.partner_id.ids)],
                                                    'model':'account.move',
                                                    'res_id':rec.id,
                                                    'author_id':self.env.user.partner_id.id,
                                                    'body':message or False,
                                                    'message_type':'comment',
                                                })
                
                if rec.partner_id.mobile and rec.text_message:
                    return {
                            'type': 'ir.actions.act_url',
                            'url': "https://web.whatsapp.com/send?l=&phone="+rec.partner_id.mobile+"&text=" + rec.text_message,
                            'target': 'new',
                            'res_id': rec.id,
                        }
                else:
                    raise UserError("Partner Mobile Number Not Exist")
                
        
