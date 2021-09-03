from app.repository import Sells_By_Client_Repository
from app.services import ReportService


class SellsByUsersService(ReportService):
    def __init__(self, repository: Sells_By_Client_Repository):
        self.repository = repository

    def get_report(self, filters: dict):
        return self.repository.get_report(filters)

    def get_detail_report(self, filters: dict):
        return self.repository.get_detail_report(filters)

    def get_total_report(self, filters: dict):
        return self.repository.get_total_report(filters)

    def get_top_by_clients(self, filters):
        return self.repository.get_top_by_clients(filters)
