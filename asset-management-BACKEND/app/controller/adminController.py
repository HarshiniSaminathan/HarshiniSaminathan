from app.models.acceessoriesModel import AccessoriesTable
from app.models.accessoriesAssModel import AccessoriesAssTable
from app.models.assetAssignmentModel import AssetAssignmentTable
from app.models.assetModel import AssetTable
from app.models.employeeModel import EmployeeTable
from app.models.vendorModel import VendorTable
from app.utils.commanUtils import add_in_entity


def insert_employee(emp_id,emp_name,emp_emailId,emp_designation,company_name):
    emp_status ="ACTIVE"
    new_employee=EmployeeTable(
        emp_id=int(emp_id),
        emp_name=emp_name,
        emp_emailId=emp_emailId,
        designation=emp_designation,
        company_name=company_name,
        emp_status=emp_status
    )
    add_in_entity(new_employee)

def check_empId_exists(emp_id):
    count = EmployeeTable.query.filter_by(emp_id=emp_id).count()
    if count > 0:
        return True
    else:
        return False

def get_empDetails_by_empId(emp_id,company_name):
    employee_detail = EmployeeTable.query.filter_by(emp_id=int(emp_id),company_name=company_name).first()
    if employee_detail:
        emp_detail=[]
        emp_detail.append(
            {
                "emp_id":employee_detail.emp_id,
                "emp_name":employee_detail.emp_name
            }
        )
        return emp_detail
    else:
        return None

def add_new_vendors():
    vendor_status="ACTIVE"
    new_vendor=VendorTable(
        vendor_name="demo",
        vendor_status=vendor_status,
        location="Bangalore"
    )
    add_in_entity(new_vendor)
def add_new_assets():
    asset_status="UNASSIGNED"
    new_asset=AssetTable(
        asset_Serial_no=112,
        asset_type="demo",
        asset_name="demo",
        asset_os="demo",
        asset_spec="128 RAM",
        asset_price="5678",
        asset_validity="3 months",
        issued_at="2024-01-06",
        asset_status=asset_status,
        vendor_id=1
    )
    add_in_entity(new_asset)

def assign_new_asset():
    new_asset_ass = AssetAssignmentTable(
        asset_id=1,
        emp_pk_id=2,
        Returned_at="2024-01-06",
        Return_type="demo",
        condition="128 RAM",
        assigned_at="2024-01-06"
    )
    add_in_entity(new_asset_ass)

def add_new_acc():
     new_acc_Add = AccessoriesTable(
         accessory_name="muse",
         accessory_count=2,
         assigned_count=0
     )
     add_in_entity(new_acc_Add)

def assign_acc():
     new_acc_assign = AccessoriesAssTable(
         emp_pk_id=2,
         accessory_id=1,
         assigned_at="2024-01-06",
         return_type="demo",
         condition="128 RAM",
         return_at="2024-01-06"

     )
     add_in_entity(new_acc_assign)

