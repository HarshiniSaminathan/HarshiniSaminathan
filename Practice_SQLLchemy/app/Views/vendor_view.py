from flask import Blueprint

from app.service.vendor_service import add_vendor,vendor_email_check,get_vendors,edit_vendor,delete_vendor_route,vendor_names

vendorapi_blueprint = Blueprint('vendorapi', __name__)

@vendorapi_blueprint.route('/addvendor', methods=['POST'])
def addvendor():
    return add_vendor()

@vendorapi_blueprint.route('/vendoremailcheck/<string:vendoremailid>',methods=['GET'])
def vendoremailcheck(vendoremailid):
    return vendor_email_check(vendoremailid)

@vendorapi_blueprint.route("/getvendors", methods=['GET'])
def vendordetails():
    return get_vendors()

@vendorapi_blueprint.route("/editvendor/<string:vendoremailid>",methods=['PUT'])
def editvendor(vendoremailid):
    return edit_vendor(vendoremailid)

@vendorapi_blueprint.route("/deletevendor/<string:vendoremailid>", methods=['DELETE'])
def deletevendor(vendoremailid):
    return delete_vendor_route(vendoremailid)

@vendorapi_blueprint.route("/vendornames",methods=['GET'])
def vendornames():
    return vendor_names()

