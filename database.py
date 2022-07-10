import pymysql.cursors
import uuid
from core import *

conn=pymysql.connect(db="users bar system",user="root",password='',host="localhost")

def checkUserNameExist(name):
    cursor=conn.cursor()
    rows=cursor.execute("SELECT * FROM users WHERE UserName=%s",[name])
    cursor.close()
    return True if rows>0 else False
def ComparePassword(name,password):
    from werkzeug.security import check_password_hash
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM users WHERE UserName=%s", [name])
    Password= check_password_hash()
    cursor.close()
    if Password == password:
        return True
    return False
def getEmployeesDB():
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees=cursor.fetchall()
    cursor.close()
    return employees

def authenticate(userName,Password):
    from werkzeug.security import check_password_hash
    cursor=conn.cursor()
    rows=cursor.execute('SELECT Password FROM users WHERE UserName=%s',[userName])
    if rows>0:
        if convertTuple(cursor.fetchone()[0])==Password:
            cursor.close()
            return True
    cursor.close()
    return False

def authenticateAdminDB(userName,Password):
    from werkzeug.security import check_password_hash
    from werkzeug.security import generate_password_hash
    cursor=conn.cursor()
    rows=cursor.execute('SELECT Password FROM admin WHERE UserName=%s',[userName])
    if rows>0:
        if cursor.fetchone()[0]== Password:
            cursor.close()
            return True
    cursor.close()
    return False

def authenticateAdmin(userName,Password):
    from werkzeug.security import generate_password_hash
    cursor=conn.cursor()
    rows=cursor.execute('SELECT Password FROM admin WHERE UserName=%s',[userName])
    if rows>0:
        if convertTuple(cursor.fetchone()[0])==Password:
            cursor.close()
            return True
    cursor.close()
    return False
def getProductsDB():
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM stock')
    products=cursor.fetchall()
    cursor.close()
    return products
def generateQuantity(array):
    cursor = conn.cursor()
    NewQuantity=[]
    for i in range(len(array)):
        cursor.execute('SELECT Quantity FROM stock  WHERE StockID=%s ',[i+1])
        NewQuantity.append(int(cursor.fetchone()[0])-int(array[i]))
    cursor.close()
    return NewQuantity
def UpdateDB(array):
    cursor = conn.cursor()
    for i in range(len(array)):
        if array[i]>0:
            cursor.execute("""UPDATE stock
                       SET Quantity=%s
                       WHERE StockID=%s""", [array[i],i+1])
    conn.commit()
    cursor.close()
def Commision(id,array):
    cursor = conn.cursor()
    cursor.execute('SELECT Commission FROM employees  WHERE EmployeeID=%s ', [int(id)])
    commission=int(cursor.fetchone()[0])
    for i in range(len(array)):
        if int(array[i]) > 0:
            cursor.execute('SELECT Commission FROM stock  WHERE StockID=%s ', [i + 1])
            commission += int(cursor.fetchone()[0]) * int(array[i])
    cursor.close()
    return commission
def Earnings(array):
    cursor = conn.cursor()
    earnings=0
    for i in range(len(array)):
        if int(array[i]) > 0:
            cursor.execute('SELECT Cost FROM stock  WHERE StockID=%s ', [i + 1])
            earnings += int(cursor.fetchone()[0]) * int(array[i])
    cursor.close()
    return earnings
def UpdateEmployee(id,array,commission):
    cursor = conn.cursor()
    cursor.execute('SELECT SoldDrinks FROM employees  WHERE EmployeeID=%s ', [int(id)])
    total=int(cursor.fetchone()[0])
    for i in range(len(array)):
        if int(array[i])>0:
            total+=int(array[i])
    cursor.execute("""UPDATE employees
           SET SoldDrinks=%s , Commission=%s
           WHERE EmployeeID =%s""", [total,commission,int(id)])
    conn.commit()
    cursor.close()
    return total
def inTialiseEmployees():
    cursor = conn.cursor()
    cursor.execute("""UPDATE employees
               SET SoldDrinks=%s , Commission=%s""", [0,0])
    conn.commit()
    cursor.close()
def addAdmin(data):
    cursor=conn.cursor()
    cursor.execute("INSERT into admin VALUES(%s,%s)",[data['userName'],data["password"]])
    conn.commit()
    cursor.close()