from flask import Flask, render_template, request, send_file
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
import datetime
from functions import *
from email_sender import *



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://munira:trash@localhost:5432/flasky"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#This is the homepage
#Lists recently added employees, employers, brokers
@app.route("/", methods=['GET', 'POST'])
def index():
    employees = Employee.query.order_by(Employee.id).all()
    employers = Employer.query.filter(Employer.id != '1').order_by(Employer.id).all()
    brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()

    employees_ = []
    for employee in employees:
        if age_days(employee.register_date) <= 30:
            employees_.append(employee)
    
    brokers_ = []
    for broker in brokers:
        if broker.id != 999999:
            brokers_.append(broker)
    
    employers_ = []
    for employer in employers:
        if employer.id != 999999:
            employers_.append(employer)
    
    employee = Employee.query.get(27)

    return render_template("home.html", employees=employees_, employers=employers_, brokers=brokers_)

#Response for register navigation link
#returns registration form for employee registration
@app.route("/RegisterEmployee", methods=["POST", "GET"])
def addEmployee():
    message = ['', '' ,'' ,'', '', '', '', '', '', '', '']
    return render_template('RegisterEmployee.html', message=message)

#Validates and registers a new employee into database
@app.route('/RegisterEmployee/', methods=["POST"])
def register_employee():
    error = 1
    message = ['', '' ,'' ,'', '', '', '', '', '', '', '']
    #####Here starts the personal details data processing {
    #validating the name
    #######################################################
    raw_name = request.form.get("name")
    
    if name_validate(raw_name):
        name = name_validate(raw_name)
    else:
        error = 2
        message[0] = 'Invalid Name'
    #######################################################
    #validating contact format
    #######################################################
    contact = request.form.get("contact-no")

    if contact_validate(contact):
        contact = contact_validate(contact)
    else:
        message[1] = 'Invalid ER Phone No.'
        error = 2
    #######################################################    
    

    #validating address information
    address = request.form.get("address").capitalize()

    #validating salary information
    #######################################################
    salary = request.form.get("salary")
    if salary_validate(salary):
        val_salary = salary_validate(salary)
    else:
        error = 2
        message[3] = "Invalid salary amount"
    #######################################################
    #no need for validation     
    position = request.form.get("position").capitalize()
    
    #registration date = current date
    now = datetime.datetime.now()
    str_now = now.strftime("%Y/%m/%d")
    register_date = str_now
    
    #National ID validation
    #######################################################
    national_id = request.form.get('national_id')
    valid = nat_validate(national_id, 7)
    if valid:
        nat_id = valid
    else:
        error = 2
        message[5] = 'Invalid or pre-existing National ID#'
    #######################################################
    #####}here ends the personal details data processing

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++#
    #######################################################
    #fetch grid image of client from registration page

    image = request.files['grid']
    data = image.read()
    rendered_data = render_picture(data)

    portrait = request.files['portrait']
    datap = portrait.read()
    rendered_datap = render_picture(datap)

    passpic = request.files['pass-pic']
    datas = passpic.read()
    rendered_datas = render_picture(datas)

    pass_no = request.form.get('pass-no')
    issue_place = request.form.get('pass-issue-place')
    issue_date = request.form.get('pass-issue-date')
    try:
        pass_valid, err = passport_validate(pass_no, issue_date)
    except:
        pass_valid, pass_num, issue_date, expire_date = passport_validate(pass_no, issue_date)
    if pass_valid:
        if len(datas) == 0:
            error = 2
            message[4] = 'Please add snapshot of passport'
    elif not pass_valid and not err:
        pass
    else:
        error = 2
        message[4] = err
    

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++#

    

    #####here starts the additional details data processing{
    #no need for validation
    religion = request.form.get("religion")

    #validating place of birth
    pob = request.form.get("pob").capitalize()

    #validating date of birth
    #######################################################
    dob = request.form.get("dob")
    b_date = datetime.datetime.strptime(dob, "%Y-%m-%d")

    if (age_years(dob) > 20) and (age_years(dob) < 45):
        val_dob = b_date
    else:
        error = 3
        message[6] = 'This person can\'t be accepted'
    #######################################################
    no_child = request.form.get("no-child")
    status = request.form.get("status")
    gender = request.form.get("gender")
    education = request.form.get("education")
    
    #####}here ends the additional data processing

    if error == 2:
        return render_template('RegisterEmployee.html', message=message)
    elif error == 3:
        return render_template('success.html', dob=message[6])
    
    employee = Employee(name=name, national_id=nat_id, contact=contact, address=address, salary=val_salary, position=position,register_date=register_date, religion=religion, pob=pob, dob=val_dob, no_of_child=no_child, status=status, gender=gender, education=education, employer_id=1, broker_id=1, sent_1=False, sent_2=False, languages=None, pport=False)

    db.session.add(employee)
    db.session.commit()
    try:
        employee.add_passport(pass_num, issue_place, issue_date, expire_date)
    except:
        pass
    try:
        employee.add_grid(data, rendered_data)
    except:
        pass
    try:
        employee.add_portrait(datap, rendered_datap)
    except:
        pass
    try:
        employee.add_passpic(datas, rendered_datas)
    except:
        pass

    

    return render_template("success.html", dob=dob)

