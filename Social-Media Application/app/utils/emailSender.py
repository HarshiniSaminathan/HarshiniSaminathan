import random

from flask_mail import Message

from run import mail

import time
sender='sharshini2003@gmail.com'

global_otp= None
global_Email=None
def generate_otp():
    return str(random.randint(10000, 99999))

def otpSending(EmailId):
    OTP=generate_otp()
    global_otp=OTP
    global_Email=EmailId
    subject ='OTP Verification'
    body = f'Your OTP is: {OTP}. \n This is to verify your account for FORGOT-PASSWORD-VERIFICATION. \n\n Note: This is an auto-generated mail. Don\'t reply to this email.'
    message = Message(subject, sender=sender,recipients=[EmailId], body=body)
    mail.send(message)
    return global_otp,global_Email

