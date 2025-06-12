import smtplib
import imghdr
from email.message import EmailMessage
from models import *

def send_gmail(reciever, employee):
    Sender_Email = "tayseeragencyforhiring971@gmail.com"
    Password = input("type in your password")
    Reciever_Email = 'munirasaid1979@gmail.com'
    
    passport = Passport.query.filter(Passport.employee_id == employee.id).first()

    message = EmailMessage()
    message['Subject'] = "Employee profile from Tayseer Agency"
    message['From'] = Sender_Email
    message['To'] = Reciever_Email

    if Reciever_Email == "eritreanlabouroffice@gmail.com":
        content = f"""
Personal Details

Name: {employee.name}
Date of Birth: {employee.dob}
Place of Birth: {employee.pob}
Gender: {employee.gender}
Address: {employee.address}
Civil Status: {employee.status}

Passport Details

Passport ID.: {passport.pass_no}
Place of Issue : {passport.place_of_issue}
Date of Issue: {passport.date_of_issue}

Attachment Images are below:-
        """
        message.set_content(content)

        files = ['LargeElementArray.pdf']
    else:        
        content = f"""
Name: {employee.name}   Age: {employee.name}
Gender: {employee.gender}
Religion: {employee.religion}
Position of work: {employee.position}
Education: {employee.education}
Spoken Languages: {employee.languages}

Attachment Images are below
    """

        message.set_content(content)

        files = ['LargeElementArray.pdf']
    try:
        for file in files:
            with open(file, 'rb') as f:
                image_data = f.read()
                image_type = imghdr.what(f.name)
                image_name = f.name
            message.add_attachment(image_data, maintype='application', subtype=image_type, filename=image_name)
    except:
        pass
    try:    
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(Sender_Email, Password)
            if smtp.send_message(message):
                if Reciever_Email == "eritreanlabouroffice@gmail.com":
                    employee.sent_1 = 1
                else:
                    employee.sent_2 = 1
                db.session.commit()
    except:
        pass