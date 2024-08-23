import pandas as pd
from sqlalchemy import create_engine
import urllib

def engine():
    params = urllib.parse.quote_plus("DRIVER={SQL Server};"
                                   "SERVER=DESKTOP-UVTISLI\MSSQLSERVERKAMYA;"
                                   "DATABASE=Northwind;"
                                   ''' "UID=AbidiPln;"
                                    "PWD=U8v@3d6Hg#c!;" '''
                                   )

    return create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

def dataframe(string):
    cnxn = engine()
    df = pd.read_sql_query(string, cnxn)
    return df

a = dataframe('select * from dbo.Customers')

# In[]: using pyodbc
import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "SERVER=DESKTOP-UVTISLI\MSSQLSERVERKAMYA;"
    "DATABASE=Northwind;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE dsp.products (
    product_id int primary key,
    product_name nvarchar(50),
    price int
    )
    """
)

conn.commit()

cursor.execute(
    """
insert into dsp.products ( product_id, product_name, price) values(1000, 'Diaper2', 15000)
    """
)

conn.commit()

df = pd.read_sql_query('''Select * from products''', conn)

for k in range(150, 999):
    cursor.execute(
        """
    insert into dsp.products ( product_id, product_name, price) values({}, '{}', {})
        """.format(k, 'Product',k**2)
    )

conn.commit()

cursor.execute("alter table dsp.products add newcolumn tinyint")
conn.commit()

cursor.execute("update dsp.products set newcolumn = 10 where newcolumn is null")
conn.commit()
