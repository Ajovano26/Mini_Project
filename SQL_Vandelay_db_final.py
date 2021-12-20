#Amy Jovanovic, 30003069 DATA 311 Project
import psycopg2
from random import randint
import matplotlib.pyplot  as plt
from matplotlib.colors import hsv_to_rgb


# The following connects user to the postgreSQL database
conn = psycopg2.connect(database='vandelay_db', user='postgres', password='password', host='localhost', port='5432')
cursor = conn.cursor()

# The following is the data to be included in the created database , the database will be populated with the following data
fist_names = ['George', 'Cosmo', 'Jerry', 'Steve', 'Elaine', 'Sally', 'Angela', 'Pam']
last_names = ['Costanza', 'Kramer', 'Seinfeld', 'Johnson', 'Benes', 'Jones', 'Burns', 'Beesly']
id_numbers = [42069, 42075, 39523, 42108, 42128, 42055, 42047, 42188]
division_names = ['Latexx', 'Beyond', 'Soup']
managers = ['Russel Dalrymple', 'Arthur Pensky', 'Yev Kassem']
locations = ['New Jersey', 'Los Angeles', 'New York']
values = [] #This creates an empty list to hold the values of the sales  
for i in range(8):
    value = 1000 * randint(15, 99) #This function is creating sales vales to populate the database 
    values.append(value)

# The following creates 3 tables in the database 
sql_table_1 = '''CREATE TABLE Employees(
    FIRST_NAME CHAR(20) NOT NULL,
    LAST_NAME CHAR(20) NOT NULL,
    ID INT)'''

sql_table_2 = '''CREATE TABLE Divisions(
    DIVISION CHAR(20) NOT NULL,
    MANAGER CHAR(20) NOT NULL,
    LOCATION CHAR(20) NOT NULL)'''

sql_table_3 = '''CREATE TABLE Sales(
    DIVISION CHAR(20) NOT NULL,
    ID INT,
    VALUE INT)'''

cursor.execute("DROP TABLE IF EXISTS Employees")
cursor.execute("DROP TABLE IF EXISTS Divisions")
cursor.execute("DROP TABLE IF EXISTS Sales")

cursor.execute(sql_table_1)
cursor.execute(sql_table_2)
cursor.execute(sql_table_3)

# The following is populating the 3 tables in the database
for i in range(8):
    sql_insert = f'''INSERT INTO Employees(FIRST_NAME,LAST_NAME,ID) 
                      VALUES('{fist_names[i]}','{last_names[i]}',{id_numbers[i]})''' #This function populates the Employee entity table with the attributes of employee identification such as first name, last name and their identification number (ID)
    cursor.execute(sql_insert)

for i in range(3):
    sql_insert = f'''INSERT INTO Divisions(DIVISION,MANAGER,LOCATION) 
                      VALUES('{division_names[i]}','{managers[i]}','{locations[i]}')''' #This function populates the Division  entity table with the attributes of their workplace division, manager and location
    cursor.execute(sql_insert)

for i in range(8):
    if i < 3:
        j = 0
    elif 3 < i < 6:
        j = 1
    else:
        j = 2
    sql_insert = f'''INSERT INTO Sales(DIVISION,ID,VALUE) 
                      VALUES('{division_names[j]}','{id_numbers[i]}',{values[i]})''' #This function populates the Sales entity table with the information of the division, the employees ID and the value of the sale(s)
    cursor.execute(sql_insert)


# Question 1 (Chart)
print("Question 1 - Generate a pie chart representing total sales by employee ID.")
sql_retrieve = '''SELECT ID, VALUE FROM Sales'''
cursor.execute(sql_retrieve)
result = cursor.fetchall()
values = []
ids = []
for rows in result:
    values.append(rows[1])
    ids.append(rows[0])
plt.pie(values, labels=ids, autopct='%1.1f%%')
plt.title("Total Sales by Employee ID Number", fontweight ="bold")
plt.show()
print("\n")

# Question 2 (Aggregate)
print("Question 2 - Print the total amount of Sales in the Sales table.")
sql_retrieve = '''SELECT SUM(VALUE) FROM Sales'''
cursor.execute(sql_retrieve)
result = cursor.fetchone()
print("The total Sales made in the Sales table is: ", result[0])
print("\n")

# Question 3 (Aggregate)
print("Question 3 - Count the Number of Managers in a given division. (Latexx, Beyond or Soup)")
sql_retrieve = '''SELECT COUNT(DIVISIONS) FROM Divisions WHERE DIVISION='Latexx' '''
cursor.execute(sql_retrieve)
result = cursor.fetchone()
print("The number of managers that work in the Latexx Division is: ", result[0])
print("\n")

# Question 4 (Aggregate)
print("Question 4 - Count the total number of Divisions in the Divisions table.")
sql_retrieve = '''SELECT DISTINCT COUNT(Divisions) FROM DIVISIONS'''
cursor.execute(sql_retrieve)
result = cursor.fetchone()
print("The total number of distict divisions from the divisions table is: ", result[0])
print("\n")

