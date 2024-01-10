

from flask import Blueprint, current_app, jsonify,request

from app.controller.patientController import sending_ad
from app.models.userModel import db
from app.service.adminService import (register_doctor, response_For_Feedback, get_Register_Doctor_Records,
                                      get_All_Feedback, uploading_Doctor_Excel,
                                      download_Errors_InExcel, download_Valid_InExcel, patient_Excel,

                                      register_Admin, get_Register_Admin_Records, add_Slot_To_Doctors,
                                      update_Slots_status, store_Records_Of_CSVIn_DB, download_csv, data_analytics,
                                      uploading_Ads, table_Data_In_Email)
from app.service.userService import token_required

adminapi_blueprint = Blueprint('adminapi', __name__, url_prefix='/api/admin')

@adminapi_blueprint.route("/registerDoctor",methods=['POST'])
@token_required(['ADMIN'])
def registerDoctor():
    return register_doctor()

@adminapi_blueprint.route("/getRegisterDoctorRecords",methods=['GET'])
@token_required(['ADMIN','DOCTOR','PATIENT'])
def getRegisterDoctorRecords():
    cache = current_app.cache
    cached_data = cache.get('getRegisterDoctorRecords_cache')
    if cached_data is None:
        cached_data = get_Register_Doctor_Records()
        cache.set('getRegisterDoctorRecords_cache', cached_data)
    return cached_data

@adminapi_blueprint.route("/registerAdmin",methods=['POST'])
@token_required(['ADMIN'])
def registerAdmin():
    return register_Admin()

@adminapi_blueprint.route("/getRegisterAdminRecords",methods=['GET'])
@token_required(['ADMIN'])
def getRegisterAdminRecords():
    return get_Register_Admin_Records()

@adminapi_blueprint.route("/addSlotToDcotors",methods=['POST'])
@token_required(['ADMIN'])
def addSloToDoctors():
    return add_Slot_To_Doctors()

@adminapi_blueprint.route("updateSlotStatus/<string:doctorEmailId>",methods=['PUT'])
@token_required(['ADMIN','DOCTOR'])
def updateSlotStatus(doctorEmailId):
    return update_Slots_status(doctorEmailId)

@adminapi_blueprint.route("getAllFeedback",methods=['GET'])
@token_required(['ADMIN'])
def getAllFeedback():
    return get_All_Feedback()

@adminapi_blueprint.route("responseForFeedback",methods=['PUT'])
@token_required(['ADMIN'])
def responseForFeedback():
    return response_For_Feedback()

@adminapi_blueprint.route("uploadingDoctorExcel",methods=['POST'])
def uploadingDoctorExcel():
    return uploading_Doctor_Excel()

@adminapi_blueprint.route("uploadingAds",methods=['POST'])
def uploadingAds():
    return uploading_Ads()

@adminapi_blueprint.route("downloadErrorsInExcel",methods=['GET'])
def downloadErrorsInExcel():
    return download_Errors_InExcel()

@adminapi_blueprint.route("downloadValidInExcel",methods=['GET'])
def downloadValidInExcel():
    return download_Valid_InExcel()

@adminapi_blueprint.route("patientExcel",methods=['GET'])
def patientExcel():
    return patient_Excel()

@adminapi_blueprint.route("storeRecordsOfCSVInDB",methods=['POST'])
def storeRecordsOfCSVInDB():
    return store_Records_Of_CSVIn_DB()

@adminapi_blueprint.route('/download_csv',methods=['GET'])
def downloadcsv():
    return download_csv()

@adminapi_blueprint.route("/data_analytics", methods=["GET"])
def dataAnalytics():
    return data_analytics()

@adminapi_blueprint.route("/sending_ad",methods=['POST'])
def sendingAd():
    return sending_ad()

@adminapi_blueprint.route("/tableDataInEmail",methods=['GET'])
def tableDataInEmail():
    return table_Data_In_Email()

from geopy.geocoders import Nominatim
from app.response import success_response,failure_response

@adminapi_blueprint.route("convertLatLonToAdd",methods=['GET'])
def convertLatLonToAdd():
    geoLoc = Nominatim(user_agent='GetLoc')
    # localname=geoLoc.reverse("11.1888, 77.7723")
    localname = geoLoc.reverse(" 12.9610° N, 77.6387° E")
    location=localname.address
    if location:
        return success_response(location)
    else:
        return failure_response(statuscode='409', content='Unable to geocode the address')


@adminapi_blueprint.route("convertAddressToLatLon", methods=['GET'])
def convertAddressToLatLon():
    geoLoc = Nominatim(user_agent='GetLoc')
    original_address = 'HAL Old Airport Road, Domlur, Domlur Ward, East Zone, Bengaluru, Bangalore North, Bengaluru Urban District, Karnataka, 560071, India'
    # original_address = 'Pasur R.S. - Elumathur - Vellodu Road, Elumathur, Modakkurichi, Erode District, Tamil Nadu, 637210, India'
    location = geoLoc.geocode(original_address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return success_response({"latitude": latitude, "longitude": longitude})
    else:
        return failure_response(statuscode='409', content='Unable to geocode the address')

