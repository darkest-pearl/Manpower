from models import *


def get_employee_sresult(search):

        split = search.split()
    
        if len(split) > 2 :
            first = split[0]
            middle = split[1]
            last = split[2]

            firstc = first.capitalize()
            middlec = middle.capitalize()
            lastc = last.capitalize()

            employees1 = Employee.query.filter(Employee.name.like("%"+first+' '+middle+' '+last+"%")).order_by(Employee.id).all()
            employees2 = Employee.query.filter(Employee.name.like("%"+firstc+' '+middlec+' '+lastc+"%")).order_by(Employee.id).all()


            employeesum = employees1 + employees2

            

        elif len(split) > 1 :
            first = split[0]
            middle = split[1]

            firstc = first.capitalize()
            middlec = middle.capitalize()

            employees1 = Employee.query.filter(Employee.name.like("%"+first+' '+middle+"%")).order_by(Employee.id).all()
            employees2 = Employee.query.filter(Employee.name.like("%"+firstc+' '+middlec+"%")).order_by(Employee.id).all()
            
            employeesum = employees1 + employees2

        elif (len(split) == 1) :

            search1 = search.capitalize()

            employees1 = Employee.query.filter(Employee.name.like("%"+search+"%")).order_by(Employee.id).all()
            employees2 = Employee.query.filter(Employee.name.like("%"+search1+"%")).order_by(Employee.id).all()
            #employees3 = Employee.query.filter(Employee.national_id.like("%"+search1+"%")).order_by(Employee.id).all()

            employeesum = employees1 + employees2

        else :
            employees = False
            return employees


        employees = []
        for employee in employeesum:
            if employee in employees:
                continue
            employees.append(employee)
        
       


        return employees            



def get_employer_sresult(search):

        split = search.split()
    
        if len(split) > 2 :
            first = split[0]
            middle = split[1]
            last = split[2]

            firstc = first.capitalize()
            middlec = middle.capitalize()
            lastc = last.capitalize()

            employers1 = Employer.query.filter(Employer.name.like("%"+first+' '+middle+' '+last+"%")).order_by(Employer.id).all()
            employers2 = Employer.query.filter(Employer.name.like("%"+firstc+' '+middlec+' '+lastc+"%")).order_by(Employer.id).all()


            employersum = employers1 + employers2

            

        elif len(split) > 1 :
            first = split[0]
            middle = split[1]

            firstc = first.capitalize()
            middlec = middle.capitalize()

            employers1 = Employer.query.filter(Employer.name.like("%"+first+' '+middle+"%")).order_by(Employer.id).all()
            employers2 = Employer.query.filter(Employer.name.like("%"+firstc+' '+middlec+"%")).order_by(Employer.id).all()
            
            employersum = employers1 + employers2

        elif (len(split) == 1) :

            search1 = search.capitalize()

            employers1 = Employer.query.filter(Employer.name.like("%"+search+"%")).order_by(Employer.id).all()
            employers2 = Employer.query.filter(Employer.name.like("%"+search1+"%")).order_by(Employer.id).all()
            employers3 = Employer.query.filter(Employer.national_id.like("%"+search1+"%")).order_by(Employer.id).all()

            employersum = employers1 + employers2 + employers3
            
        employers = []
        for employer in employersum:
            if employer in employers:
                continue
            employers.append(employer)


        return employers            


def get_broker_sresult(search):
    split = search.split()
    
    if len(split) > 2 :
        first = split[0]
        middle = split[1]
        last = split[2]

        firstc = first.capitalize()
        middlec = middle.capitalize()
        lastc = last.capitalize()

        brokers1 = Broker.query.filter(Broker.name.like("%"+first+' '+middle+' '+last+"%")).order_by(Broker.id).all()
        brokers2 = Broker.query.filter(Broker.name.like("%"+firstc+' '+middlec+' '+lastc+"%")).order_by(Broker.id).all()


        brokersum = brokers1 + brokers2

            

    elif len(split) > 1 :
        first = split[0]
        middle = split[1]

        firstc = first.capitalize()
        middlec = middle.capitalize()

        brokers1 = Broker.query.filter(Broker.name.like("%"+first+' '+middle+"%")).order_by(Broker.id).all()
        brokers2 = Broker.query.filter(Broker.name.like("%"+firstc+' '+middlec+"%")).order_by(Broker.id).all()
            
        brokersum = brokers1 + brokers2

    elif (len(split) == 1) :

        search1 = search.capitalize()

        brokers1 = Broker.query.filter(Broker.name.like("%"+search+"%")).order_by(Broker.id).all()
        brokers2 = Broker.query.filter(Broker.name.like("%"+search1+"%")).order_by(Broker.id).all()
        brokers3 = Broker.query.filter(Broker.national_id.like("%"+search1+"%")).order_by(Broker.id).all()

        brokersum = brokers1 + brokers2 + brokers3
            
    brokers = []
    for broker in brokersum:
        if broker in brokers:
            continue
        brokers.append(broker)

    return brokers

