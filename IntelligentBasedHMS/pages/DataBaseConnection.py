import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import psycopg2
DB_name='HMS_DATABASE'
DB_user='postgres'
DB_pass='1234'
DB_host="localhost"
DB_port='5432'

def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            database=DB_name,
            user=DB_user,
            password=DB_pass,
            host=DB_host,
            port=DB_port
        )
        curr=conn.cursor()
        print("Connection to the database was successful.")
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
    return conn
 
def create_table():
    conn = create_connection()
    curr = conn.cursor()
    create_table_query="""
CREATE TABLE IF NOT EXISTS PATIENT_DATA (
    Patient_ID INTEGER PRIMARY KEY,                                

    First_Name VARCHAR(50) NOT NULL,
    Last_Name  VARCHAR(50) NOT NULL,

    Email VARCHAR(100) UNIQUE NOT NULL,                            
    Phone VARCHAR(15) NOT NULL,

    Home_Address TEXT DEFAULT 'Not Provided',                      

    Emergency_Contact VARCHAR(15),

    Date_of_Birth DATE NOT NULL,

    Gender VARCHAR(10) NOT NULL 
        CHECK (Gender IN ('Male', 'Female', 'Other')),             

    Blood_Type VARCHAR(10) 
        CHECK (Blood_Type IN 
              ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),  

    Password VARCHAR(255) UNIQUE NOT NULL                        

         
);


"""
    curr.execute(create_table_query)
    conn.commit()
    print("Patient Data Table created successfully.")
create_table()