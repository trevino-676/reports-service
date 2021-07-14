from app.models import Model
from app import app, mongo


class RetentionReportModel(Model):
    """
    Esta clase contiene el metodo para obtener los datos del reporte
    de retenciones
    """

    collection_name = app.config["RETENTION_COLLECTION"]
    collection = mongo.db[collection_name]

    @classmethod
    def get_retention_report(cls, filters: dict) -> list:
        """
        Genera la informacion del reporte de retenciones.

        Params:
            filters (dict): Diccionario con los filtros para
                el reporte.

        Returns:
            Retorna una lista con todos los registros que se
            encontraron en la base de datos.
        """
        pipeline = [
            {"$match": filters},
            {"$unwind": "$conceptos"},
            {"$addFields": {"impuesto": "$conceptos.Impuestos"}},
            {"$unwind": "$impuesto"},
            {
                "$unionWith": {
                    "coll": "nomina",
                    "pipeline": [
                        {"$match": filters},
                        {"$unwind": "$conceptos"},
                        {"$addFields": {"impuesto": "$conceptos.Impuestos"}},
                        {"$unwind": "$impuesto"},
                    ],
                }
            },
            {
                "$group": {
                    "_id": {
                        "clave": "$impuesto.Impuesto",
                        "tasa_cuota": "$impuesto.TasaOCuota",
                    },
                    "importe": {"$sum": {"$toDouble": "$impuesto.Base"}},
                    "retencion": {"$sum": {"$toDouble": "$impuesto.Importe"}},
                    "tipo_factor": {"$first": "$impuesto.TipoFactor"},
                }
            },
        ]
        report_data = cls.collection.aggregate(pipeline=pipeline)
        return list(report_data)
