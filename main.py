import pandas as pd
import sqlite3

#connect to The DB
conn = sqlite3.Connection('data.sqlite')

#Subtittute JOIn with subQueries
q ="""
SELECT lastName, firstName, OfficeCode
FROM employees
JOIN offices
    USING(officeCode)
WHERE country = 'USA'

;
"""
df = pd.read_sql(q, conn)

print(df)

#Subquery usage
q = """
SELECT firstName, lastName, officeCode
FROM employees
WHERE officeCode IN (
    SELECT officeCode
    FROM offices
    WHERE country = "USA"
)
;
"""
df = pd.read_sql(q, conn)
print(df)

#subqueries for filtering Based on an aggregation

q = """
SELECT lastName, firstName, officeCode
FROM employees
WHERE officeCode IN (
    SELECT officeCode
    FROM offices
    JOIN employees
        USING(officeCode)
    GROUP BY 1
    HAVING COUNT(employeeNumber) >= 5
)
;
"""
df = pd.read_sql(q, conn)
print(df)

#Chaining aggregates
q = """
SELECT AVG(customerAvgPayment) 
AS averagePayment
FROM (
    SELECT AVG(amount) AS customerAvgPayment
    FROM payments
    JOIN customers
        USING(customerNumber)
    GROUP BY customerNumber

)
;
"""
df = pd.read_sql(q, conn)
print(df)

#Foreign Key Reference

q = """
SELECT lastName, firstName, employeeNumber
FROM employees
WHERE employeeNumber IN
    (
    SELECT salesRepEmployeeNumber
        FROM customers
        WHERE country = 'USA')

;
"""
df = pd.read_sql(q, conn)
print(df)

conn.close()