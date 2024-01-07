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
        level_name ENUM('Bachelors', 'Masters', 'Phd', 'Associates', 'Post Graduate Diploma', 'Under Graduate Diploma'),
        level ENUM('Level 6', 'Level 7', 'Level 8'),
        description VARCHAR(255),
        ects_requirements INT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Degree (
        degree_id INT PRIMARY KEY,
        education_level_id INT NOT NULL,
        degree_name VARCHAR(255) NOT NULL,
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

# this is not finished yet 
def generate_and_insert_faculties(num, university_ids):
    faculties = []

    (1, 1, 'NKUA Faculty of Arts', NULL, NULL, 1, 'Head of NKUA Faculty of Arts'),
    (2, 1, 'NKUA Faculty of Sciences', NULL, NULL, 1, 'Head of NKUA Faculty of Sciences'),
    (3, 1, 'NKUA Faculty of Law', NULL, NULL, 1, 'Head of NKUA Faculty of Law'),
    (4, 1, 'NKUA Faculty of Medicine', NULL, NULL, 1, 'Head of NKUA Faculty of Medicine'),
    (5, 1, 'NKUA Faculty of Engineering', NULL, NULL, 1, 'Head of NKUA Faculty of Engineering'),
    (6, 1, 'NKUA Faculty of Architecture', NULL, NULL, 1, 'Head of NKUA Faculty of Architecture'),

    (7, 2, 'NTUA School of Civil Engineering', NULL, NULL, 2, 'Head of NTUA School of Civil Engineering'),
    (8, 2, 'NTUA School of Mechanical Engineering', NULL, NULL, 2, 'Head of NTUA School of Mechanical Engineering'),
    (9, 2, 'NTUA School of Electrical and Computer Engineering', NULL, NULL, 2, 'Head of NTUA School of Electrical and Computer Engineering'),
    (10, 2, 'NTUA School of Chemical Engineering', NULL, NULL, 2, 'Head of NTUA School of Chemical Engineering'),
    (11, 2, 'NTUA School of Rural and Surveying Engineering', NULL, NULL, 2, 'Head of NTUA School of Rural and Surveying Engineering'),
    (12, 2, 'NTUA School of Applied Mathematical and Physical Sciences', NULL, NULL, 2, 'Head of NTUA School of Applied Mathematical and Physical Sciences'),

    (13, 3, 'AUEB Department of Business Administration', NULL, NULL, 3, 'Head of AUEB Department of Business Administration'),
    (14, 3, 'AUEB Department of Economics', NULL, NULL, 3, 'Head of AUEB Department of Economics'),
    (15, 3, 'AUEB Department of International and European Economic Studies', NULL, NULL, 3, 'Head of AUEB Department of International and European Economic Studies'),
    (16, 3, 'AUEB Department of Marketing and Communication', NULL, NULL, 3, 'Head of AUEB Department of Marketing and Communication'),
    (17, 3, 'AUEB Department of Accounting and Finance', NULL, NULL, 3, 'Head of AUEB Department of Accounting and Finance'),
    (18, 3, 'AUEB Department of Management Science and Technology', NULL, NULL, 3, 'Head of AUEB Department of Management Science and Technology'),

    (19, 4, 'UoP Department of Banking and Financial Management', NULL, NULL, 4, 'Head of UoP Department of Banking and Financial Management'),
    (20, 4, 'UoP Department of Business Administration', NULL, NULL, 4, 'Head of UoP Department of Business Administration'),
    (21, 4, 'UoP Department of Maritime Studies', NULL, NULL, 4, 'Head of UoP Department of Maritime Studies'),
    (22, 4, 'UoP Department of International and European Studies', NULL, NULL, 4, 'Head of UoP Department of International and European Studies'),
    (23, 4, 'UoP Department of Digital Systems', NULL, NULL, 4, 'Head of UoP Department of Digital Systems'),

    (24, 5, 'Panteion Department of Political Science and History', NULL, NULL, 5, 'Head of Panteion Department of Political Science and History'),
    (25, 5, 'Panteion Department of Sociology', NULL, NULL, 5, 'Head of Panteion Department of Sociology'),
    (26, 5, 'Panteion Department of Social Policy', NULL, NULL, 5, 'Head of Panteion Department of Social Policy'),
    (27, 5, 'Panteion Department of Communication, Media, and Culture', NULL, NULL, 5, 'Head of Panteion Department of Communication, Media, and Culture'),
    (28, 5, 'Panteion Department of Psychology', NULL, NULL, 5, 'Head of Panteion Department of Psychology'),

    (29, 6, 'Harokopio Department of Dietetics and Nutritional Science', NULL, NULL, 6, 'Head of Harokopio Department of Dietetics and Nutritional Science'),
    (30, 6, 'Harokopio Department of Informatics and Telematics', NULL, NULL, 6, 'Head of Harokopio Department of Informatics and Telematics'),
    (31, 6, 'Harokopio Department of Home Economics and Ecology', NULL, NULL, 6, 'Head of Harokopio Department of Home Economics and Ecology'),
    (32, 6, 'Harokopio Department of Geography', NULL, NULL, 6, 'Head of Harokopio Department of Geography'),

    (33, 7, 'AUA School of Agricultural Sciences', NULL, NULL, 7, 'Head of AUA School of Agricultural Sciences'),
    (34, 7, 'AUA School of Food, Biotechnology, and Development', NULL, NULL, 7, 'Head of AUA School of Food, Biotechnology, and Development'),
    (35, 7, 'AUA School of Natural Resources and Agricultural Engineering', NULL, NULL, 7, 'Head of AUA School of Natural Resources and Agricultural Engineering'),

    (36, 8, 'UniWA Department of Business Administration', NULL, NULL, 8, 'Head of UniWA Department of Business Administration'),
    (37, 8, 'UniWA Department of Informatics and Computer Engineering', NULL, NULL, 8, 'Head of UniWA Department of Informatics and Computer Engineering'),
    (38, 8, 'UniWA Department of Civil Engineering', NULL, NULL, 8, 'Head of UniWA Department of Civil Engineering'),
    (39, 8, 'UniWA Department of Electrical and Computer Engineering', NULL, NULL, 8, 'Head of UniWA Department of Electrical and Computer Engineering'),

    (40, 9, 'UoP Department of Computer Science and Technology', NULL, NULL, 9, 'Head of UoP Department of Computer Science and Technology'),
    (41, 9, 'UoP Department of Environmental and Natural Resources Management', NULL, NULL, 9, 'Head of UoP Department of Environmental and Natural Resources Management'),
    (42, 9, 'UoP Department of Economics, Sports Science, and Tourism', NULL, NULL, 9, 'Head of UoP Department of Economics, Sports Science, and Tourism'),
    (43, 9, 'UoP Department of History, Archaeology, and Cultural Resources Management', NULL, NULL, 9, 'Head of UoP Department of History, Archaeology, and Cultural Resources Management'),

    (44, 10, 'HOU School of Science and Technology', NULL, NULL, 10, 'Head of HOU School of Science and Technology'),
    (45, 10, 'HOU School of Humanities', NULL, NULL, 10, 'Head of HOU School of Humanities'),
    (46, 10, 'HOU School of Social Sciences', NULL, NULL, 10, 'Head of HOU School of Social Sciences'),
    (47, 10, 'HOU School of Applied Arts', NULL, NULL, 10, 'Head of HOU School of Applied Arts');


    INSERT INTO Faculty (faculty_id, university_id, faculty_name, contact_phone, contact_email, location_id, head_of_faculty)

    # CREATE TABLE IF NOT EXISTS Location


def generate_and_insert_educationLevel():
    education_levels = [
        (1, 'Bachelors', 'Level 6', 'Description for Bachelor', 180),
        (2, 'Masters', 'Level 7', 'Description for Master', 120),
        (3, 'Phd', 'Level 8', 'Description for Doctor', 240),
        (4, 'Associates Degree', 'Level 6', 'Description for Associate', 90),
        (5, 'Post Graduate Diploma', 'Level 7', 'Description for Post Graduate Diploma', 60),
        (6, 'Under Graduate Diploma', 'Level 6', 'Description for Under Graduate Diploma', 120),
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO EducationLevel (level_id, level_name, level, description, ects_requirements) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, education_levels)
    connection.commit()
    print(f"Inserted {len(education_levels)} records into the EducationLevel table.")



def generate_and_insert_degree():

    degrees = [
        (1, 1, 'Bachelor of Arts'),
        (2, 1, 'Bachelor of Science'),
        (3, 1, 'Bachelor of Law'),
        (4, 1, 'Bachelor of Medicine'),
        (5, 1, 'Bachelor of Engineering'),
        (6, 1, 'Bachelor of Architecture'),
        (7, 2, 'Master of Arts'),
        (8, 2, 'Master of Science'),
        (9, 2, 'Master of Law'),
        (10, 2, 'Master of Medicine'),
        (11, 2, 'Master of Engineering'),
        (12, 2, 'Master of Architecture'),
        (13, 3, 'Ph.D. in Arts'),
        (14, 3, 'Ph.D. in Science'),
        (15, 3, 'Ph.D. in Law'),
        (16, 3, 'Ph.D. in Medicine'),
        (17, 3, 'Ph.D. in Engineering'),
        (18, 3, 'Ph.D. in Architecture'),
        (19, 4, 'Associate Degree in Arts'),
        (20, 4, 'Associate Degree in Science'),
        (21, 5, 'Post Graduate Diploma in Business'),
        (22, 5, 'Post Graduate Diploma in Law'),
        (23, 5, 'Post Graduate Diploma in Architecture'),
        (24, 6, 'Undergraduate Diploma in Law'),
        (25, 6, 'Undergraduate Diploma in Business'),
        (26, 6, 'Undergraduate Diploma in IT'),
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Degree (degree_id, education_level_id, degree_name) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, degrees)
    connection.commit()
    print(f"Inserted {len(degrees)} records into the EducationLevel table.")




def generate_and_insert_Program():

    programs_list = [
        (1, 2, 1, 'Masters in Advanced Information Systems', 2022, 'Remote', '4', 'Full Time', 'Technology'),
        (2, 2, 1, 'Masters in Business Analytics', 2023, 'Hybrid', '5', 'Part Time', 'Business & Finance'),
        (3, 3, 2, 'Ph.D. in Environmental Engineering Research', 2021, 'Physical', '8', 'Full Time', 'Technology'),
        (4, 1, 3, 'Bachelor of Arts in Political Science and International Relations', 2022, 'Remote', '6', 'Full Time', 'Arts'),
        (5, 2, 4, 'Master of Law in Intellectual Property', 2023, 'Physical', '4', 'Part Time', 'Law'),
        (6, 4, 5, 'Associate Degree in Business and Finance', 2022, 'Hybrid', '2', 'Full Time', 'Business & Finance'),
        (7, 2, 1, 'Masters in Technology Management', 2023, 'Remote', '5', 'Part Time', 'Technology'),
        (8, 2, 2, 'Masters in Marketing Analytics', 2022, 'Physical', '4', 'Full Time', 'Business & Finance'),
        (9, 3, 3, 'Ph.D. in Civil Engineering Structures', 2021, 'Hybrid', '7', 'Part Time', 'Technology'),
        (10, 1, 4, 'Bachelor of Arts in English Literature', 2022, 'Physical', '6', 'Full Time', 'Arts'),
        (11, 2, 5, 'Master of Science in Criminal Law', 2023, 'Remote', '4', 'Part Time', 'Law'),
        (12, 4, 1, 'Associate Degree in IT Management', 2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (13, 2, 2, 'Masters in Financial Management', 2023, 'Physical', '5', 'Full Time', 'Business & Finance'),
        (14, 3, 3, 'Ph.D. in Renewable Energy Engineering', 2021, 'Hybrid', '8', 'Part Time', 'Technology'),
        (15, 1, 4, 'Bachelor of Arts in History', 2022, 'Remote', '6', 'Full Time', 'Arts'),
        (16, 2, 5, 'Master of Law in International Human Rights', 2023, 'Physical', '4', 'Part Time', 'Law'),
        (17, 4, 1, 'Associate Degree in Computer Science', 2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (18, 2, 1, 'Masters in Data Science', 2023, 'Remote', '4', 'Part Time', 'Technology'),
        (19, 3, 2, 'Ph.D. in Aerospace Engineering', 2021, 'Physical', '7', 'Full Time', 'Technology'),
        (20, 1, 3, 'Bachelor of Arts in Sociology', 2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (21, 2, 4, 'Master of Law in Environmental Law', 2023, 'Remote', '4', 'Part Time', 'Law'),
        (22, 4, 5, 'Associate Degree in Business Administration', 2022, 'Physical', '2', 'Full Time', 'Business & Finance'),
        (23, 2, 1, 'Masters in Information Technology', 2023, 'Hybrid', '5', 'Full Time', 'Technology'),
        (24, 2, 2, 'Masters in Human Resource Management', 2022, 'Remote', '4', 'Part Time', 'Business & Finance'),
        (25, 3, 3, 'Ph.D. in Mechanical Engineering', 2021, 'Physical', '8', 'Full Time', 'Technology'),
        (26, 1, 4, 'Bachelor of Arts in Psychology', 2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (27, 2, 5, 'Master of Law in Corporate Law', 2023, 'Remote', '4', 'Part Time', 'Law'),
        (28, 4, 1, 'Associate Degree in Software Development', 2022, 'Physical', '2', 'Full Time', 'Technology'),
        (29, 2, 1, 'Masters in Business Administration', 2023, 'Hybrid', '5', 'Part Time', 'Business & Finance'),
        (30, 3, 2, 'Ph.D. in Electrical Engineering', 2021, 'Physical', '7', 'Full Time', 'Technology'),
        (31, 1, 3, 'Bachelor of Arts in Philosophy', 2022, 'Remote', '6', 'Full Time', 'Arts'),
        (32, 2, 4, 'Master of Law in Intellectual Property Law', 2023, 'Physical', '4', 'Part Time', 'Law'),
        (33, 4, 5, 'Associate Degree in Network Security', 2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (34, 2, 1, 'Masters in Marketing Management', 2023, 'Remote', '4', 'Part Time', 'Business & Finance'),
        (35, 3, 3, 'Ph.D. in Computer Engineering', 2021, 'Hybrid', '8', 'Full Time', 'Technology'),
        (36, 1, 4, 'Bachelor of Arts in Creative Writing', 2022, 'Physical', '6', 'Full Time', 'Arts'),
        (37, 2, 5, 'Master of Law in Criminal Law', 2023, 'Remote', '4', 'Part Time', 'Law'),
        (38, 4, 1, 'Associate Degree in Mobile App Development', 2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (39, 2, 2, 'Masters in Financial Analysis', 2023, 'Physical', '5', 'Full Time', 'Business & Finance'),
        (40, 3, 3, 'Ph.D. in Software Engineering', 2021, 'Hybrid', '7', 'Part Time', 'Technology'),
        (41, 1, 4, 'Bachelor of Arts in Political Science', 2022, 'Remote', '6', 'Full Time', 'Arts'),
        (42, 2, 5, 'Master of Law in International Business Law', 2023, 'Physical', '4', 'Part Time', 'Law'),
        (43, 4, 1, 'Associate Degree in Information Technology Management', 2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (44, 2, 1, 'Masters in Business and IT', 2023, 'Remote', '5', 'Part Time', 'Business & Finance'),
        (45, 3, 2, 'Ph.D. in Artificial Intelligence', 2021, 'Physical', '8', 'Full Time', 'Technology'),
        (46, 1, 3, 'Bachelor of Arts in Economics', 2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (47, 2, 4, 'Master of Law in Environmental Law and Policy', 2023, 'Remote', '4', 'Part Time', 'Law'),
        (48, 4, 5, 'Associate Degree in Business and Finance Administration', 2022, 'Physical', '2', 'Full Time', 'Business & Finance'),
        (49, 2, 1, 'Masters in Information Systems Management', 2023, 'Hybrid', '4', 'Part Time', 'Technology'),
        (50, 2, 2, 'Masters in Human Resource Development', 2022, 'Physical', '5', 'Full Time', 'Business & Finance')
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Program (program_id, awarded_degree, faculty_id, program_name, year_started, teaching_type, semesters, pace, subject_type) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, programs_list)
    connection.commit()
    print(f"Inserted {len(programs_list)} records into the EducationLevel table.")



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
