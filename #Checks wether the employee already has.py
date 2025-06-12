#Checks wether the employee already has broker linked and confirms overright of broker
@app.route('/Register Broker/<int:broker_id>/<int:employee_id>/<int:location>/confirm', methods=["GET"])
def confirm_broker_overright(broker_id, employee_id, location):
    new = 1
    employee = Employee.query.get(employee_id)
    cur_broker_id = employee.broker_id
    if int(cur_broker_id) == 999999:
        cur_broker_id = '1'
    
    cur_broker = Broker.query.get(cur_broker_id)

    if (int(broker_id) != 999999):
        broker = Broker.query.get(broker_id)
    else:
        broker = Broker.query.get('1')
        new = 2
    try:    
        return render_template('confirmbroker.html', broker=broker, employee=employee, new=new, cur_broker=cur_broker, location=location)

#Checks wether the employee already has employer linked and confirms overright of employer
@app.route('/Register Employer/<int:employer_id>/<int:employee_id>/<int:location>/confirm', methods=["GET"])
def confirm_employer_overright(employer_id, employee_id, location):
    new = 1
    employee = Employee.query.get(employee_id)
    cur_employer_id = employee.employer_id
    if int(cur_employer_id) == 999999:
        cur_employer_id = '1'
    
    cur_employer = Employer.query.get(cur_employer_id)

    if (int(employer_id) != 999999):
        employer = Employer.query.get(employer_id)
    else:
        employer = Employer.query.get('1')
        new = 2
    try:
        return render_template('confirmemployer.html', employer=employer, employee=employee, new=new, cur_employer=cur_employer, location=location)
    except:
        return index()



function createIncomeTracker() {
            let income = 0;
            return {
                addIncome(amount) {
                    income += amount;
                },
                getIncome() {
                    return income;
                }
            };
        }
        const incomeTracker = createIncomeTracker();
        console.log(incomeTracker.getIncome());
        incomeTracker.addIncome(5000);
        console.log(incomeTracker.getIncome());


@app.route('/Modify Employer Details/<int:employer_id>/<int:employee_id>', methods=["GET"])
def employee_unlink(employer_id, employee_id):
    message = ['','']
    employee = Employee.query.get(employee_id)
    try:
        employee.employer_id = None
    
        db.session.commit()
    
        employer = Employer.query.get(employer_id)
        employees = Employee.query.filter_by(employer_id=employer_id).all()
    except:
        pass
    try:
        return render_template('ModifyEmployerForm.html',message=message, employer=employer, employees=employees)
    except:
        return index()

@app.route('/Modify Broker Details/<int:broker_id>/<int:employee_id>', methods=["GET"])
def employee_broker_unlink(broker_id, employee_id):
    message = ['','']
    employee = Employee.query.get(employee_id)
    try:
        employee.broker_id = None
    
        db.session.commit()
    except:
        pass
    broker = Broker.query.get(broker_id)
    employees = Employee.query.filter_by(broker_id=broker_id).all()

    try:
        return render_template('ModifyBrokerForm.html',message=message, broker=broker, employees=employees)
    except:
        return index()


