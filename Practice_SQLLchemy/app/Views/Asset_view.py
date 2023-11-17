from flask import Blueprint

from app.service.Asset_Service import add_asset,get_asset,get_asset_vendor_details

asset_api_blueprint = Blueprint('assetapi', __name__)

@asset_api_blueprint.route('/addasset', methods=['POST'])
def addasst():
    return add_asset()

@asset_api_blueprint.route('/getassets',methods=['GET'])
def getasset():
    return get_asset()

@asset_api_blueprint.route('/GetAssetsWithVendorDetails',methods=['GET'])
def GetAssetsWithVendorDetails():
    return get_asset_vendor_details()