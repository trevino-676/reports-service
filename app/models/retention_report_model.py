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
        pass


