from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "flash message"

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudmodel'

mysql = MySQL(app)




@app.route('/')
def index():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM crudmodel.students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students = data)


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        flash('Data Inserted Successfully')
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)', (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/update', methods = ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']


        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students
        SET name=%s, email=%s, phone=%s
        WHERE id=%s
        
        """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods = ['POST', 'GET'])
def delete(id_data):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (id_data))
    flash("Data Deleted Successfully")
    mysql.connection.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)