import datetime

def age_days(b_date):
    now = datetime.datetime.now()
    b_date = str(b_date)
    b_date = datetime.datetime.strptime(b_date, "%Y-%m-%d")
    age_days = ((now-b_date).total_seconds()/(24*3600))
    return age_days

def age_months(b_date):
    now = datetime.datetime.now()
    b_date = str(b_date)
    b_date = datetime.datetime.strptime(b_date, "%Y-%m-%d")
    age_months = ((now-b_date).total_seconds()/(30.43675*24*3600))
    return age_months

def age_years(b_date):
    now = datetime.datetime.now()
    b_date = str(b_date)
    try:
        b_date = datetime.datetime.strptime(b_date, "%Y-%m-%d")
    except:
        try:
            b_date = datetime.datetime.strptime(b_date, "%d-%m-%Y")
        except:
            try:
                b_date = datetime.datetime.strptime(b_date, "%m-%d-%Y")
            except:
                pass

    age_years = ((now-b_date).total_seconds()/(365.241*24*3600))
    return age_years

def dob_validate(dob):
    if (age_years(dob) < 20):
        return False
    elif (age_years(dob) > 45):
        return False
    else:
        return dob

def nat_validate(national_id, size):
    try:
        nat_id = national_id
        national_id = int(national_id)
        if len(nat_id) != size:
            return False
    except ValueError:
        return False
    
    employees = Employee.query.all()
    for employee in employees:
        if nat_id == employee.national_id:
            return False     

    return nat_id

def name_validate(name):
    no_err = 1
    split_name = name.split()
    
    if len(split_name) != 3:
        
        return False
    for word in split_name:
        for letter in word:
            try:
                test = int(letter)
                return False
            except:
                pass
    f_name = split_name[0].capitalize()
    m_name = split_name[1].capitalize()
    l_name = split_name[2].capitalize()
    
    name = (f_name+' '+m_name+' '+l_name)
    
    return name

def contact_validate(contact):
    no_err = 1
    if len(contact) != 0:
        try:
            if (eval(contact[0]) != 0):
                return False
            elif (eval(contact[1]) != 7):
                return False
            elif len(contact) != 8 :
                return False
            elif int(contact) >= 7900000 :
                return False
            else:
                par_contact = contact[1::]
                contact = '00291'+par_contact
                return contact
        except ValueError:
            return False
    else:
        return False

def salary_validate(salary):
    try:
        int_sal = int(salary)
        if (int_sal < 1300) or (int_sal > 1800):
            return False
        else:
            val_salary = int_sal
    except ValueError:
        return False

    return val_salary

def passport_validate(pass_no, issue):
    result = []
    #passport number validation
    if len(pass_no) == 0:
        return False, False
    elif len(pass_no) != 8:
        return False, 'Please enter a valid passport number'
    elif pass_no[0] != 'k':
        return False, 'Please enter passport number starting with k'
    elif pass_no[1] != '0':
        return False, 'Please enter valid ER passport number'
    else:
        pass_no = pass_no

    passports = Passport.query.all()
    for passport in passports:
        if passport.pass_no == pass_no:
            return False, 'The passport is already registered in database'
    
    #date of issue validate
    now = datetime.datetime.now()
    issue_date = datetime.datetime.strptime(issue, '%Y-%m-%d')
    age_days = ((now-issue_date).total_seconds()/(24*3600))
    if age_days < 1:
        return False, 'The issue date of passport is invalid'
    elif age_years(issue) > 5:
        return False, 'The passport is already expired'
    else:
        issue = issue

    #Assigning value to passport expire date    
    issue_date = datetime.datetime.strptime(issue, "%Y-%m-%d")
    year = str(issue_date.year + 5)
    month = str(issue_date.month)
    day = str(issue_date.day)
    date_ = year+'-'+month+'-'+day
    exp = datetime.datetime.strptime(date_, "%Y-%m-%d")

    return True, pass_no, issue, exp

def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

def pic(data):
    
    pic = base64.b64decode(data, 'pn')

    return pic
