# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime
from datetime import datetime
#import logging
#_logger = logging.getLogger(__name__)

class ForacareNotasDeEvolucion(models.Model):
    _inherit = 'notas.evolucion'

    @api.model
    def record_from_api(self, vals):

        patient_id = vals.get('UploadData').get('PatientID')
        measure_id = vals.get('UploadData').get('MeasureData')
        
        mtype = [ type['MType'] for type in measure_id ]
        mslot = [ slot['MSlot'] for slot in measure_id ]
        mvalue1 = [ value1['MValue1'] for value1 in measure_id ]
        mvalue2 = [ value1['MValue2'] for value1 in measure_id ]
        mvalue3 = [ value1['MValue3'] for value1 in measure_id ]

        date_time = [ value1['MDateTime'] for value1 in measure_id ][0]
        date = str(date_time)[:10]
        time = str(date_time)[11:]
        
        pacientes = self.env['pacientes'].search([('name', '=', patient_id)])
        
        if pacientes:
            values = {
                'paciente': pacientes.id,
                'fecha': datetime.strptime(date, "%Y/%m/%d").strftime('%Y-%m-%d'),
                'hora': time,
                }

            if mtype[0] == '1':
                values.update({'glucemia': mvalue1[0]})
            elif mtype[0] == '2':
                values.update({'presion': mvalue1[0]})
                values.update({'sistole': mvalue1[0]})
                values.update({'diastole': mvalue2[0]})
                values.update({'pulso': mvalue3[0]})
            elif mtype[0] == '7':
                values.update({'sp02': mvalue1[0]})
            elif mtype[0] == '8':
                values.update({'peso': mvalue1[0]})
            elif mtype[0] == '11':
                values.update({'cetona': mvalue1[0]})
            elif mtype[0] == '12':
                values.update({'colesterol': mvalue1[0]})
            elif mtype[0] == '13':
                values.update({'acido_urico': mvalue1[0]})
            elif mtype[0] == '14':
                values.update({'hbac': mvalue1[0]})
            elif mtype[0] == '15':
                values.update({'hb': mvalue1[0]})
            elif mtype[0] == '16':
                values.update({'hct': mvalue1[0]})
            elif mtype[0] == '17':
                values.update({'lactato': mvalue1[0]})
            elif mtype[0] == '60':
                values.update({'temp_oido': mvalue1[0]})
            elif mtype[0] == '61':
                values.update({'temp_frente': mvalue1[0]})
            elif mtype[0] == '62':
                values.update({'temp_axila': mvalue1[0]})
            elif mtype[0] == '63':
                values.update({'temp_recto': mvalue1[0]})
            nota_evolucion = self.env['notas.evolucion'].create(values)
            return nota_evolucion

    