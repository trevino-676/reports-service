from app import app
from app.models import Sells_By_Client
from app.repository import ReportRepository


class Sells_By_Client_Repository(ReportRepository):
    def get_report(self, filters: dict) -> list:
        try:
            report = Sells_By_Client.get_sells_by_client(filters)
            if len(report) == 0:
                return None
            return report
        except Exception as e:
            app.logger.error(e)
            return None

    def get_detail_report(self, filters: dict):
        try:
            data = Sells_By_Client.sells_details_report(filters)
            if len(data) == 0:
                return None
            return data
        except Exception as e:
            app.logger.error(e)
            return None

    def get_total_report(self, filters: dict):
        try:
            data = Sells_By_Client.get_total_sells(filters)
            return data
        except Exception as e:
            app.logger.error(e)
            return None
