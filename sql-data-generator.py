# pip install mysql-connector-python & faker
from mysql.connector import connect, Error
import mysql.connector
from faker import Faker
import random

fake = Faker('el_GR')  # Set the locale to Greek (Greece)

database_name = "school_Database"

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database=database_name
)


def create_database_and_tables():
    create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
    create_db_tables = """
	CREATE TABLE IF NOT EXISTS Location (
        location_id INT PRIMARY KEY,
        address VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        postcode INT NOT NULL
    );
          
	CREATE TABLE IF NOT EXISTS University (
        university_id INT PRIMARY KEY,
        university_name VARCHAR(255) NOT NULL,
        founded_year YEAR NOT NULL,
        website VARCHAR(255),
        location_id INT NOT NULL,
        faculty_count INT,
        FOREIGN KEY (location_id) REFERENCES Location(location_id)
    );

    CREATE TABLE IF NOT EXISTS Faculty (
        faculty_id INT PRIMARY KEY,
        university_id INT NOT NULL,
        faculty_name VARCHAR(255) NOT NULL,
        contact_phone INT,
        contact_email VARCHAR(255),
        location_id INT NOT NULL,
        head_of_faculty VARCHAR(255) NOT NULL,
        FOREIGN KEY (university_id) REFERENCES University(university_id),
        FOREIGN KEY (location_id) REFERENCES Location(location_id)
    );        
        
    CREATE TABLE IF NOT EXISTS EducationLevel (
        level_id INT PRIMARY KEY,
        level_name ENUM('Bachelors', 'Masters', 'Phd'),
        description VARCHAR(255),
        entrance_requirements VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Degree (
        degree_id INT PRIMARY KEY,
        education_level_id INT NOT NULL,
        degree_name VARCHAR(255) NOT NULL,
        credits_required INT NOT NULL,
        FOREIGN KEY (education_level_id) REFERENCES EducationLevel(level_id)
    );
       
    CREATE TABLE IF NOT EXISTS Program (
        program_id INT PRIMARY KEY,
        awarded_degree INT not null,
        faculty_id INT NOT NULL,
        program_name VARCHAR(255) NOT NULL,
        year_started YEAR NOT NULL,
        teaching_type ENUM('Physical', 'Remote', 'Hybrid'),
        semesters INT NOT NULL,
        FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
        FOREIGN KEY (awarded_degree) REFERENCES Degree(degree_id)
    );
    
    CREATE TABLE IF NOT EXISTS Program_Term (
        program_term_id INT PRIMARY KEY,
        program_id INT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        max_capacity INT NOT NULL,
        registered_students INT,
        FOREIGN KEY (program_id) REFERENCES Program(program_id)
    );

    CREATE TABLE IF NOT EXISTS Modules (
        module_id INT PRIMARY KEY,
        program_term_id INT NOT NULL,
        module_name VARCHAR(255) NOT NULL,
        module_subject VARCHAR(255) NOT NULL,
        module_points INT NOT NULL,
        semester VARCHAR(255) NOT NULL,
        FOREIGN KEY (program_term_id) REFERENCES Program_Term(program_term_id)
    );

	CREATE TABLE IF NOT EXISTS Student (
        student_id INT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        father_name VARCHAR(255),
        email VARCHAR(255) NOT NULL,
        date_of_birth DATE NOT NULL
    );
            
   CREATE TABLE IF NOT EXISTS StudentModuleResults (
        result_id INT PRIMARY KEY,
        module_id INT NOT NULL,
        student_id INT NOT NULL,
        result_grade VARCHAR(255) NOT NULL,
        passed BOOLEAN,
        FOREIGN KEY (module_id) REFERENCES Modules(module_id),
        FOREIGN KEY (student_id) REFERENCES Student(student_id)
    );
    
    CREATE TABLE IF NOT EXISTS Enrollment (
        enrollment_id INT PRIMARY KEY,
        student_id INT NOT NULL,
        program_term_id INT NOT NULL,
        registration_date DATE NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (program_term_id) REFERENCES Program_Term(program_term_id)
    );

    CREATE TABLE IF NOT EXISTS Graduation (
        graduation_id INT PRIMARY KEY,
        enrollment_id INT NOT NULL,
        final_grade INT NOT NULL,
        graduation_date DATE NOT NULL,
        top_of_class BOOLEAN NOT NULL,
        location_id INT NOT NULL,
        FOREIGN KEY (location_id) REFERENCES Location(location_id),
        FOREIGN KEY (enrollment_id) REFERENCES Enrollment(enrollment_id)
    );
    
    
    CREATE TABLE IF NOT EXISTS Company (
        company_id INT PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        location_id INT NOT NULL,
        employees INT NOT NULL,
        industry ENUM('Telecommunications', 'Hospitality', 'Shipping', 'Engineering', 'Software', 'Auditing', 'Banking', 'Other'),
        FOREIGN KEY (location_id) REFERENCES Location(location_id)
    );

    CREATE TABLE IF NOT EXISTS JobTitle (
        title_id INT PRIMARY KEY,
        title_name VARCHAR(255) NOT NULL,
        job_type ENUM('SoftwareEngineering', 'accounting', 'Shipping', 'DataScience', 'Business', 'Sales', 'Consulting'),
        description VARCHAR(255) NOT NULL
    );
        
    CREATE TABLE IF NOT EXISTS WorkExperience (
        experience_id INT PRIMARY KEY,
        student_id INT NOT NULL,
        company_id INT NOT NULL,
        job_title_id INT NOT NULL,
        job_category ENUM('SoftwareEngineering', 'accounting', 'Shipping', 'DataScience', 'Business', 'Sales', 'Consulting'),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        description VARCHAR(255) NOT NULL,
        responsibilities VARCHAR(255) NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (company_id) REFERENCES Company(company_id),
        FOREIGN KEY (job_title_id) REFERENCES JobTitle(title_id)
    );
"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
            cursor.execute(create_db_tables)

    except Error as e:
        print(e)


def generate_and_insert_locations(num):
    locations = []
    location_ids = []
    # Generate fake data
    for i in range(1, num + 1):
        location = (
            i,                           # location_id
            fake.address(),              # location_address
            fake.city(),                 # city
            fake.random_int(min=10000, max=99999)  # postcode
        )
        locations.append(location)
        location_ids.append(i)

    cursor = connection.cursor()

    # Assuming your table has columns (location_id, location_address, city, postcode)
    insert_query = "INSERT INTO Location (location_id, location_address, city, postcode) VALUES (%s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, locations)
        connection.commit()
        print(f"Inserted {len(locations)} records into the Location table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

    return location_ids


# generate 100 locations
generate_and_insert_locations(100)


def generate_and_insert_students(num):
    students = []

    # Generate fake data
    for i in range(1, num + 1):
        student = (
            i,                           # student_id
            fake.first_name(),           # first_name
            fake.last_name(),            # last_name
            fake.first_name(),           # father_name
            fake.email(),                # email
            fake.date_of_birth(),        # date_of_birth
        )
        students.append(student)

    # Create a cursor object
    cursor = connection.cursor()

    # Assuming your table has columns (student_id, first_name, last_name, father_name, email, date_of_birth)
    insert_query = "INSERT INTO Student (student_id, first_name, last_name, father_name, email, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, students)
        connection.commit()
        print(f"Inserted {len(students)} records into the Student table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# need to generate universities and make sure that the location_id is matchingone entry generated from the generate and insert location function.


generate_and_insert_students(500)


def generate_and_insert_universities(num, location_ids):
    universities = []

    # Use the provided list of university names
    athens_universities = [
        "National and Kapodistrian University of Athens",
        "National Technical University of Athens",
        "Athens University of Economics and Business",
        "University of Piraeus",
        "Panteion University of Social and Political Sciences",
        "Harokopio University",
        "Agricultural University of Athens",
        "University of West Attica",
        "University of Peloponnese",
        "Hellenic Open University",
    ]

    random.shuffle(location_ids)

    # Generate fake data
    # Generate entries for each Athens university
    for i, university_name in enumerate(athens_universities, start=1):
        university = (
            i,                                    # university_id
            university_name,                      # university_name
            fake.random_int(min=1902, max=2024),   # founded_year
            fake.url(),                            # website
            location_ids[i - 1],          # location_id
            fake.random_int(min=1, max=1000),      # faculty_count
        )
        universities.append(university)

    # Create a cursor object
    cursor = connection.cursor()

    # Assuming your table has columns (university_id, university_name, founded_year, website, location_id, faculty_count)
    insert_query = "INSERT INTO University (university_id, university_name, founded_year, website, location_id, faculty_count) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, universities)
        connection.commit()
        print(
            f"Inserted {len(universities)} records into the University table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


location_ids = generate_and_insert_locations(100)
generate_and_insert_universities(10, location_ids)


def generate_and_insert_faculties(num, university_ids):
    faculties = []

    # Use the provided list of university names
    random_faculties = [
        "Faculty of Arts",
        "Faculty of Sciences",
        "Faculty of Engineering",
        "Faculty of Business Administration",
        "Faculty of Social Sciences",
        "Faculty of Medicine",
        "Faculty of Law",
        "Faculty of Economics",
        "Faculty of Information Technology",
        "Faculty of Environmental Sciences",
        "Faculty of Education",
        "Faculty of Agriculture",
        "Faculty of Fine Arts",
        "Faculty of Psychology",
        "Faculty of Communication",
    ]

    # CREATE TABLE IF NOT EXISTS Location


# def generate_and_insert_EducationLevel()

# def generate_and_insert_Degree()

# def generate_and_insert_Program()

# def generate_and_insert_Programterm()

# def generate_and_insert_modules()

# def generate_and_insert_student_module_results()

# def generate_and_insert_student_enrollment()

# def generate_and_insert_student_graduation()

# def generate_and_insert_student_company()

# def generate_and_insert_student_jobtitle()

# def generate_and_insert_student_workexperience()


# Close the connection
connection.close()
