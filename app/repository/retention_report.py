import uuid

from app.models import RetentionReportModel
from app.repository import ReportRepository


class RetentionRepository(ReportRepository):
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
        except Exception:
            raise Exception(
                "Hubo un error al consultar la informacion en la base de datos"
            )
