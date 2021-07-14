from app.repository import RetentionRepository
from app.services import ReportService


class RetentionReportService(ReportService):
    def __init__(self, repository: RetentionRepository):
        self.repository = repository

    def get_report(self, filters: dict):
        """
        Ejecuta el metodo para obtener los datos del reporte de
        retenciones.

        Params:
            filters (dict): Diccionario con los filtros de busqueda
                del reporte.

        Returns:
            Lista con los datos del reporte.
        """
        return self.repository.get_report(filters)
