from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.services import sells_by_clients_service, sells_by_items_service
from app.utils import make_filters
from app import app


sells_by_client_routes = Blueprint(
    "user_by_client", __name__, url_prefix="/v1/sellsreport"
)


@sells_by_client_routes.route("/by_client", methods=["GET"])
@cross_origin()
def sells_by_client():
    company_rfc = request.args.get("datos.Rfc")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    amount = request.args.get("amount")
    status = request.args.get("status")
    rfc = request.args.get("rfc")
    filters = make_filters(
        company_rfc=company_rfc,
        from_date=from_date,
        to_date=to_date,
        amount=amount,
        status=status,
        rfc=rfc,
        date_field="datos.Fecha",
    )
    app.logger.info(filters)
    report = sells_by_clients_service.get_report(filters)
    if not report:
        resp = make_response(
            dumps({"status": False, "message": "No se encontraron datos del reporte"}),
            404,
        )
        return resp

    resp = make_response(dumps({"status": True, "data": report}), 200)
    return resp


@sells_by_client_routes.route("/by_items", methods=["GET"])
@cross_origin()
def sells_by_items():
    company_rfc = request.args.get("datos.Rfc")
    to_date = request.args.get("to_date")
    from_date = request.args.get("from_date")
    filters = make_filters(
        company_rfc=company_rfc,
        date_field="datos.Fecha",
        from_date=from_date,
        to_date=to_date,
    )
    report = sells_by_items_service.get_report(filters)

    if not report:
        return make_response(
            dumps({"status": False, "message": "No se encontraron datos."}), 404
        )

    return make_response(dumps({"status": True, "data": report}), 200)


@sells_by_client_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
