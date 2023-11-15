# model.py
from app.utils.postgres_utils import dbconnection

def get_total_records():
    conn = dbconnection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM userinfo")
    total_records = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total_records

def fetch_user_data(limit, offset):
    conn = dbconnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM userinfo ORDER BY recenttime DESC LIMIT %s OFFSET %s", (limit, offset))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def insert_user(emailid, firstname, lastname, mobileno, dob, address):
    conn = dbconnection()
    cur = conn.cursor()
    query = "INSERT INTO USERINFO (EMAILID, FIRSTNAME, LASTNAME, MOBILENO, DOB, ADDRESS, RECENTTIME) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
    cur.execute(query, (emailid, firstname, lastname, mobileno, dob, address))
    conn.commit()
    cur.close()
    conn.close()

def check_email_existence(emailid):
    conn = dbconnection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM userinfo WHERE emailid=%s", (emailid,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count > 0

def update_user(emailid, firstname, lastname, mobileno, dob, address):
    conn = dbconnection()
    cur = conn.cursor()
    cur.execute("UPDATE USERINFO SET EMAILID=%s, FIRSTNAME=%s, LASTNAME=%s, MOBILENO=%s, DOB=%s, ADDRESS=%s ,RECENTTIME=CURRENT_TIMESTAMP WHERE EMAILID=%s", (emailid, firstname, lastname, mobileno, dob, address, emailid))
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(emailid):
    conn = dbconnection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM userinfo WHERE emailid=%s", (emailid,))
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

def delete_user(emailid):
    conn = dbconnection()
    cur = conn.cursor()
    cur.execute("DELETE FROM USERINFO WHERE emailid = %s", (emailid,))
    conn.commit()
    cur.close()
    conn.close()


