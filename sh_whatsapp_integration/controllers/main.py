# -*- coding: utf-8 -*-
from odoo import  http, _
from odoo.exceptions import AccessError, MissingError,UserError
from odoo.http import request, content_disposition
import re

class DownloadReport(http.Controller):
    
    def _document_check_access(self, model_name, document_id, access_token=None):
        document = request.env[model_name].browse([document_id])
        document_sudo = document.sudo().exists()
        if not document_sudo:
            raise MissingError(_("This document does not exist."))
        if access_token and document_sudo.report_token and access_token == document_sudo.report_token:
            return document_sudo
        else:
            raise AccessError("Sorry, you are not allowed to access this document.")
    
    def _show_report(self, model, report_type, report_ref, download=False):
        if report_type not in ('html', 'pdf', 'text'):
            raise UserError(_("Invalid report type: %s") % report_type)

        report_sudo = request.env.ref(report_ref).sudo()

        if not isinstance(report_sudo, type(request.env['ir.actions.report'])):
            raise UserError(_("%s is not the reference of a report") % report_ref)

        method_name = 'render_qweb_%s' % (report_type)
        report = getattr(report_sudo, method_name)([model.id], data={'report_type': report_type})[0]
        reporthttpheaders = [
            ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
            ('Content-Length', len(report)),
        ]
        if report_type == 'pdf' and download:
            filename = "%s.pdf" % (re.sub('\W+', '-', model._get_report_base_filename()))
            reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
        return request.make_response(report, headers=reporthttpheaders)
    
    @http.route(['/download/so/<int:order_id>'], type='http', auth="public", website=True)
    def download_order(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return '<br/><br/><center><h1><b>Oops Invalid URL! Please check URL and try again!</b></h1></center>'
        report_type = 'pdf'
        download= True
        return self._show_report(model=order_sudo, report_type=report_type, report_ref='sale.action_report_saleorder', download=download)
    
    @http.route(['/download/inv/<int:order_id>'], type='http', auth="public", website=True)
    def download_invoice(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('account.move', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return '<br/><br/><center><h1><b>Oops Invalid URL! Please check URL and try again!</b></h1></center>'
        report_type = 'pdf'
        download= True
        return self._show_report(model=order_sudo, report_type=report_type, report_ref='account.account_invoices', download=download)


    @http.route(['/download/po/<int:order_id>'], type='http', auth="public", website=True)
    def download_purchase_order(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return '<br/><br/><center><h1><b>Oops Invalid URL! Please check URL and try again!</b></h1></center>'
        report_type = 'pdf'
        download= True
        return self._show_report(model=order_sudo, report_type=report_type, report_ref='purchase.action_report_purchase_order', download=download)
    
    @http.route(['/download/do/<int:order_id>'], type='http', auth="public", website=True)
    def download_do(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('stock.picking', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return '<br/><br/><center><h1><b>Oops Invalid URL! Please check URL and try again!</b></h1></center>'
        report_type = 'pdf'
        download= True
        return self._show_report(model=order_sudo, report_type=report_type, report_ref='stock.action_report_delivery', download=download)


    @http.route(['/download/ship/<int:order_id>'], type='http', auth="public", website=True)
    def download_shipment(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('stock.picking', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return '<br/><br/><center><h1><b>Oops Invalid URL! Please check URL and try again!</b></h1></center>'
        report_type = 'pdf'
        download= True
        return self._show_report(model=order_sudo, report_type=report_type, report_ref='stock.action_report_picking', download=download)
    
    @http.route(['/download/pay/<int:order_id>'], type='http', auth="public", website=True)
    def download_payment(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('account.payment', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return '<br/><br/><center><h1><b>Oops Invalid URL! Please check URL and try again!</b></h1></center>'
        report_type = 'pdf'
        download= True
        return self._show_report(model=order_sudo, report_type=report_type, report_ref='account.action_report_payment_receipt', download=download)
    
    