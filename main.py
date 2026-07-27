# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

def _table_name(*candidates):
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
    lower_to_name = {name.lower(): name for name in tables['name'].tolist()}
    for candidate in candidates:
        if candidate.lower() in lower_to_name:
            return lower_to_name[candidate.lower()]
    return None

def _column_name(table, *candidates):
    if table is None:
        return None
    info = pd.read_sql(f"PRAGMA table_info({table})", conn)
    lower_to_name = {name.lower(): name for name in info['name'].tolist()}
    for candidate in candidates:
        if candidate.lower() in lower_to_name:
            return lower_to_name[candidate.lower()]
    return None

def _select_all(table, where=None):
    if table is None:
        return pd.DataFrame()
    statement = f"SELECT * FROM {table}"
    if where:
        statement += f" WHERE {where}"
    return pd.read_sql(statement, conn)

customers_table = _table_name('customers', 'Customers')
employees_table = _table_name('employees', 'Employees')
contacts_table = _table_name('contacts', 'Contacts')
payment_table = _table_name('payment', 'Payment')
credit_table = _table_name('credit', 'Credit')
product_sold_table = _table_name('product_sold', 'productsold', 'ProductSold')

# STEP 1
city_col = _column_name(customers_table, 'city', 'City', 'customer_city', 'CustomerCity')
df_boston = _select_all(customers_table, f"{city_col} = 'Boston'") if city_col else pd.DataFrame()

# STEP 2
employee_count_col = _column_name(customers_table, 'employees', 'employee_count', 'number_of_employees')
df_zero_emp = _select_all(customers_table, f"{employee_count_col} = 0") if employee_count_col else pd.DataFrame()

# STEP 3
df_employee = _select_all(employees_table)

# STEP 4
df_contacts = _select_all(contacts_table)

# STEP 5
df_payment = _select_all(payment_table)

# STEP 6
df_credit = _select_all(credit_table)

# STEP 7
df_product_sold = _select_all(product_sold_table)

# STEP 8
if customers_table:
    df_total_customers = pd.read_sql(
        f"SELECT COUNT(*) AS total_customers FROM {customers_table}", conn
    )
else:
    df_total_customers = pd.DataFrame()

# STEP 9
df_customers = _select_all(customers_table)

# STEP 10
age_col = _column_name(customers_table, 'age', 'Age', 'customer_age', 'CustomerAge')
df_under_20 = _select_all(customers_table, f"{age_col} < 20") if age_col else pd.DataFrame()

conn.close()