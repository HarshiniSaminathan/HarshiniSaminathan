# Import required modules
import json
import logging

from openpyxl.utils import coordinate_to_tuple

logging.basicConfig(level=logging.INFO)
from flask import jsonify
import bcrypt
import os
from os.path import join, dirname



# Define commonly used helper functions
def to_json(data):
    """
    Convert a dictionary to JSON format.

    :param data: The dictionary to convert to JSON.
    :return: A string representing the JSON data.
    """
    return json.dumps(data)

def from_json(json_str):
    """
    Convert a string in JSON format to a dictionary.

    :param json_str: The string in JSON format to convert.
    :return: A dictionary representing the JSON data.
    """
    return json.loads(json_str)

def hash_password(password):
    """
    Hash a password using the bcrypt algorithm.

    :param password: The password to hash.
    :return: A string representing the hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def check_password(password, hashed_password):
    """
    Check if a password matches its hashed representation.

    :param password: The plain-text password to check.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# json schema validation
def schema_validator(data, schema_file_path=None,schema=None):
    """ Checks whether the given data matches the schema """
    try:
        if schema==None:
            schema = _load_json_schema(schema_file_path)
            return validate(data, schema)
        else:
            return validate(data, schema)
    except exceptions.ValidationError as err:
        return err.message


def _load_json_schema(filename):
    """ Loads the given schema file """

    relative_path = join('../models', filename)
    print("relative_path", relative_path)
    absolute_path = join(dirname(__file__), relative_path)
    print("absolute_path", absolute_path)
    base_path = dirname(absolute_path)
    print("base_path", base_path)
    base_uri = 'file://{}/'.format(base_path)
    print("base_uri", base_uri)
    with open(absolute_path) as schema_file:
        return jsonref.loads(schema_file.read(), base_uri=base_uri, jsonschema=True)


# def send_verification_email(email):
#     #verification code
#     verification_token = str(uuid.uuid4())
#     # Send the verification email with the verification link
#     verification_url ='http://localhost:5000/api/v1/user/verification/' + verification_token
#     msg = Message('Email verification', recipients=email)
#     msg.body = f'Please click the following link to verify your email: {verification_url}'
#     mail.send(msg)
#     return jsonify({'message': 'Verification email sent.'})

def send_vendor_mail_0(from_mail, to_email, type,agency_name):
    try :
        logging.info(f'sending email from %s',{from_mail})
        logging.info(f'sending email to %s', {to_email})
        from flask_mail import Message
        subject = f"{type} has been created"
        body =  f'Hi there , {type} is created  along with {agency_name}'

        message = Message(subject, sender=from_mail, recipients=[to_email] , bcc=['shaheen.karoji@adityabirla.com','yashwant.salian@adityabirla.com'])
        # logging.info('Message %s',message)
        message.body = body
        # logging.info('Message body %s', message.body)
        logging.info('sending email')
        mail.send(message)
        logging.info('sende email')
        # logging.info(f'Email sent to %s',to_email)
        print(f"email sent to {to_email}")
    except Exception as e:
        logging.info('Something went wrong %s',e)


