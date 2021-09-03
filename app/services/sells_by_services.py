from app.repository import SellsByServicesRepository
from app.services import ReportService


class SellsByServicesService(ReportService):
    def __init__(self, repository: SellsByServicesRepository):
        self.repository = repository

    def get_report(self, filters: dict):
        return self.repository.get_report(filters)

    def get_top_by_services(self, filters):
        return self.repository.get_top_by_service
