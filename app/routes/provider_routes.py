from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.services import (detailed_service, sells_by_clients_service)
from app.utils import make_filters

detailed_routes = Blueprint("detailed_report", __name__, url_prefix="/v1/report/detialed")


@detailed_routes.route("/provider", methods=["GET"])
@cross_origin()
def providers_detailed_report():
    filters = {
        "datos.Fecha": {
            "$gte": request.args.get("from_date"),
            "$lte": request.args.get("to_date"),
        },
        "Receptor.Rfc": request.args.get("rfc"),
    }
    report = detailed_service.get_provider_report(filters)
    if not report:
        return make_response(dumps({"status": False}), 404)

    return make_response(dumps({"status": True, "data": report}), 200)

@detailed_routes.route("/all", methods=["GET"])
@cross_origin()
def total_detailed_report():
    filters = {
        "datos.Fecha": {
            "$gte": request.args.get("from_date"),
            "$lte": request.args.get("to_date"),
        },
        "Receptor.Rfc": request.args.get("rfc"),
        "datos.Cancelado": None
    }
    report_pro = detailed_service.get_provider_report(filters)

    filters = make_filters(
        company_rfc=request.args.get("rfc"),
        date_field="datos.Fecha",
        from_date=request.args.get("from_date"),
        to_date=request.args.get("to_date")
    )
    report_ser = sells_by_clients_service.get_detail_report(filters)

    if (not report_pro) and (not report_ser):
        return make_response(dumps({"status": False}), 404)

    return make_response(dumps({"status": True, "data": report_pro+report_ser}), 200)


@detailed_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
