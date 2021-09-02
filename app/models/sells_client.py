from app.models import Model
from app import mongo, app


class Sells_By_Client(Model):

    collection_name = app.config["PRINCIPAL_COLLECTION"]
    collection = mongo.db[collection_name]

    @classmethod
    def get_sells_by_client(cls, filters: dict) -> list:
        pipeline = [
            {"$match": filters},
            {"$unwind": "$impuestos.TrasladoIVA"},
            {
                "$set": {
                    "total": {"$toDouble": "$datos.Total"},
                    "subtotal": {"$toDouble": "$datos.SubTotal"},
                    "iva": {"$toDouble": "$impuestos.TrasladoIVA"},
                }
            },
            {
                "$group": {
                    "_id": "$Receptor.Nombre",
                    "rfc": {"$first": "$Receptor.Rfc"},
                    "total": {"$sum": "$total"},
                    "subtotal": {"$sum": "$subtotal"},
                    "iva": {"$sum": "$iva"},
                    "metodo_pago": {"$push": "$datos.MetodoPago"},
                    "serie": {"$push": "$datos.Serie"},
                    "folio": {"$push": "$datos.Folio"},
                    "fechas": {"$push": "$datos.Fecha"},
                    "total_por_factura": {"$push": "$total"},
                    "subtotal_por_factura": {"$push": "$subtotal"},
                    "iva_por_factura": {"$push": "$iva"},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        sells = cls.collection.aggregate(pipeline=pipeline)
        return list(sells)

    @classmethod
    def sells_details_report(cls, filters):
        pipeline = [
            {"$match": filters},
            {
                "$set": {
                    "folio_fiscal": "$_id",
                    "receptor": "$Receptor.Nombre",
                    "receptor_rfc": "$Receptor.Rfc",
                    "fecha": "$datos.Fecha",
                    "metodo_pago": "$datos.MetodoPago",
                    "moneda": "$datos.Moneda",
                    "folio": "$datos.Folio",
                    "serie": "$datos.Serie",
                    "total": "$datos.Total",
                    "subtotal": "$datos.SubTotal",
                    "impuesto": "$impuestos.TrasladoIVA",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "datos": 0,
                    "Receptor": 0,
                    "impuestos": 0,
                    "conceptos": 0,
                }
            },
        ]
        data = cls.collection.aggregate(pipeline=pipeline)
        return list(data)

    @classmethod
    def get_total_sells(cls, filters: dict):
        pipeline = [
            {"$match": filters},
            {"$group": {"_id": "$datos.Rfc", "total": {"$sum": "$datos.Total"}}},
        ]
        total = cls.collection.aggregate(pipeline=pipeline)
        return list(total)[0]

    @classmethod
    def get_top_sells(cls, filters: dict):
        pipeline = [
            {"$match": filters},
            {
                "$group": {
                    "_id": {"rfc": "$Receptor.Rfc", "nombre": "$Receptor.Nombre"},
                    "total": {"$sum": {"$toDouble": "$datos.Total"}},
                }
            },
            {"$sort": {"total": 1}},
            {"$limit": 5},
        ]
        data = cls.collection.aggregate(pipeline)
        return list(data)
