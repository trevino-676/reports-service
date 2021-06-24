from abc import ABC, abstractmethod


class ReportService(ABC):
    @abstractmethod
    def get_report(self, filters):
        pass
