import sys
import os
from flask import Flask, render_template,request, jsonify,redirect,url_for,jsonify,flash
import mysql.connector as mysql
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime
import glob, os
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = open("/var/www/html/password.txt", "r").read(),
    database = "fandommap"
)
cursor = db.cursor()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)
@app.route('/')
def index():
    cursor.execute('SELECT id,name,author,date FROM maps WHERE visibility="Public"')
    temp=''
    for row in cursor.fetchall():
        temp+='列列'.join(row)+'行行'
    return render_template('index.html',result=temp)
@app.route('/$temp')
def temp():
    return render_template('temp.html')
@app.route('/$fetch',methods=['POST'])
def fetch():
    cursor.execute("SELECT * FROM maps WHERE id='"+id+"';")
    return jsonify({'fetch':cursor.fetchall() })
@app.route('/$create',methods=['POST'])
def create():
    cursor.execute("SELECT COUNT(*) FROM maps;")
    try:
        Counter=cursor.fetchone()[0]+1
    except:
        Counter=1
    cursor.execute("""INSERT INTO maps (id,name,email,author,poi,sortable,visibility,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
    ,(str(Counter),request.form['name']+"'s Map",request.form['email'],request.form['name'],'{}','','Public',str(datetime.now().strftime('%d/%m/%Y'))))
    db.commit()
    return jsonify({'result':Counter})
@app.route('/<id>')
def maps(id):
    cursor.execute("SELECT * FROM maps WHERE id='"+id+"';")
    result=cursor.fetchone()
    try:
        return render_template('map.html',id=id,name=result[1],email=result[2],author=result[3],json=result[4],sortable=result[5],visibility=result[6],date=result[7])
    except:
        return render_template('index.html',popup='Error: Map '+id+' does not exists')
@app.route('/temp<id>')
def mapstemp(id):
    cursor.execute("SELECT * FROM maps WHERE id='"+id+"';")
    result=cursor.fetchone()
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
    cursor.execute("UPDATE maps SET poi=%s, sortable=%s, visibility=%s, name=%s WHERE id=%s;",(request.form['json'],request.form['sortable'],request.form['visibility'],request.form['name'],request.form['id']))
    db.commit()
    return jsonify({'result':'Map update successfully'})
@app.route('/$delete',methods=['POST'])
def delete():
    cursor.execute("DELETE FROM maps WHERE id=%s;",(request.form['id'],))
    db.commit()
    for f in glob.glob('/var/www/html/static/'+str(request.form['id'])+'_map.*'):
        os.remove(f)
    return render_template('index.html',popup='Success: Map '+request.form['name']+' been successfully deleted.')
if __name__ == "__main__":
    app.run()