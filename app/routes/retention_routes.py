from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.services import retention_service
from app.utils import make_filters


retention_routes = Blueprint(
    "retention_routes", __name__, url_prefix="/v1/retentions/reports"
)


@retention_routes.route("/", methods=["GET"])
@cross_origin()
def retention_report():
    company_rfc = request.args.get("datos.Rfc")
    retention_type = request.args.get("type")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    filters = make_filters(
        company_rfc=company_rfc,
        retention_type=retention_type,
        from_date=from_date,
        to_date=to_date,
        date_field="datos.Fecha",
    )
    report_data = retention_service.get_report(filters)
    if not report_data:
        return make_response(
            dumps({"status": False, "message": "No se encontraron datos en el reporte"}),
            404,
        )
    return make_response(dumps({"status": True, "data": report_data}), 200)
@retention_routes.route("/nominas", methods=["GET"])
@cross_origin() 
def nominas():
    empresa      =  request.args.get('empresa') 
    empleado     =  request.args.get('empleado') 
    dataFrom     =  request.args.get('from') 
    dataTo       =  request.args.get('to')  

    filters = make_filters(
        company_rfc=empresa,
        from_date=dataFrom,
        to_date=dataTo,
        date_field="datos.Fecha",
    ) 

    filters = [ { "empresa" : empresa, "empleado" : empleado, "dataFrom" : dataFrom, "dataTo" : dataTo }]
    report_data = retention_service.get_report_nomina(filters)  
    
    return make_response(dumps( report_data ), 200)


@retention_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