#fetches the employee list from database and return it to page
#supports 'delete', 'add employer', 'add broker', 'edit profile' oprations
#The passportless employees support operation 'add passport' and 'edit profile'
#It also has search input to valid search argument and get results
@app.route('/home/list employees', methods=["POST", "GET"])
def list_employees():
    search = request.form.get("search")
    
    if (search != None) and (len(search) != 0) :
        
        if (len(search.split()) != 0) :
            message = ''
            employees = get_employee_sresult(search)
    elif search == None:
        employees = Employee.query.order_by(Employee.id).all()
    
        message = ''       

    else:
            
        employees = Employee.query.order_by(Employee.id).all()
    
        message = 'please type in valid searches!'
        
    return render_template('list.html',message=message, completelist=employees)        


#Returns a list of employers to link them with the specific employee
@app.route('/Register Employer/<int:employer_id>/<int:employee_id>/<int:new>/<int:location>/link', methods=["GET"])
def add_employer_list(employer_id, employee_id, new, location):
    
    employee = Employee.query.get(employee_id)
    message = ''

    
    if new == 2:
        try:
            return render_template('RegisterEmployer.html',message=message, employee=employee, location=location)
        except:
            return index()
    else:
        employer = Employer.query.get(employer_id)
        try:
            employer.add_employee(employee_id)
        except:
            pass
    
    if location == 1:
        return index()
    elif location == 2:
        return list_employees()
    else:
        return employee_details(employee_id)

#Returns a list of brokers to link them with the specific employee
@app.route('/Register Broker/<int:broker_id>/<int:employee_id>/<int:new>/<int:location>/link', methods=["GET"])
def add_broker_list(broker_id, employee_id, new, location):
    
    employee = Employee.query.get(employee_id)
    message = ''
    if new == 2:
        try:
            return render_template('RegisterBroker.html',message=message, employee=employee, location=location)
        except:
            return index()
    else:
        broker = Broker.query.get(broker_id)
        try:
            broker.add_employee(employee_id)
        except:
            pass    
    if location == 2:
        return list_employees()         
    elif location == 1:
        return index()
    else:
        return employee_details(employee_id)

#deletes employee specified by employee_id var from the database
@app.route("/home/list employees/<int:employee_id>", methods=["GET"])
def employee_remove(employee_id):
    if employee_id == None:
        employees = Employee.query.order_by(Employee.id).all()
        message = ''

        try:
            return render_template('list.html', completelist=employees, message=message)
        except:
            return index()    
    else:
        message = ''
        employee = Employee.query.get(employee_id)
        try:
            if employee != None:
                passport = Passport.query.filter(Passport.employee_id == employee.id).first()
                if passport != None:
                    db.session.delete(passport)
                db.session.delete(employee)
                db.session.commit()
        except:
            pass        

        employees = Employee.query.order_by(Employee.id).all()
        return render_template('list.html', completelist=employees, message=message)

#This action returns the form to update employee details in database
@app.route('/Modify Employee Details/<int:location>/<int:employee_id>', methods=["Get"])
def modify_employee(employee_id, location):
    employee = Employee.query.get(employee_id)
    message = ['','','','','','','']
    try:
        return render_template('ModifyEmployeeForm.html', employee=employee, location=location, message=message)
    except:
        raise
