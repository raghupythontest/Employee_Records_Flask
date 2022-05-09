from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)



#Create Table
class Employee(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(100), unique=True, nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    gender= db.Column(db.String(10), nullable=False)
    salary=db.Column(db.Float, nullable=False)
    location=db.Column(db.String(100), nullable=False)

db.create_all()


@app.route("/")
def home():
    all_employees = db.session.query(Employee).all()
    print(all_employees)
    return render_template("index.html",employees=all_employees)

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method=="POST":
        data=request.form
        new_emp = Employee(firstname=data["firstname"],lastname=data["lastname"],gender=data["gender"],salary=data["salary"],location=data["location"])
        db.session.add(new_emp)
        db.session.commit()
        print("Record added")
        # firstname=data["firstname"]
        # last_name=data["lastname"]
        # gender=data["gender"]
        # salary=data["salary"]
        # location=data["location"]
        # print(firstname,last_name,gender,salary,location)
        return redirect(url_for("home"))

    return render_template("add.html")
@app.route("/edit",methods=['GET','POST'])
def edit():
    if request.method=="POST":
        data = request.form
        employee_id=request.form["id"]
        print("ID:",employee_id)
        firstname = request.form["firstname"]
        last_name=request.form["lastname"]
        gender=request.form["gender"]
        salary=request.form["salary"]
        location=request.form["location"]
        print(employee_id,firstname,last_name,gender,location,salary)
        employee_update = Employee.query.get(employee_id)
        employee_update.firstname=firstname
        employee_update.lastname =last_name
        employee_update.gender =gender
        employee_update.salary =salary
        employee_update.location=location
        db.session.commit()
        print("Update successful")
        return redirect(url_for("home"))
    #getting id from index.html and sending it to edit.html
    emp_id=request.args.get('id')
    employee_record=Employee.query.get(emp_id)
    return render_template("edit.html",emp_record=employee_record)

@app.route("/delete")
def delete():
    id=request.args.get("id")
    employee_to_be_deleted=Employee.query.get(id)
    db.session.delete(employee_to_be_deleted)
    db.session.commit()
    return redirect(url_for("home"))
if __name__=="__main__":
    app.run(debug=True)