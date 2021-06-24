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
                }
            },
        ]

        sells = cls.collection.aggregate(pipeline=pipeline)
        return list(sells)
