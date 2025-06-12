from application import *
import datetime

now = datetime.datetime.now()
day = str(now.day)
month = str(now.month)
year = str(now.year)

date = request.form.get('dob')
print (now)
print (day+'/'+month+'/'+year)
print (date)