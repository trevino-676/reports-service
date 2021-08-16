from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.services import detailed_service

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


@detailed_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
