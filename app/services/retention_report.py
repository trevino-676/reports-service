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
    def getComprasDelMes(self, filters: dict):
        try: 
            client = MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017")
            db2         = client["cfdi"];
            principal   = db2["principal"]
  
            date_from = "2021-08-01"
            date_to = "2021-08-28"
      
            filter_date = {"$gte":  date_from, "$lte":  date_to}
            rfc_receptor = "PGT190401156" 
            #{"$match": { "Receptor.Rfc": rfc_receptor, "datos.Fecha": filter_date }}, 
            col_principal = principal.aggregate([ {"$match": { "Receptor.Rfc": rfc_receptor, "datos.Fecha": filter_date }}, 
                                                  {"$group": {"_id": "..", "i": {"$sum": "$datos.Total"}}}])  

            col_principal = principal.aggregate([ {"$match": { "Receptor.Rfc": rfc_receptor, "datos.Fecha": filter_date }} ])

            total = 0 
            for compra in col_principal: 
                total += float(compra['datos']["Total"])

            col_principal = list(col_principal) 
                 
            return json.dumps({"elements": total })
        except Exception as e:
            app.logger.error(e)
            return None
    def getTopCompras(self, filters: dict):
        try: 
            client = MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017")
            db2         = client["cfdi"];
            principal   = db2["principal"]

            date_from = "2021-07-01"
            date_to = "2021-08-31"
      
            filter_date = {"$gte":  date_from, "$lte":  date_to}
            rfc_receptor = filters["receptor"] 
            #{"$match": { "Receptor.Rfc": rfc_receptor, "datos.Fecha": filter_date }}, 
            col_principal = principal.aggregate([ {"$match": { "Receptor.Rfc": rfc_receptor, "datos.Fecha": filter_date }}, 
                                                  {"$group": {"_id": "$datos.Nombre", "i": {"$sum": "$datos.Total"}}},
                                                  {"$sort": {"i": -1}}, {"$limit": 4}])  
            col_principal = list(col_principal) 
        
            empresas_list = [ ['Proveedores', 'Compras'] ]
 
            for empresa in col_principal: 
                empresas_list.append( [ empresa["_id"], empresa["i"] ]) 

            return json.dumps({"elements": empresas_list })
        except Exception as e:
            app.logger.error(e)
            return None
    def getEfos(self, filters: dict):
        try:
            client = MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017")
            db          = client["robin_hood"];
            db2         = client["cfdi"];
            collection  = db["suppliers"]
            principal   = db2["principal"] 
            
            efos = collection.find({"Efo": {"$exists": "true"}}, {"_id": 1, "Nombre": 1}) 
            
            total = 0 
            list_efos = []

            for efo in efos: 
                cantidad = 0 
                total = 0 
                col_principal = principal.find({"datos.Rfc": efo["_id"], "Receptor.Rfc": "PGT190401156"}, {"datos.Total": 1, "datos.Nombre": 1})
                nombre = ""
                for factura in col_principal:   
                    total += float(factura["datos"]["Total"])  
                    nombre = factura["datos"]["Nombre"]
                    cantidad+=1 
                list_efos.append( { "Nombre" : locale.currency( float(total), grouping=True), 
                                    "_id": efo["_id"], 
                                    "Empresa": nombre, 
                                    "cantidad": cantidad}) 
                 
            col_principal = list(col_principal)      
            return {"elements": list(list_efos) } 
        except Exception as e:
            app.logger.error(e)
            return None
    def comprasPorProveedor(self, filters: dict):
         
        client     = MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017")
        db         = client["cfdi"]  

        rfc_receptor =  filters[0]['receptor']  
        rfc_emisor   =  filters[0]['emisor']   
        dataFrom     =  filters[0]['dataFrom']   
        dataTo       =  filters[0]['dataTo']

        collection   = db["principal"] 
        rfc_receptor = "PGT190401156"; 
          
        if dataFrom is None:  
            dataFrom = "2021-03-01"
        if dataTo is None: 
            dataTo = "2021-05-02"

        filter_date = {"$gte":  dataFrom, "$lte":  dataTo}
        
        if rfc_emisor is not None: 
            res = collection.aggregate([ { "$match": { "Receptor.Rfc": rfc_receptor, "datos.Fecha": filter_date, 
                                                       "datos.Rfc": rfc_emisor }}, 
                                         { "$group": { "_id": "$datos.Rfc",  } }, 
                                         {"$limit": 10}  
                                        ]) 
        else: 
            res = collection.aggregate([ { "$match": { "Receptor.Rfc": rfc_receptor, "datos.Fecha": filter_date }}, 
                                         { "$group": { "_id": "$datos.Rfc",  } } 
                                        ]) 

        emisores_coll   = [] 
        receptores_coll = [] 
        row_facturas    = []
        cant = 0 
        for col in res: 
            row_facturas    = []
            cant = cant + 1 
            total_fac       = 0
            compras = collection.aggregate([ { "$match": { "Receptor.Rfc": rfc_receptor, "datos.Rfc": col["_id"], 
                                                "datos.Fecha": filter_date } } ]) 
            compras2 = collection.aggregate([ { "$match": { "Receptor.Rfc": rfc_receptor, "datos.Rfc": col["_id"], 
                                                "datos.Fecha": filter_date } }, {"$limit": 1} ])
            for com in compras: 
                row_facturas.append( {"id": cant, "rfc": col["_id"], "Nombre": com["datos"]["Nombre"],
                                      "MetodoPago": com["datos"]["MetodoPago"], 
                                      "Fecha": datetime.fromisoformat(com["datos"]["Fecha"]).strftime("%d/%m/%Y"), "Total": locale.currency( float(com["datos"]["Total"]), grouping=True) , "SubTotal": locale.currency(float(com["datos"]["SubTotal"]), grouping=True) })  
                total_fac = total_fac + float(com["datos"]["Total"])
            for comp in compras2: 
                receptores_coll.append( {"id" : cant, "rfc": comp["datos"]["Rfc"], "Nombre": comp["datos"]["Nombre"], "Total": locale.currency( float(total_fac), grouping=True), "MonedaDR" : "...." } ) 
            emisores_coll.append( list(row_facturas))

        #receptores_coll = list(receptores_coll)
        return ({'elements': receptores_coll , 'emisores' : [emisores_coll] })

    def get_report_nomina(self, filters: dict):
        empresa      =  filters[0]['empresa']
        empleado     =  filters[0]['empleado']
        dataFrom     =  filters[0]['dataFrom']
        dataTo       =  filters[0]['dataTo']
            
        if dataFrom is None:   
            dataFrom = "2021-01-01" 
        if dataTo  is None:  
            dataTo   = "2021-01-23" 

        client     = MongoClient("mongodb://root:drumb0t2o21@3.141.244.21:27017")
        db         = client["cfdi"]  
        collection = db["nomina"] 
        
        filer_date = {"$gte":  dataFrom, "$lte":  dataTo}
  
        if empleado is not None: 
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
                                     {"$limit": 8}  
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
                              "rfc":  locale.currency( float( total_deducciones ), grouping=True) , 
                              "price": locale.currency( float( total_percepcciones ), grouping=True) , 
                              "otrospagos":  locale.currency( float( total_otrospagos ), grouping=True) }) 
  
            row_detalles.append(  list( deducciones_arr ) )  
            row_detalles.append(  list( percepccion_arr ) ) 
            row_detalles.append(  list( otrospagos_arr  ) )
  
            movimientos.append(row_detalles) 
        return ({'elements': empleados, 'percepciones': movimientos})
         
