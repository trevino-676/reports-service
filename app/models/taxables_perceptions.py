from app.models import Model
from app import app, mongo


class TaxablesPerceptions(Model):
    """
    Modelo para el reporte de percepciones gravables.
    """

    collection_name = app.config["NOMINAS_COLLECTION"]
    collection = mongo.db[collection_name]

    @classmethod
    def get_taxables_perceptions(cls, filters: dict) -> list:
        pipeline = [
            {"$match": filters},
            {"$addFields": {"percepciones": "$nomina.Percepciones.Percepcion"}},
            {"$unwind": "$percepciones"},
            {
                "$group": {
                    "_id": {"empleado": "$Receptor.Nombre", "rfc": "$Receptor.Rfc"},
                    "total_grabado": {
                        "$sum": {"$toDouble": "$percepciones.ImporteGravado"}
                    },
                    "total_exento": {
                        "$sum": {"$toDouble": "$percepciones.ImporteExento"}
                    },
                    "tipo_percepcion": {"$push": "$percepciones.TipoPercepcion"},
                    "claves": {"$push": "$percepciones.Clave"},
                    "conceptos": {"$push": "$percepciones.Concepto"},
                    "importes_gravados": {"$push": "$percepciones.ImporteGravado"},
                    "importes_exento": {"$push": "$percepciones.ImporteExento"},
                    "fecha_pago": {"$push": "$nomina.FechaPago"},
                }
            },
            {
                "$addFields": {
                    "total_sueldo": {"$sum": ["$total_grabado", "$total_exento"]}
                }
            },
            {"$sort": {"_id.empleado": 1}},
        ]
        data = cls.collection.aggregate(pipeline=pipeline)
        return list(data)
