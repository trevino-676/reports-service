import uuid

from app import app
from app.models import SellsByServices
from app.repository import ReportRepository


class SellsByServicesRepository(ReportRepository):
    def get_report(self, filters: dict) -> list:
        try:
            report = SellsByServices.get_sells_by_services(filters)
            if len(report) == 0:
                return None

            for item in report:
                item["uuid"] = uuid.uuid4().hex

            return report
        except Exception as e:
            app.logger.error(e)
            return None

    def get_top_by_service(self, filters):
        try:
            data = SellsByServices.get_top_by_service(filters)
            return data
        except Exception as e:
            app.logger.error(e)
            return None
