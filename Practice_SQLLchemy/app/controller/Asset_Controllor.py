from app.models.user_model import Asset, db,Vendor
from app.utils.comman_utils import add_in_entity


def check_vendorname_existence(vendorname):
    count=Vendor.query.filter_by(vendorname=vendorname).count()
    if count>0:
        return True
    return False

def insert_asset(AssetName,AssetType,vendorname):
    new_asset= Asset(
        AssetName=AssetName,
        AssetType=AssetType,
        vendorname=vendorname
    )
    add_in_entity(new_asset)

def fetch_asset_data():
    assets=Asset.query.all()
    data=[]
    for asset in assets:
        data.append(
                {
                    "AssetName": asset.AssetName,
                    "AssetType": asset.AssetType,
                    "vendorname": asset.vendorname
                })
    return data

def get_total_asset():
    total_records = Asset.query.count()
    return total_records

def fetch_asset_vendor_details():
    assets = Asset.query.join(Vendor, Asset.vendorname == Vendor.vendorname).all()

    result = []
    for asset in assets:
        asset_data = {
            'Asset_Serial_Number': asset.AssetSerialNumber,
            'Asset_Name': asset.AssetName,
            'Asset_Type': asset.AssetType,
            'vendor_name': asset.vendor.vendorname,
            'vendor_emailid': asset.vendor.vendoremailid,
            'vendor_mobileno': asset.vendor.mobileno,
            'vendor_address': asset.vendor.address
        }
        result.append(asset_data)
    return result
