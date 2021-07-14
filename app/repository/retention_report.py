import uuid

from app.models import RetentionReportModel
from app.repository import Repository
from app import app


class RetentionRepository(Repository):
    """
    Esta clase contiene el metodo para obtener el reporte.
    """

    def get_report(self, filters: dict) -> list:
        """
        Manda a llamar el metodo para generar la informacion del
        reporte de retenciones

        Params:
            filters (dict): Filtros para generar el reporte.

        Returns:
            Una lista con los datos del reporte de retenciones.
        """
        try:
            report = RetentionReportModel.get_retention_report(filters)
            if len(report) == 0:
                raise Exception("No se encontraron datos para el reporte")
            for item in report:
                item["uuid"] = uuid.uuid4().hex
            return report
        except Exception as e:
            app.logger.error(e)
            return None