# Question 5 (Chart)
print("Question 5 - Generate a pie chart depicting the ratio of all employees in each Division")
latexx_count = '''SELECT COUNT(DIVISION) FROM Divisions WHERE DIVISION='Latexx' '''
soup_count = '''SELECT COUNT(DIVISION) FROM Divisions WHERE DIVISION='Soup' '''
beyond_count = '''SELECT COUNT(DIVISION) FROM Divisions WHERE DIVISION='Beyond' '''
values = []
cursor.execute(latexx_count)
latexx_result = cursor.fetchone()
values.append(latexx_result[0])
cursor.execute(soup_count)
soup_result = cursor.fetchone()
values.append(soup_result[0])
cursor.execute(beyond_count)
beyond_result = cursor.fetchone()
values.append(beyond_result[0])
labels = ["Latexx", "Soup", "Beyond"]
plt.pie(values, labels = labels, autopct='%1.1f%%')
plt.title("Ratio of all company employees by division", fontweight ="bold")
plt.show()
print("\n")

# Question 6 (Aggregate)
print("Question 6 - What was the highest sale to date?")
sql_retrieve = '''SELECT MAX(VALUE) FROM Sales'''
cursor.execute(sql_retrieve)
result = cursor.fetchone()
print("The Highest sale in the sales table is: ", result[0])
print("\n")

# Question 7 (Aggregate)
print("Question 7 - Vandelay hires a new employee Scott Benson. Insert his employee info into the applicable table.")
sql_insert = '''INSERT INTO Employees(FIRST_NAME, LAST_NAME, ID)
VALUES('Scott', 'Benson', 36942)'''
cursor.execute(sql_insert)
print("Scott Benson has been added to the employee Database.")
cursor.execute("SELECT * FROM employees")
result = cursor.fetchall() 
# loop through the rows
for row in result:
    print(row)  
print("\n")

# Question 8 (AGGREGATE)
print("Question 8 - Who is the Manager for the Soup Division?")
sql_retrieve = '''SELECT MANAGER FROM Divisions WHERE DIVISION='Soup' '''
cursor.execute(sql_retrieve)
result = cursor.fetchone()
print("The manager of the Soup Division is: ", result[0])
print("\n")


# QUESTION 9 (join)
print("Question 9 - What was the lowest sale to date?")
sql_retrieve = '''SELECT MIN(VALUE) FROM Sales'''
cursor.execute(sql_retrieve)
result = cursor.fetchone()
print("The LOWEST sale in the sales table is: ", result[0])
print("\n")



# Question 10 (join)
print("Question 10 - Generate a table that combines Sales Values and Managers from the divisions table.")
sql_retrieve = '''SELECT sales.VALUE, divisions.MANAGER, divisions.DIVISION FROM Divisions INNER JOIN Sales ON Divisions.DIVISION=Sales.DIVISION'''
cursor.execute(sql_retrieve)
result = cursor.fetchall()
print("Generated a new table Combining Sales values, Managers and Divisions.")
for rows in result:
    print(rows)
conn.commit()
print("\n")

# Question 11 (join)
print("Question 11 -  Generate a table that combines employee names with sales.")#This creates an inner join 
sql_retrieve = '''SELECT employees.FIRST_NAME, employees.LAST_NAME, employees.ID, Sales.VALUE FROM Sales INNER JOIN Employees ON Sales.ID=Employees.ID'''
cursor.execute(sql_retrieve)
result = cursor.fetchall()
print("Generated a new table Combining Sales values, Managers and Divisions.")
for rows in result:
    print(rows)
conn.commit()
print("\n")

# Question 12 (chart)
print("Question 12 - Display a bar chart showing the difference in sales by division.")
sql_retrieve = '''SELECT VALUE, DIVISION FROM Sales'''
cursor.execute(sql_retrieve)
result = cursor.fetchall()
values = []
labels = []
for rows in result:
    values.append(rows[0])
    labels.append(rows[1])
values.sort()
labels.sort()
cleaned_labels = []
plt.bar(labels, values, align ='center', label="Total sales")
plt.legend()
plt.ylabel("Sales ($USD)", fontweight ="bold")
plt.xlabel("Division", fontweight ="bold")
plt.title("Sales by Division", fontweight ="bold")
plt.show()
print("\n")

print("Question 13 - Generate a table LAST_NAME, Sales and Divisions")
sql_retrieve = '''SELECT Employees.LAST_NAME, Sales.VALUE, Sales.DIVISION FROM Sales INNER JOIN Employees ON Sales.ID=Employees.ID'''
cursor.execute(sql_retrieve)
result = cursor.fetchall()
print("New joined employee last name and sales value.")
for rows in result:
    print(rows)
conn.commit()
print("\n")

conn.close()