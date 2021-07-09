from app.models import Model
from app import app, mongo


class SellsByServices(Model):
    collection_name = app.config["PRINCIPAL_COLLECTION"]
    collection = mongo.db[collection_name]

    @classmethod
    def get_sells_by_services(cls, filters: dict) -> list:
        pipeline = [
            {"$match": filters},
            {"$unwind": "$conceptos"},
            {
                "$match": {
                    "conceptos.Detalles.ClaveUnidad": {"$in": ["E48", "ACT", "AS", "E54"]}
                }
            },
            {
                "$group": {
                    "_id": {
                        "servicio": "$conceptos.Detalles.Descripcion",
                        "codigo": "$conceptos.Detalles.ClaveProdServ",
                        "clave": "$conceptos.Detalles.ClaveUnidad",
                    },
                    "cantidad": {"$sum": {"$toDouble": "$conceptos.Detalles.Cantidad"}},
                    "precio_unitario": {
                        "$first": {"$toDouble": "$conceptos.Detalles.ValorUnitario"}
                    },
                    "importe": {"$sum": {"$toDouble": "$conceptos.Detalles.Importe"}},
                }
            },
            {"$sort": {"_id.servicio": 1}},
        ]
        sells = cls.collection.aggregate(pipeline=pipeline)
        return list(sells)
