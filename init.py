#sudo service apache2 restart
import sys
import os
from flask import Flask, render_template,request, jsonify,redirect,url_for,jsonify,flash
import mysql.connector as mysql
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime
import glob, os
import json
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = open("/var/www/html/password.txt", "r").read(),
    database = "fandommap"
)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)
@app.route('/')
def index():
    cursor = db.cursor(buffered=True)
    cursor.execute('SELECT id,name,author,date FROM maps WHERE visibility="Public"')
    temp=''
    for row in cursor.fetchall():
        cursor.execute('SELECT view FROM views WHERE id="'+row[0]+'";')
        view=cursor.fetchone()
        if view is None:temp+='列列'.join(row)+'行行'
        else:temp+='列列'.join(row)+'列列'+str(view[0])+'行行'
    cursor.close()
    return render_template('index.html',result=temp)
@app.route('/profile')
def profile():
    cursor = db.cursor(buffered=True)
    cursor.execute('SELECT id,name,author,date,sortable,visibility FROM maps')
    temp=''
    for row in cursor.fetchall():
        cursor.execute('SELECT view FROM views WHERE id="'+row[0]+'";')
        view=cursor.fetchone()
        if view is None:temp+='列列'.join(row)+'行行'
        else:temp+='列列'.join(row)+'列列'+str(view[0])+'行行'
    cursor.close()
    return render_template('profile.html',result=temp)
@app.route('/$temp')
def temp():
    return render_template('temp.html')
@app.route('/$tsp')
def tsp():
    return render_template('tsp.html')
@app.route('/$fetch',methods=['POST'])
def fetch():
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM maps WHERE id='"+id+"';")
    temp=cursor.fetchall() 
    cursor.close()
    return jsonify({'fetch':temp})
@app.route('/$create',methods=['POST'])
def create():
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM counter;")
    counter=cursor.fetchone()[0]
    counter=counter+1
    cursor.execute('UPDATE counter SET count='+str(counter))
    cursor.execute("""INSERT INTO maps (id,name,email,author,poi,sortable,visibility,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
    ,(str(counter),request.form['name']+"'s Map",request.form['email'],request.form['name'],'{}','','Public',str(datetime.now().strftime('%d/%m/%Y'))))
    db.commit()
    cursor.close()
    return jsonify({'result':counter})
@app.route('/<id>')
def maps(id):
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM maps WHERE id='"+id+"';")
    result=cursor.fetchone()
    cursor.close()
    if result is None:
        cursor = db.cursor(buffered=True)
        cursor.execute('SELECT id,name,author,date FROM maps WHERE visibility="Public"')
        temp=''
        for row in cursor.fetchall():
            temp+='列列'.join(row)+'行行'
        cursor.close()
        return render_template('index.html',popup='Error: Map '+id+' does not exists',result=temp)
    else:
        cursor = db.cursor(buffered=True)
        cursor.execute('SELECT view FROM views WHERE id="'+id+'";')
        result2=cursor.fetchone()
        if result2 is None:
            cursor.execute("""INSERT INTO views(id,view) VALUES (%s,%s);""",(id,str(1)))
        else:
            cursor.execute("UPDATE views SET view=%s WHERE id=%s;",(str(int(result2[0])+1),id))
        db.commit()
        cursor.close()
        return render_template('map.html',id=id,name=result[1],email=result[2],author=result[3],json=result[4],sortable=result[5],visibility=result[6],date=result[7])
@app.route('/$temp<id>')
def mapstemp(id):
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM maps WHERE id='"+id+"';")
    result=cursor.fetchone()
    cursor.close()
    return render_template('temp.html',id=id,name=result[1],email=result[2],author=result[3],json=result[4],sortable=result[5],visibility=result[6],date=result[7])
@app.route('/$upload<id>', methods=['POST'])
def upload_file(id):
	if 'files[]' not in request.files:
		return jsonify({'result':'No file part in the request'})
	files = request.files.getlist('files[]')
	file=files[0]
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		filename=id+'_map.'+filename.rsplit('.', 1)[1].lower()
		file.save(os.path.join(r'/var/www/html/static', filename))
		return jsonify({'result':filename})
	else:
		return jsonify({'result':'File type is not allowed'})
@app.route('/$update',methods=['POST'])
def update():
    cursor = db.cursor(buffered=True)
    cursor.execute("UPDATE maps SET poi=%s, sortable=%s, visibility=%s, name=%s WHERE id=%s;",(request.form['json'],request.form['sortable'],request.form['visibility'],request.form['name'],request.form['id']))
    db.commit()
    cursor.close()
    return jsonify({'result':'Map update successfully'})
@app.route('/$delete',methods=['POST'])
def delete():
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM maps WHERE id=%s;",(request.form['id'],))
    db.commit()
    cursor.close()
    for f in glob.glob('/var/www/html/static/'+str(request.form['id'])+'_map.*'):
        os.remove(f)
    return render_template('index.html',popup='Success: Map '+request.form['name']+' been successfully deleted.')
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html',popup='Error: 404 Page not found'), 404
from werkzeug.exceptions import HTTPException
@app.errorhandler(Exception)
def handle_exception(e):
   if isinstance(e, HTTPException):
       return e
   return render_template("index.html", popup='Error: 500 Internal Server Error'), 500
if __name__ == "__main__":
    app.run()