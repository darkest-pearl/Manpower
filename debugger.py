from models import *

employee = Employee.query.get(3)
employee.pport = False

db.session.commit()