#Edit employee detail of a specific employee by first validating the forms
@app.route('/Modify Employee Details/<int:location>/<int:employee_id>/info', methods=["POST"])
def modify_employee_form(employee_id, location):
    employee = Employee.query.get(employee_id)
    raw_name = request.form.get("name")
    message = ['','','','','','','','']
    error = 1
    if name_validate(raw_name):
        employee.name = name_validate(raw_name)
    elif raw_name == '':
        employee.name = employee.name
    else:
        error = 2
        message[0] = 'Invalid Name'


    contact = request.form.get("contact-no")
    if contact_validate(contact):
        employee.contact = contact_validate(contact)
    elif contact == '':
        employee.contact = employee.contact
    else:
        error = 2
        message[1] = 'Invalid Contact#'
    
    address = request.form.get("address")
    if address != '':
        employee.address = address.capitalize()
    
    salary = request.form.get("salary")
    if salary_validate(salary):
        employee.salary = salary_validate(salary)
    elif salary == '':
        employee.salary = employee.salary
    else:
        error = 2
        message[3] = 'Invalid Salary Amount'
    
    position = request.form.get("position")
    if (position != None) and (len(position) != 0):
        employee.position = position.capitalize()

    #register_date = date
    
    religion = request.form.get("religion")
    if (religion != None ) and (len(religion) != 0):
        employee.religion = religion.capitalize()
    
    pob = request.form.get("pob")
    if (pob != None) and (len(pob) != 0):
        employee.pob = pob.capitalize()

    dob = request.form.get("dob")
    if len(dob) != 0 and dob_validate(dob):
        employee.dob = dob_validate(dob)
    elif dob == '' or dob == None:
        employee.dob = employee.dob
    else:
        error = 2
        message[6] = 'Invalid Birth Date'

    no_child = request.form.get("no-child")
    if (no_child != None) and (no_child != ''):
        if int(no_child) < 0 or int(no_child) > 7:
            error = 2
            message[7] = 'Unacceptable Number of Children'
        else:
            employee.no_of_child = no_child

    status = request.form.get("status")
    if (status != None) and (len(status) != 0):
        employee.status = status

    gender = request.form.get("gender")
    if (gender != None) and (len(gender) != 0):
        employee.gender = gender

    education = request.form.get("education")
    if (education != None) and (len(education) != 0):
        employee.education = education

    image = request.files['grid']
    data = image.read()
    if len(data) != 0:
        rendered_data = render_picture(data)
    
        grid = GridContent.query.filter_by(employee_id=employee.id).first()
        grid.data = data
        grid.rendered_data = rendered_data
    
    portrait = request.files['portrait']
    datap = portrait.read()
    if len(datap) != 0:
        rendered_datap = render_picture(datap)

        portrait = Portrait.query.filter_by(employee_id=employee.id).first()
        portrait.data = datap
        portrait.rendered_data = rendered_datap
        
    employees = Employee.query.order_by(Employee.id).all()
    
    db.session.commit()
    if error == 1:
        if location == 2:
            return list_employees()
        elif location == 1:
            return index()
        else:
            return employee_details(employee_id)
    else:
        return render_template('ModifyEmployeeForm.html', employee=employee, location=location, message=message)
    
#request to link or add employer to a specific employee
#Returns either list of employers to choose from, or registers a new employer
@app.route("/Register Employer/<int:location>/<int:employee_id>", methods=["GET", "POST"])
def addEmployer(employee_id, location):
    employers = Employer.query.filter(Employer.id != '1').order_by(Employer.id).all()
    employee = Employee.query.get(employee_id)
    employers_ = []
    ###
    search = request.form.get("search")
    
    if (search != None) and (len(search) != 0) :
        
        if (len(search.split()) != 0) :
            search_error = ''
            employers_ = get_employer_sresult(search)
            if len(employers_) == 0:
                employers_ = Employer.query.filter(Employer.id == '1').all()
            #employers = get_employer_sresult(search)
            #brokers = get_broker_sresult(search)
            employer_id = employee.employer_id
            employer = Employer.query.get(employer_id)
    elif search == None:
        employers = Employer.query.filter(Employer.id != '1').order_by(Employer.id).all()
        employers_ = []
        for employer in employers:
            if employer.id != 999999:
                employers_.append(employer)
    
        search_error = ''       
        employer_id = employee.employer_id
        employer = Employer.query.get(employer_id)
    else:
        search_error = 'please type in valid searches!'
        employers = Employer.query.filter(Employer.id != '1').order_by(Employer.id).all()
        

    ###
        try:
            employers_ = []
            for employer in employers:
                if (employer.id != employee.employer_id) or (employer.id != 999999):
                    employers_.append(employer)
    

            employer_id = employee.employer_id
            employer = Employer.query.get(employer_id)
        except:
            raise

    message = ['','']

    if len(employers_) == 0:
        try:
            return render_template('RegisterEmployer.html', employee=employee, message=message, location=location)
        except:
            return index()
    try:        
        return render_template('addemployerlist.html', employers=employers_, employee=employee, employer=employer, location=location)
    except:
        raise

