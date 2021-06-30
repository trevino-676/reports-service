from app.models import Model
from app import mongo, app


class SellsByItems(Model):
    collection_name = app.config["PRINCIPAL_COLLECTION"]
    collection = mongo.db[collection_name]

    @classmethod
    def get_sells_by_items(cls, filters: dict) -> list:
        pipeline = [
            {"$match": filters},
            {"$unwind": "$conceptos"},
            {
                "$group": {
                    "_id": {
                        "articulo": "$conceptos.Detalles.Descripcion",
                        "codigo": "$conceptos.Detalles.ClaveProdServ",
                    },
                    "cantidad": {"$sum": {"$toDouble": "$conceptos.Detalles.Cantidad"}},
                    "precio_unitario": {
                        "$first": {"$toDouble": "$conceptos.Detalles.ValorUnitario"}
                    },
                    "importe": {"$sum": {"$toDouble": "$conceptos.Detalles.Importe"}},
                }
            },
            {"$match": {"_id.codigo": {"$nin": ["01010101"]}}},
        ]
        sells = cls.collection.aggregate(pipeline=pipeline)
        return list(sells)
