from app.models import Model
from app import mongo, app


class Sells_By_Client(Model):

    collection_name = app.config["PRINCIPAL_COLLECTION"]
    collection = mongo.db[collection_name]

    @classmethod
    def get_sells_by_client(cls, filters: dict) -> list:
        pipeline = [
            {"$match": filters},
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
                    "total_por_factura": {"$push": {"$toDouble": "$datos.Total"}},
                    "subtotal_por_factura": {"$push": {"$toDouble": "$datos.SubTotal"}},
                    "iva_por_factura": {"$push": {"$toDouble": "$impuestos.TrasladoIVA"}},
                }
            },
        ]

        sells = cls.collection.aggregate(pipeline=pipeline)
        return list(sells)
