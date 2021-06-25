from app.services.authentication import token_required
from app.services.service import ReportService
from app.services.sells_by_clients import SellsByUsersService
from app.repository import sells_clients_repo

sells_by_clients_service = SellsByUsersService(sells_clients_repo)
