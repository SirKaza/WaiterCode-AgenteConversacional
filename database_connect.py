import mysql.connector

def dataUp():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="rasa"
    )
    mycursor = mydb.cursor()
    sql = 'INSERT INTO user (q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14)'
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

if __name__=="__main__":
    dataUp()