#fetches employers from database and lists them in page
#It delete and modify operations
@app.route('/home/list employers', methods=["POST", "GET"])
def list_employers():
    search = request.form.get("search")
    
    if (search != None) and (len(search) != 0) :
        
        if (len(search.split()) != 0) :
            message = ''
            employers_ = get_employer_sresult(search)
            #employers = get_employer_sresult(search)
            #brokers = get_broker_sresult(search)
            
    elif search == None:
        employers = Employer.query.filter(Employer.id != '1').order_by(Employer.id).all()
        employers_ = []
        for employer in employers:
            if employer.id != 999999:
                employers_.append(employer)
    
        message = ''       

    else:
        message = 'please type in valid searches!'
        employers = Employer.query.filter(Employer.id != '1').order_by(Employer.id).all()
        
        employers_ = []
        for employer in employers:
            if employer.id != 999999:
                employers_.append(employer)

        
    return render_template('ListEmployer.html',message=message, employers=employers_)

#registers a new employer and links it with the specified employee
@app.route("/Register Employer/<int:location>/<int:employee_id>/info", methods=["POST"])
def register_employer(employee_id, location):
    employee = Employee.query.get(employee_id)
    
    raw_name = request.form.get("name")
    message = ['','']
    if name_validate(raw_name):
        name = name_validate(raw_name)
    else:
        message0 = 'Please write First, Middle and Last name correctly!'
        message[0] = message0
        try:
            return render_template('RegisterEmployer.html', message=message, employee=employee)
        except:
            return index()
    
    
    national_id = request.form.get('national_id')
    
    if nat_validate(national_id, 10):
        national_id = national_id
    else:
        message[1] = "Please enter a valid National ID#"
        return render_template('RegisterEmployer.html', message=message, employee=employee, location=location)
    #checking if submitted employer already exists
    employ = Employer.query.filter_by(national_id=str(national_id)).first()
    if employ == None:
        try:
            register_date = datetime.datetime.now()
            employer = Employer(name=name, national_id=national_id, register_date=register_date)
            db.session.add(employer)
            db.session.commit()
            employer = Employer.query.filter_by(national_id=str(national_id)).first()
            employer.add_employee(employee_id)
        except:
            message[1] = 'Please enter a valid National ID#'
            try:
                return render_template('RegisterEmployer.html', message=message, employee=employee)
            except:
                return index()
    else:
        message[1] = 'Please enter a unique National ID#'
        try:
            return render_template('RegisterEmployer.html', message=message, employee=employee, location=location)
        except:
            return index()
    
    
    
    if location == 1:
        return index()
    elif location == 2:
        return list_employees()
    else:
        return employee_details(employee_id)


#deletes employer specified by employer_id var from the database
@app.route("/home/list employers/<int:employer_id>/<int:location>/", methods=["GET"])
def employer_remove(employer_id, location):
    if employer_id == None:
        employers = Employer.query.filter(Employer.id != '1').order_by(Employer.id).all()
        employers_ = []
        for employer in employers:
            if employer.id != 999999:
                employers_.append(employer)

        return render_template('ListEmployer.html', employers=employers_)
    else:

        employer = Employer.query.get(employer_id)
        try:
            if employer != None:
                db.session.delete(employer)
                db.session.commit()
        except:
            pass

        if location == 2:
            return list_employers()
        elif location == 1:
            return index()
        else:
            return employer_details(employer_id, location)
