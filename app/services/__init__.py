from app.services.authentication import token_required
from app.services.service import ReportService
from app.services.sells_by_clients import SellsByUsersService
from app.repository import (
    sells_clients_repo,
    sells_by_items_repo,
    taxables_perceptions_repo,
    sells_by_services_repo,
)
from app.services.sells_by_items import SellsByItemsService
from app.services.sells_by_services import SellsByServicesService
from app.services.payroll_reports.taxables_perceptions_service import (
    TaxablesPerceptionsService,
)

sells_by_clients_service = SellsByUsersService(sells_clients_repo)
sells_by_items_service = SellsByItemsService(sells_by_items_repo)
taxables_perceptions_service = TaxablesPerceptionsService(taxables_perceptions_repo)
sells_by_services_service = SellsByServicesService(sells_by_services_repo)
