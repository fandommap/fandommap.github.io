import mysql.connector as mysql
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "Laws2902",
    database = "fandommap"
)
name='Zachary'
email='zac@gmail.com'
mapname=name+"'s Map"
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM maps;")
try:
    Counter=cursor.fetchone()[0]+1
except:
    Counter=1
Counter=str(Counter)    
sql="""INSERT INTO maps (id,name,email,author,poi) VALUES (%s,%s,%s,%s,%s)"""
val=(Counter,mapname,email,name,'{}')
cursor.execute(sql,val)
#cursor.execute("""INSERT INTO maps (id,name,email,author,poi) VALUES ('%s','%s','%s','%s','%s');"""%('','','','',{}))
db.commit()
print({'result':Counter})

"""
cursor.execute("CREATE TABLE users (name VARCHAR(255), user_name VARCHAR(255))")
cursor.execute("INSERT INTO users (name, user_name) VALUES (%s, %s)", ("Hafeez", "hafeez"))
db.commit()
print(cursor.rowcount, "record inserted")
cursor.execute("SELECT * FROM users")
for record in cursor.fetchall():
    print(record)
cursor.execute("CREATE DATABASE datacamp")
print(cursor.fetchall())
for database in cursor.fetchall():
    print(database)
print(db)
cursor.execute("SELECT * FROM users")
databases = cursor.fetchall()
cursor = db.cursor()
CREATE DATABASE [database_name]
cursor.execute("CREATE DATABASE fandommap")
cursor.execute("CREATE TABLE maps (id VARCHAR(255), name VARCHAR(255), email VARCHAR(255),author VARCHAR(255),poi JSON)")
db.commit()
#id name email
"""