#This action returns the form to update employer details in database
@app.route('/Modify Employer Details/<int:location>/<int:employer_id>', methods=["GET"])
def modify_employer(employer_id, location):
    message = ['','']
    employer = Employer.query.get(employer_id)
    employees = Employee.query.filter_by(employer_id=employer_id).all()
    
    try:
        return render_template('ModifyEmployerForm.html',message=message, employer=employer, employees=employees, location=location)

    except:
        raise

#Edit employer detail of a specific employer by first validating the forms
@app.route('/Modify Employer Form/<int:employer_id>/<int:location>info', methods=["POST"])
def modify_employer_form(employer_id, location):
    employer = Employer.query.get(employer_id)
    employees = Employee.query.filter_by(employer_id=employer_id).all()
    error = False
    message = ['','']

    raw_name = request.form.get("name")

    if (raw_name != None) and (len(raw_name) != 0):
        split_name = raw_name.split()

        if len(split_name) != 3:
            message[0] = 'Please write First, Middle and Last name correctly!'
            error = True
            
        else:    
            f_name = split_name[0].capitalize()
            m_name = split_name[1].capitalize()
            l_name = split_name[2].capitalize()
    
            name = (f_name+' '+m_name+' '+l_name)
        
    else:
        name = employer.name
        

    national_id = request.form.get('national_id')
    if national_id == None or len(national_id) == 0:
        national_id = employer.national_id
    else:    
        try:
            national_id = int(national_id)
        except ValueError:
            message1 = 'Please enter a valid and unique National ID#'
            message[1] = message1
            error = True
        
    if error :
        try:
            return render_template('ModifyEmployerForm.html', message=message, employer=employer, employees=employees, location=location)
        except:
            return index()    
    employer.name = name
    employer.national_id = national_id
    db.session.commit()
    if location == 1:
        return index()
    elif location == 2:
        return list_employers()
    else:
        return employer_details(employer_id, location)
    

#This action url sets the employer id column of the specified employee to None
#In other words it unlinks the employees from the employer

@app.route('/Modify Employer Employee Details/<int:employer_id>/<int:employee_id>/<int:location>', methods=["GET"])
def employee_unlink(employer_id, employee_id, location):
    message = ['','']
    employee = Employee.query.get(employee_id)
    try:
        employee.employer_id = 1
    
        db.session.commit()
    
        employer = Employer.query.get(employer_id)
        employees = Employee.query.filter_by(employer_id=employer_id).all()
    except:
        pass
    try:
        return render_template('ModifyEmployerForm.html',message=message, employer=employer, employees=employees, location=location)
    except:
        raise


#request to link or add broker to a specific employee
#Returns either list of brokers to choose from, or registers a new broker
@app.route("/Register Broker/<int:location>/<int:employee_id>", methods=["GET", "POST"])
def addBroker(employee_id, location):
    brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()
    employee = Employee.query.get(employee_id)
    ###
    search = request.form.get("search")
    
    if (search != None) and (len(search) != 0) :
        
        if (len(search.split()) != 0) :
            search_error = ''
            brokers_ = get_broker_sresult(search)
            if len(brokers_) == 0:
                brokers_ = Broker.query.filter(Broker.id == '1').all()
            #employers = get_employer_sresult(search)
            #brokers = get_broker_sresult(search)
            broker_id = employee.broker_id
            broker = Broker.query.get(broker_id)
    elif search == None:
        brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()
        brokers_ = []
        for broker in brokers:
            if broker.id != 999999:
                brokers_.append(broker)
    
        search_error = ''       
        broker_id = employee.broker_id
        broker = Broker.query.get(broker_id)
    else:
        search_error = 'please type in valid searches!'
        brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()
    ###
        try:
            brokers_ = []
            for broker in brokers:
                if (broker.id != employee.broker_id) or (broker.id != 999999):
                    brokers_.append(broker)
    

            broker_id = employee.broker_id
            broker = Broker.query.get(broker_id)
        except:
            raise

    
    message = ['','']

    if len(brokers_) == 0:
        try:
            return render_template('RegisterBroker.html', employee=employee, message=message, location=location)
        except:
            return index()
    try:
        return render_template('addbrokerlist.html', brokers=brokers_, employee=employee, broker=broker, location=location)
    except:
        return index()
