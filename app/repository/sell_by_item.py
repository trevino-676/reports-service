import uuid

from app import app
from app.models import SellsByItems
from app.repository import ReportRepository


class SellsByItemsRepository(ReportRepository):
    def get_report(self, filters: dict) -> list:
        try:
            report = SellsByItems.get_sells_by_items(filters)
            for item in report:
                item["uuid"] = uuid.uuid4().hex
            if len(report) == 0:
                return None
            return report
        except Exception as e:
            app.logger.error(e)
            return None

    def get_top_by_items(self, filters):
        try:
            data = SellsByItems.get_top_by_items(filters)
            return data
        except Exception as e:
            app.logger.error(e)
            return None
