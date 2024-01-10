import logging
import os
import uuid

from flask import request
from werkzeug.utils import secure_filename

from app.controller.adminController import insert_employee, check_empId_exists, get_empDetails_by_empId, \
    add_new_vendors, add_new_assets, assign_new_asset, add_new_acc, assign_acc
from app.response import success_response,failure_response
import pandas as pd
import openpyxl


def read_file_data(file, file_extension):
    try:
        if file_extension == '.csv':
            data = pd.read_csv(file)
            return data
        elif file_extension == '.xlsx':
            data = pd.read_excel(file, engine='openpyxl')
            return data
        else:
            return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def add_Employee():
    try:
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1]
            if file_extension in ['.csv', '.xlsx']:
                read_data = read_file_data(file, file_extension)
                if read_data is not None:
                    records_to_insert = read_data.values.tolist()
                    existing_empId = []
                    for record in records_to_insert:
                        emp_id, emp_name, emp_emailId, designation, company_name = record
                        if not check_empId_exists(emp_id):
                            insert_employee(emp_id, emp_name,emp_emailId, designation, company_name)
                        else:
                            existing_empId.append(emp_id)
                    if len(existing_empId) == 0:
                        return success_response('All datas added successfully')
                    else:
                        existing_empIds_str = ', '.join(map(str, existing_empId))
                        return success_response(f'{existing_empIds_str} already exists')
                else:
                    return failure_response(statuscode='400', content='Unable to read CSV / Excel file')
            else:
                return failure_response('409', f'{file_extension} files not allowed')
        elif all(key in request.form for key in ['emp_id', 'emp_name', 'emp_emailId','designation', 'company_name']):
            emp_id = request.form.get('emp_id')
            emp_name = request.form.get('emp_name')
            emp_emailId = request.form.get('emp_emailId')
            emp_designation = request.form.get('designation')
            company_name = request.form.get('company_name')
            if not check_empId_exists(emp_id):
                insert_employee(emp_id, emp_name, emp_emailId,emp_designation, company_name)
                return success_response('Employee added successfully')
            return failure_response('409', 'Emp_id already exists')
        else:
            return failure_response(statuscode='400', content='Fields / files missing to insert.')

    except Exception as e:
        print(f"Error: {e}")
        return failure_response(statuscode='500', content=f'An unexpected error occurred: {e}')

def search_by_empId(emp_id,company_name):
    try:
        if emp_id:
            get_empId_empName = get_empDetails_by_empId(emp_id,company_name)
            if get_empId_empName:
                return success_response(get_empId_empName)
            else:
                return failure_response(statuscode='400', content=f'Employee with ID {emp_id} not found')
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return failure_response(statuscode='500', content=f'An unexpected error occurred: {e}')

def add_vendors():
    try:
        add_new_vendors()
        return success_response("success")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return failure_response(statuscode='500', content=f'An unexpected error occurred: {e}')

def add_new_Assets():
    try:
        add_new_assets()
        return success_response("success")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return failure_response(statuscode='500', content=f'An unexpected error occurred: {e}')
def assign_asset():
    try:
        assign_new_asset()
        return success_response("success")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return failure_response(statuscode='500', content=f'An unexpected error occurred: {e}')
def add_new_accessory():
    try:
        add_new_acc()
        return success_response("success")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return failure_response(statuscode='500', content=f'An unexpected error occurred: {e}')
def assign_new_Acc():
    try:
        assign_acc()
        return success_response("success")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return failure_response(statuscode='500', content=f'An unexpected error occurred: {e}')