#registers a new broker and links it with the specified employee
@app.route("/Register Broker/<int:location>/<int:employee_id>/info", methods=["POST"])
def register_broker(employee_id, location):
    employee = Employee.query.get(employee_id)
    error = False
    raw_name = request.form.get("name")
    split_name = raw_name.split()

    message = ['','']

    if len(split_name) != 3:
        message[0] = 'Please write First, Middle and Last name correctly!'
        error = True
    else:
        f_name = split_name[0].capitalize()
        m_name = split_name[1].capitalize()
        l_name = split_name[2].capitalize()
        name = (f_name+' '+m_name+' '+l_name)
    
    national_id = request.form.get('national_id')
    contact = request.form.get('contact')
    try:
        national_id = int(national_id)
        if len(str(national_id)) != 10:
            message[1] = 'Please enter a valid and unique National ID#'
            error = True
    except ValueError:
        message1 = 'Please enter a valid and unique National ID#'
        message[1] = message1
        error = True

    #checking if the broker already exists
    
    
    brokr = Broker.query.filter_by(national_id=str(national_id)).first()
    if (brokr == None) and (error == False) :
        register_date = datetime.datetime.now()
        broker = Broker(name=name, contact=contact, national_id=national_id, register_date=register_date)
        db.session.add(broker)
        db.session.commit()
        broker = Broker.query.filter_by(national_id=str(national_id)).first()
    else:
        broker = brokr
        message[1] = 'Please enter a valid and unique National ID#'
        error = True
    
    if error == False :
        broker = Broker.query.filter_by(national_id=str(national_id)).first()
        try:
            broker.add_employee(employee_id)
        except:
            pass
    #only for listing the employees to the page
    employees = Employee.query.order_by(Employee.id).all()

    if error:
        try:
            return render_template('RegisterBroker.html', message=message, employee=employee, location=location)
        except:
            return index()    
    if location == 2:
        return render_template('list.html', completelist=employees)           
    elif location == 1:
        return index()
    else:
        return employee_details(employee.id)

#fetches brokers from database and lists them in page
#It supports delete and modify operations
@app.route('/home/list brokers', methods=["POST", "GET"])
def list_brokers():
    search = request.form.get("search")
    
    if (search != None) and (len(search) != 0) :
        
        if (len(search.split()) != 0) :
            message = ''
            brokers_ = get_broker_sresult(search)
            #employers = get_employer_sresult(search)
            #brokers = get_broker_sresult(search)
            
    elif search == None:
        brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()
        brokers_ = []
        for broker in brokers:
            if broker.id != 999999:
                brokers_.append(broker)
    
        message = ''

    else:
        message = 'please type in valid searches!'
        brokers_ = []
        brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()
        for broker in brokers:
            if broker.id != 999999:
                brokers_.append(broker)

        
    return render_template('ListBroker.html',message=message, brokers=brokers_)

#deletes broker specified by broker_id var from the database
@app.route("/home/list brokers/<int:broker_id>", methods=["GET"])
def broker_remove(broker_id):
    if broker_id == None:
        brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()

        brokers_ = []
        for broker in brokers:
            if broker.id != 999999:
                brokers_.append(brokers)

        return render_template('listBroker.html', brokers=brokers_)
    else:

        broker = Broker.query.get(broker_id)
        try:
            if broker != None:
                db.session.delete(broker)
                db.session.commit()
        except:
            pass
        brokers = Broker.query.filter(Broker.id != '1').order_by(Broker.id).all()

        brokers_ = []
        for broker in brokers:
            if broker.id != 999999:
                brokers_.append(broker)
    
        return render_template('ListBroker.html', brokers=brokers_)        

#This action returns the form to update broker details in database
@app.route('/Modify Broker Details/<int:location>/<int:broker_id>', methods=["GET"])
def modify_broker(broker_id, location):
    message = ['','']
    broker = Broker.query.get(broker_id)
    employees = Employee.query.filter_by(broker_id=broker_id).all()
    try:
        return render_template('ModifyBrokerForm.html',message=message, broker=broker, employees=employees,location=location)
    except:
        raise
