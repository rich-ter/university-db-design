import mysql.connector
from mysql.connector import Error
from db_operations import generate_and_insert_locations, create_database_and_tables, generate_and_insert_students, generate_and_insert_universities, generate_and_insert_faculties, generate_and_insert_educationLevel, generate_and_insert_degree, generate_and_insert_Program, generate_and_insert_Programterm, generate_and_insert_modules, generate_and_insert_enrollments, generate_and_insert_companies, generate_and_insert_job_titles, generate_and_insert_graduations, generate_and_insert_work_experiences, generate_and_insert_student_module_participation


def create_database(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database '{database_name}' created or already exists.")
    cursor.close()

def connect_to_database(host_name, user_name, user_password, database_name=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name,
            allow_local_infile=True
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

host_name = 'localhost'
user_name = 'root'
user_password = 'root'
database_name = 'university_db'

connection = connect_to_database(host_name, user_name, user_password)

if connection is not None:
    create_database(connection, database_name)
    connection.close()  

# Step 3: Connect to the newly created or existing database
connection = connect_to_database(host_name, user_name, user_password, database_name)

if connection is not None:
    create_database_and_tables(connection)

    num_locations = 12000  
    generate_and_insert_locations(connection, num_locations)

    num_students = 10000
    generate_and_insert_students(connection, num_students)

    generate_and_insert_universities(connection)

    generate_and_insert_faculties(connection)
    
    generate_and_insert_educationLevel(connection)

    generate_and_insert_degree(connection)

    generate_and_insert_Program(connection)

    generate_and_insert_Programterm(connection)

    generate_and_insert_modules(connection)

    generate_and_insert_student_module_participation(connection, num_students)

    number_of_enrollments = 20000
    generate_and_insert_enrollments(connection,number_of_enrollments)

    number_of_companies = 300
    generate_and_insert_companies(connection,number_of_companies)

    number_of_job_titles = 800
    generate_and_insert_job_titles(connection, number_of_job_titles)

    generate_and_insert_graduations(connection, 44998)

    number_of_work_experiences = 10000
    generate_and_insert_work_experiences(connection, number_of_work_experiences)


    connection.close()
