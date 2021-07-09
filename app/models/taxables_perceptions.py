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
            {"$unwind": "$nomina.Percepciones.Percepcion"},
            {
                "$group": {
                    "_id": {"empleado": "$Receptor.Nombre", "rfc": "$Receptor.Rfc"},
                    "total_grabado": {
                        "$sum": {"$toDouble": "$nomina.Percepciones.TotalGravado"}
                    },
                    "total_sueldo": {
                        "$sum": {"$toDouble": "$nomina.Percepciones.TotalSueldos"}
                    },
                    "total_exento": {
                        "$sum": {"$toDouble": "$nomina.Percepciones.TotalExento"}
                    },
                    "tipo_percepcion": {
                        "$push": "$nomina.Percepciones.Percepcion.TipoPercepcion"
                    },
                    "claves": {"$push": "$nomina.Percepciones.Percepcion.Clave"},
                    "conceptos": {"$push": "$nomina.Percepciones.Percepcion.Concepto"},
                    "importes_gravados": {
                        "$push": "$nomina.Percepciones.Percepcion.ImporteGravado"
                    },
                    "importes_exento": {
                        "$push": "$nomina.Percepciones.Percepcion.ImporteExento"
                    },
                }
            },
            {"$sort": {"_id.empleado": 1}},
        ]
        data = cls.collection.aggregate(pipeline=pipeline)
        return list(data)