#Edit broker detail of a specific broker by first validating the forms
@app.route('/Modify Broker Form/<int:location>/<int:broker_id>/info', methods=["POST"])
def modify_broker_form(broker_id, location):
    broker = Broker.query.get(broker_id)
    employees = Employee.query.filter_by(broker_id=broker_id).all()
    error = False

    message = ['','']

    raw_name = request.form.get("name")

    if (raw_name != None) and (len(raw_name) != 0):
        split_name = raw_name.split()

        if len(split_name) != 3:
            message[0] = 'Please write First, Middle and Last name correctly!'
            error = True
            
        else:    
            f_name = split_name[0].capitalize()
            m_name = split_name[1].capitalize()
            l_name = split_name[2].capitalize()
    
            name = (f_name+' '+m_name+' '+l_name)
        
    else:
        name = broker.name
        

    national_id = request.form.get('national_id')
    if national_id == None or len(national_id) == 0:
        national_id = broker.national_id
    else:    
        
        if len(national_id) != 10:
            message[1] = "Please enter a valid and unique National ID#"
            error = True
        else:
            try:
                national_id = int(national_id)
            except ValueError:
                message1 = 'Please enter a valid and unique National ID#'
                message[1] = message1
                error = True    
    
    
    
    contact = request.form.get('contact')
    if (contact == None) and (len(contact) == 0):
        contact = broker.contact
    else:
            contact = contact

    if error :
        try:
            return render_template('ModifyBrokerForm.html', message=message, broker=broker, employees=employees)
        except:
            return index()    
    broker.name = name
    broker.national_id = national_id
    broker.contact = contact
    
    db.session.commit()

    if location == 2:
        return list_brokers()
    elif location == 2:
        return index()
    else:
        return broker_details(broker_id, location)
    

#This action url sets the broker id column of the specified employee to None
#In other words it unlinks the employees from the broker
@app.route('/Modify Brokers Details/<int:broker_id>/<int:employee_id>/<int:location>', methods=["GET"])
def employee_broker_unlink(broker_id, employee_id, location):
    message = ['','']
    employee = Employee.query.get(employee_id)
    try:
        employee.broker_id = 1
    
        db.session.commit()
    except:
        pass
    broker = Broker.query.get(broker_id)
    employees = Employee.query.filter_by(broker_id=broker_id).all()

    try:
        return render_template('ModifyBrokerForm.html',message=message, broker=broker, employees=employees, location=location)
    except:
        return index()


@app.route('/Emails/<int:location>/<int:employee_id>', methods=["GET"])
def send_mail(employee_id, location):
    employee = Employee.query.get(employee_id)
    labour = "eritreanlabouroffice@gmail.com"
    Kuwait = "kuwaitreqruitment@gmail.com"
    Saudi = "saudireqruitment@gmail.com"
    
    if employee.pport:
        if not employee.sent_1:
            send_gmail(labour, employee)
            
        elif not employee.sent_2:
            country = employee.country_of_work
            if country == "Kuwait":
                send_gmail('munirasaid1979@gmail.com', employee)
            elif country == "Saudi":
                send_gmail(Saudi, employee)
            
    if location == 2:
        return list_employees()
    elif location == 1:
        return index()
    else:
        return employee_details(employee_id)

@app.route("/Add passport/<int:employee_id>/<int:location>", methods=["GET"])
def add_passport(employee_id, location):
    employee = Employee.query.get(employee_id)
    message = ''
    try:
        return render_template("RegisterPassport.html",message=message, employee=employee, location=location)
    except:
        raise
@app.route("/Register Passport Details/<int:employee_id>/<int:location>", methods=["POST", "GET"])
def register_passport(employee_id, location):
    employee = Employee.query.get(employee_id)
    error = 1
    

    pass_no = request.form.get('pass-no')
    issue_place = request.form.get('pass-issue-place')
    issue_date = request.form.get('pass-issue-date')
    try:
        pass_valid, err = passport_validate(pass_no, issue_date)
    except:
        pass_valid, pass_num, issue_date, expire_date = passport_validate(pass_no, issue_date)
    if pass_valid:
        pass
    elif not pass_valid and not err:
        pass
    else:
        error = 2
        message = err

    passpic = request.files['pass-pic']
    datas = passpic.read()
    rendered_datas = render_picture(datas)

    if error == 2:
        try:
            return render_template("RegisterPassport.html",message=message, employee=employee, location=location)
        except:
            return index()    
    else:
        employee.add_passport(pass_no, issue_place, issue_date, expire_date)
        try:
            employee.add_passpic(datas, rendered_datas)
        except:
            pass
        if location == 1:
             return index()
        elif location == 2:
            return list_employees()
        else:
            return employee_details(employee_id)

