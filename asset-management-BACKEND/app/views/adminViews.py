from flask import Blueprint, request, abort

from app.service.adminService import add_Employee, search_by_empId, add_vendors, add_new_Assets, assign_asset, \
    add_new_accessory, assign_new_Acc

adminapi_blueprint = Blueprint('adminapi', __name__, url_prefix='/assets')

@adminapi_blueprint.route("/employee/add", methods=['POST'])
def add_employee():
    return add_Employee()
@adminapi_blueprint.route("/dashboard/search/<emp_id>",methods=['GET'])
def search_empId(emp_id):
    company_name = request.args.get('type')
    if not emp_id:
        abort(400, description='Employee ID is required in the URL endpoint.')
    return search_by_empId(emp_id, company_name)

@adminapi_blueprint.route("addvendor",methods=['POST'])
def add_vendor():
    return add_vendors()
@adminapi_blueprint.route("addassets",methods=['POST'])
def add_Assets():
    return add_new_Assets()

@adminapi_blueprint.route("assignasset",methods=['POST'])
def assign_Asset():
    return assign_asset()

@adminapi_blueprint.route("addaccessory",methods=['POST'])
def add_accessory():
    return add_new_accessory()

@adminapi_blueprint.route("assign-acc",methods=['POST'])
def assign_accessory():
    return assign_new_Acc()