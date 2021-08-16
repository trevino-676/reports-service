from app import app, mongo


class DetailedReport:

    collection_name = app.config["PRINCIPAL_COLLECTION"]
    collection = mongo.db[collection_name]

    @classmethod
    def provider_report(cls, filters: dict):
        pipeline = [
            {"$match": filters},
            {
                "$set": {
                    "folio_fiscal": "$_id",
                    "receptor": "$datos.Nombre",
                    "receptor_rfc": "$datos.Rfc",
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
