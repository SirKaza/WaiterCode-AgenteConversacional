import mysql.connector

def dataUp(sender, message, column):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="rasa"
        #database="test"
    )
    mycursor = mydb.cursor(buffered=True)
    #sql = 'INSERT INTO user (q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14)'
    ifnull=  mycursor.execute('SELECT IFNULL( (SELECT %s FROM rasa.user WHERE sender = %s LIMIT 1) ,"not found");',(column,sender))
    #ifnull=  mycursor.execute('SELECT IFNULL( (SELECT q2 FROM test.user WHERE sender = %s LIMIT 1) ,"not found");',(sender,))
   # if (ifnull == None):
    if (column == "q1" and ifnull == None):
        sql = 'INSERT INTO rasa.user (sender, q1) VALUES ("{0}","{1}");'.format(sender,message)
        mycursor.execute(sql)
        mydb.commit()
    else:
        final = column+": "+message
        #sql ='UPDATE test.user SET %s=%s WHERE sender=%s;'
        #sql ='UPDATE test.user SET "{0}"="{1}" WHERE sender="{2}"};'.format(column,final,sender)
        sql ='UPDATE rasa.user SET '+column+'=%s WHERE sender=%s;'
        mycursor.execute(sql,(final,sender))
        #mycursor.execute(sql)
        mydb.commit()
        
  #  else:
        #sql ='update test.user set %s=%s where sender=%s;'
    #    sql ='UPDATE test.user SET q1="changed again" WHERE sender="rasa";'
     #   mycursor.execute(sql)
        #mydb.commit(sql,(column,message,sender))
      #  mydb.commit()
    #check = "SELECT * FROM test.rasa WHERE sender = ? AND ? IS NULL ",
    #update update test.user set q2="fairly" where sender="admin";
    # sql='INSERT INTO FeedBack_rasa_date (firstName, lastName, feedback) VALUES ("{0}","{1}", "{2}");'.format(FirstName,LastName,Feedback) 