@app.route('/EmployeeDetails/<int:employee_id>/', methods=["GET"])
def employee_details(employee_id):
    employee = Employee.query.get(employee_id)
    
    first = 1
    last = 1
    employees1 = Employee.query.filter(Employee.id < employee_id).all()
    if employees1:
        first = 0
    employees2 = Employee.query.filter(Employee.id > employee_id).all()
    if employees2:
        last = 0
        
    age = int(age_years(employee.dob))
    passport = Passport.query.filter(Passport.employee_id==employee.id).first()
    grid = GridContent.query.filter(GridContent.employee_id==employee.id).first()
    employer = Employer.query.get(employee.employer_id)
    broker = Broker.query.get(employee.broker_id)
    image = grid.data
    img = pic(image)
    try:
        return render_template('EmployeeDetails.html', employee=employee, passport=passport, age=age, image=img, employer=employer, broker=broker, first=first, last=last)
    except:
        raise

@app.route('/PreviousEmployee/<int:employee_id>/', methods=['GET'])
def prev_employee(employee_id):
    employee_id = employee_id - 1
    return employee_details(employee_id)
@app.route('/NextEmployee/<int:employee_id>/', methods=['GET'])
def next_employee(employee_id):
    employee_id = employee_id + 1
    return employee_details(employee_id)
    
            

@app.route('/EmployerDetails/<int:employer_id>/<int:location>', methods=["GET"])
def employer_details(employer_id, location):
    employer = Employer.query.get(employer_id)
    employees = Employee.query.filter(Employee.employer_id==employer_id).all()

    employees1 = Employer.query.filter((Employer.id < employer_id) & (Employer.id != 1)).all()
    if employees1:
        first = 0
    else:
        first = 1
    employees2 = Employer.query.filter((Employer.id > employer_id) & (Employer.id != 999999) ).all()
    if employees2:
        last = 0
    else:
        last = 1

    try:
        return render_template('EmployerDetails.html', employer=employer, employees=employees, location=location, first=first, last=last)
    except:
        raise

@app.route('/NextEmployer/<int:employer_id>/<int:location>', methods=['GET'])
def next_employer(employer_id, location):
    employer_id = employer_id + 1
    return employer_details(employer_id, location)

@app.route('/PreviousEmployer/<int:employer_id>/<int:location>', methods=['GET'])
def prev_employer(employer_id, location):
    employer_id = employer_id - 1
    return employer_details(employer_id, location)

@app.route('/BrokerDetails/<int:broker_id>/<int:location>', methods=["GET"])
def broker_details(broker_id, location):
    broker = Broker.query.get(broker_id)
    employees = Employee.query.filter(Employee.broker_id==broker_id).all()

    employees1 = Broker.query.filter((Broker.id < broker_id) & (Broker.id != 1)).all()
    if employees1:
        first = 0
    else:
        first = 1
    employees2 = Broker.query.filter((Broker.id > broker_id) & (Broker.id != 999999) ).all()
    if employees2:
        last = 0
    else:
        last = 1

    try:
        return render_template('BrokerDetails.html', broker=broker, employees=employees, location=location, first=first, last=last)
    except:
        raise

@app.route('/NextBroker/<int:broker_id>/<int:location>', methods=['GET'])
def next_broker(broker_id, location):
    broker_id = broker_id + 1
    return broker_details(broker_id, location)

@app.route('/PreviousBroker/<int:broker_id>/<int:location>', methods=['GET'])
def prev_broker(broker_id, location):
    broker_id = broker_id - 1
    return broker_details(broker_id, location)

@app.route('/event/<int:employee_id>/logo')
def event_grid(employee_id):
    event = GridContent.query.filter(GridContent.employee_id==employee_id).first()
    return app.response_class(event.data, mimetype='application/octet-stream')

@app.route('/event/<int:employee_id>/portrait')
def event_portrait(employee_id):
    event = Portrait.query.filter(Portrait.employee_id==employee_id).first()
    return app.response_class(event.data, mimetype='application/octet-stream')

@app.route('/event/<int:employee_id>/passpic')
def event_passpic(employee_id):
    event = Passpic.query.filter(Passpic.employee_id==employee_id).first()
    return app.response_class(event.data, mimetype='application/octet-stream')
