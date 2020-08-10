# -*- coding: utf-8 -*-
import json
from odoo.tools.translate import _
from odoo import http
from odoo.http import request
#import logging
#_logger = logging.getLogger(__name__)

class RestAPI(http.Controller):

    @http.route(['/api/record/create'
                 ], type='json', auth="none", csrf=False, methods=['POST'])

    def create_data(self, model=None, **post):
        """
            create record , it is medetory to pass model name
            and values for record creation pass as create_vals of JOSN/Dictionary format.
            eg.
            QueryString:
                localhost:8069/api/product.product/create?token=24e635ff9cc74429bed3d420243f5aa6&create_vals={'name':'Apple'}
            Return:
                If record is successfully created then it will return record id eg. {'id':101}
        """
        data = request.jsonrequest
        #_logger.info('data: %s', data)

        if data.get('db'):
            request.session.db = data.get('db')
        try:
            Model = request.env['notas.evolucion']
        except Exception as e:
            return json.dumps({'error': _('Model Not Found %s' % e), 'status': 0})
        else:
            if data:
                try:
                    record = Model.sudo().record_from_api(data)
                except Exception as e:
                    return json.dumps({'error': _(' %s' % e), 'status': 0, 'message': 'In-appropriate data contact administrator'})
                if record:
                    res = {'id': record.id, 'status': 1, 'message': 'success'}
                    return json.dumps(res)
            else:
                return json.dumps({'error': _('create_vals not found in query string'), 'status': 0, 'message': 'In-appropriate data contact administrator'})
