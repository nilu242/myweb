from flask import Flask, render_template, request, redirect, jsonify


import psycopg2
import psycopg2.extras

app = Flask('Portfoli')   # Flask constructor  
  
# A decorator used to tell the application 
# which URL is associated function 
def get_db_connection():
    return psycopg2.connect(
        database="flask",
        user="postgres",
        password="admin",  # replace with your actual password
        host="localhost",
        port="5432"
    )


@app.route('/')       
def hello(): 
    return render_template('index.html')

@app.route('/about')
def about(): 
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')  

@app.route('/contact_list')
def contact_list():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, email, message, created_at FROM contacts ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('contact_list.html', contacts=rows)

@app.route('/update', methods=['POST'])
def update_contact():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET name=%s, email=%s, message=%s WHERE id=%s",
        (name, email, message, id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True})


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email'] 
    message = request.form['message']
      
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')


if __name__=='__main__': 
   app.run(debug=True) 
