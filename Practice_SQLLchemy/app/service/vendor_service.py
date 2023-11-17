from flask import jsonify, request
from app.controller.vendor_controllor import check_vendor_email_existence, insert_vendor,fetch_vendor_data,get_total_records,update_vendor,delete_vendor,list_vendor_names
from app.response import failure_response, success_response


def add_vendor():
    try:
        data = request.get_json()
        vendoremailid = data.get('vendoremailid')
        vendorname = data.get('vendorname')
        mobileno = data.get('mobileno')
        address = data.get('address')
        if check_vendor_email_existence(vendoremailid):
            return failure_response(statuscode='409',content='Emailid already exists')
        insert_vendor(vendoremailid, vendorname, mobileno, address)
        return success_response('Vendor Added Sucessfully')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400',content=str(e))


def vendor_email_check(vendoremailid):
    if check_vendor_email_existence(vendoremailid):
        return success_response('Emailid Already exists')
    else:
        return failure_response(statuscode='409', content='Emailid Does Not Exists')

def get_vendors():
    data = fetch_vendor_data()
    total_records = get_total_records()
    return success_response({'data':data,'X-Total-Count': str(total_records)})


def edit_vendor(vendoremailid):
    if check_vendor_email_existence(vendoremailid):
        try:
            data=request.get_json()
            vendorname = data.get('vendorname')
            mobileno = data.get('mobileno')
            address = data.get('address')
            update_vendor(vendoremailid,vendorname,mobileno,address)
            return success_response('Vendor updated successfully')
        except Exception as e:
            print(f"Error: {e}")
            return failure_response(statuscode='500',content=str(e))
    else:
        return failure_response(statuscode='500',content='Emailid Does Not Exists')

def delete_vendor_route(vendoremailid):
    try:
        if not check_vendor_email_existence(vendoremailid):
            return failure_response(statuscode='500',content='Emailid Does Not Exists')
        delete_vendor(vendoremailid)
        return success_response('Vendor Deleted Successfully')
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400', content=str(e))


def vendor_names():
    try:
        lists=list_vendor_names()
        return success_response({'data':lists})
    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='400', content=str(e))