from app.repository import RetentionRepository
from app.services import ReportService
from app import app
from pymongo import MongoClient
import locale 
from datetime import datetime
import json

locale.setlocale(locale.LC_ALL, 'en_US')
locale.setlocale(locale.LC_TIME, "es_ES")

class RetentionReportService(ReportService):
    def __init__(self, repository: RetentionRepository):
        self.repository = repository

    def get_report(self, filters: dict):
        """
        Ejecuta el metodo para obtener los datos del reporte de
        retenciones.

        Params:
            filters (dict): Diccionario con los filtros de busqueda
                del reporte.

        Returns:
            Lista con los datos del reporte.
        """
        try:
            return self.repository.get_report(filters)
        except Exception as e:
            app.logger.error(e)
            return None
    def get_report_nomina(self, filters: dict):
        empresa      =  filters[0]['empresa']
        empleado     =  filters[0]['empleado']
        dataFrom     =  filters[0]['dataFrom']
        dataTo       =  filters[0]['dataTo']
            
        if len(dataFrom) < 2:  
            dataFrom = "2021-07-01" 
        if len(dataTo) < 2:  
            dataTo   = "2021-08-23" 

        client     = MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017")
        db         = client["cfdi"]  
        collection = db["nomina"] 
        
        filer_date = {"$gte":  dataFrom, "$lte":  dataTo}

        if len(empleado) > 2 : 
            res = collection.aggregate([ { "$match": { "datos.Rfc": empresa, "Receptor.Rfc" : empleado, 
                                                   "nomina.FechaPago" : filer_date } }, 
                                     { "$group": { "_id": "$Receptor.Rfc",  } }, 
                                     {"$sort": {"Receptor.Rfc": -1}}, 
                                     {"$limit": 1}  
                                    ])     
        else: 
            res = collection.aggregate([ { "$match": { "datos.Rfc": empresa,
                                                   "nomina.FechaPago" : filer_date } }, 
                                     { "$group": { "_id": "$Receptor.Rfc",  } }, 
                                     {"$sort": {"Receptor.Rfc": -1}}, 
                                     {"$limit": 4}  
                                    ])     

        empleados = []  
        movimientos = [] 
        index = 0 
        row_detalles = []
        index_otr = 0 
        index_per = 0 
        index_ded = 0 
        otrospagos_arr = []
        total_deducciones = 0
        total_percepcciones = 0 
        total_otrospagos = 0 
        gen_nombre = "" 
        #list all the rfc's employees 
        for doc in res:
            index = index+1 
            row_detalles = []
            total_deducciones   = 0 
            total_percepcciones = 0
            total_otrospagos    = 0
            index_per = 0
            index_ded = 0

             #get all | percepciones 
            percepccion_arr = []  
            percepciones = collection.find({"Receptor.Rfc": doc["_id"], "nomina.FechaPago" : filer_date, "nomina.Percepciones.Percepcion": 
                            { '$exists': 'true', '$ne': 'null' }},  
                            { "Receptor.Nombre": 1, "Receptor.Rfc": 1, "nomina.TotalPercepciones": 1,
                              "nomina.TotalDeducciones": 1, "nomina.TotalOtrosPagos" :1, "nomina.FechaPago" :1, "_id" : 1, "nomina.Percepciones.Percepcion" : 1})  
            for per in percepciones:  
                index_per = 0
                for perc in per["nomina"]["Percepciones"]["Percepcion"]: 
                            percepccion_arr += [ {  
                                                    "id" : (index), 
                                                    "Clave" : per["nomina"]["Percepciones"]["Percepcion"][index_per]["Clave"], 
                                                    "TipoDeduccion" : per["nomina"]["Percepciones"]["Percepcion"][index_per]["TipoPercepcion"], 
                                                    "Concepto" : per["nomina"]["Percepciones"]["Percepcion"][index_per]["Concepto"], 
                                                    "Importe" : locale.currency( float(per["nomina"]["Percepciones"]["Percepcion"][index_per]["ImporteGravado"]), grouping=True), 
                                                    "fecha" : datetime.strptime( per["nomina"]["FechaPago"], '%Y-%m-%d').date().strftime("%d/%m/%Y") 
                                                    }]     
                            total_percepcciones += float(per["nomina"]["Percepciones"]["Percepcion"][index_per]["ImporteGravado"])
                            index_per = index_per + 1  

            #get all | deducciones 
            deducciones_arr = [] 
            deducciones = collection.find({"Receptor.Rfc": doc["_id"], "nomina.FechaPago" : filer_date, "nomina.Deducciones.Deduccion": 
                            { '$exists': 'true', '$ne': 'null' }},  
                            { "Receptor.Nombre": 1, "Receptor.Rfc": 1, "nomina.TotalDeducciones": 1,
                              "nomina.TotalDeducciones": 1, "nomina.TotalOtrosPagos" :1, "nomina.FechaPago" :1, "_id" : 1, "nomina.Deducciones.Deduccion" : 1})   
            for ded in deducciones: 
                        index_ded = 0
                        gen_nombre = ded["Receptor"]["Nombre"]
                        for dedu in ded["nomina"]["Deducciones"]["Deduccion"]: 
                            deducciones_arr += [ {  
                                                    "id" : index_ded, 
                                                    "Clave" : ded["nomina"]["Deducciones"]["Deduccion"][index_ded]["Clave"], 
                                                    "TipoDePercepcion" : ded["nomina"]["Deducciones"]["Deduccion"][index_ded]["TipoDeduccion"], 
                                                    "Concepto" : ded["nomina"]["Deducciones"]["Deduccion"][index_ded]["Concepto"], 
                                                    "Importe" : locale.currency( float( ded["nomina"]["Deducciones"]["Deduccion"][index_ded]["Importe"] ), grouping=True), 
                                                    "fecha" : datetime.strptime( ded["nomina"]["FechaPago"], '%Y-%m-%d').date().strftime("%d/%m/%Y")
                                                    }]
                            total_deducciones += float(ded["nomina"]["Deducciones"]["Deduccion"][index_ded]["Importe"])
                            index_ded = index_ded + 1  
            
            #get all | otrosPagos 
            otrospagos_arr = []  
            otrospagos = collection.find({"Receptor.Rfc": doc["_id"], "nomina.FechaPago" : filer_date, "nomina.OtrosPagos": 
                            { '$exists': 'true', '$ne': 'null' }},  
                            { "Receptor.Nombre": 1, "Receptor.Rfc": 1, "nomina.TotalPercepciones": 1,
                              "nomina.TotalDeducciones": 1, "nomina.TotalOtrosPagos" :1, "nomina.FechaPago" :1, "_id" : 1, "nomina.OtrosPagos" : 1})   
            
            for otr in otrospagos: 
                index_otr = 0  
                #otrospagos_arr += [ {"xxxxxx": otr} ]
                for o in otr["nomina"]["OtrosPagos"]:   
                    otrospagos_arr +=  [{  
                                            "id" : (index_otr+1), 
                                            "TipoDeduccion" : otr["nomina"]["OtrosPagos"][index_otr]["TipoOtroPago"], 
                                            "Clave"         : otr["nomina"]["OtrosPagos"][index_otr]["Clave"], 
                                            "Concepto"      : otr["nomina"]["OtrosPagos"][index_otr]["Concepto"],
                                            "Importe"       : locale.currency( float( otr["nomina"]["OtrosPagos"][index_otr]["Importe"] ), grouping=True),
                                            "fecha"         : datetime.strptime( otr["nomina"]["FechaPago"], '%Y-%m-%d').date().strftime("%d/%m/%Y") 
                                        }] 
                    total_otrospagos += float( otr["nomina"]["OtrosPagos"][index_otr]["Importe"] )
                index_otr = index_otr + 1                      
       
            empleados.append({"id": index, "empleado" : gen_nombre,     
                              "rfc":  locale.currency( float( total_deducciones ), grouping=True) , "price": locale.currency( float( total_percepcciones ), grouping=True) , 
                              "otrospagos":  locale.currency( float( total_otrospagos ), grouping=True) })    
            row_detalles.append(  list( deducciones_arr ) )  
            row_detalles.append(  list( percepccion_arr ) ) 
            row_detalles.append(  list( otrospagos_arr  ) )
 
            movimientos.append(row_detalles) 
            return ({'elements': empleados, 'percepciones': movimientos})
         
