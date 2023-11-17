from flask import request
from app.controller.Asset_Controllor import check_vendorname_existence,insert_asset,fetch_asset_data,get_total_asset,fetch_asset_vendor_details
from app.response import success_response, failure_response

def add_asset():
    try:
        data = request.get_json()
        AssetName = data.get('AssetName')
        AssetType = data.get('AssetType')
        vendorname = data.get('vendorname')
        if check_vendorname_existence(vendorname):
            insert_asset(AssetName,AssetType,vendorname)
            return success_response('Asset Added Sucessfully')
        return failure_response(statuscode='409',content='Vendor Does Not Exists')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400',content=str(e))

def get_asset():
    data = fetch_asset_data()
    total_records = get_total_asset()
    return success_response({'data': data, 'X-Total-Count': str(total_records)})

def get_asset_vendor_details():
    data= fetch_asset_vendor_details()
    return success_response({'data': data})