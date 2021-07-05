from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.services import taxables_perceptions_service
from app.utils import make_filters


payroll_routes = Blueprint("payroll_routes", __name__, url_prefix="/v1/payroll/reports")


@payroll_routes("/taxables_perceptions", methods=["GET"])
@cross_origin()
def taxables_perceptions():
    company_rfc = request.args.get("datos.Rfc")
    to_date = request.args.get("to_date")
    from_date = request.args.get("from_date")
    rfc = request.args.get("rfc")
    filters = make_filters(
        company_rfc=company_rfc,
        from_date=from_date,
        to_date=to_date,
        rfc=rfc,
        date_field="datos.Fecha",
    )
    data = taxables_perceptions_service.get_report(filters)
    if not data:
        return make_response(
            dumps(
                {"status": False, "message": "No se encontraron datos con esos filtros"}
            ),
            404,
        )
    return make_response(dumps({"status": True, "data": data}), 200)


@payroll_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
