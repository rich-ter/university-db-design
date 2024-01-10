# pip install mysql-connector-python & faker
from mysql.connector import connect, Error
import mysql.connector
from faker import Faker
import random

fake = Faker('el_GR')  # Set the locale to Greek (Greece)

database_name = "school_database"

create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database=database_name
)

cursor = connection.cursor()

cursor.execute(create_db_query)
cursor.execute(f"USE {database_name}")


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
        pace ENUM('Full Time', 'Part Time') NOT NULL,
        subject_type ENUM(
        'Business & Finance',
        'Technology',
        'Law',
        'Arts',
        'Architecture'),
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
        description varchar, 
        FOREIGN KEY (program_id) REFERENCES Program(program_id)
    );

    CREATE TABLE IF NOT EXISTS Modules (
        module_id INT PRIMARY KEY,
        program_term_id INT NOT NULL,
        module_name VARCHAR(255) NOT NULL,
        module_subject ENUM(
          'Financial Management', 'Accounting Principles', 'Business Ethics', 'Marketing Strategies', 'Entrepreneurship', 
          'Front-end Development', 'Back-end Development', 'Database Management', 'Mobile App Development', 'Cybersecurity', 
          'Criminal Law', 'Contract Law', 'Constitutional Law', 'International Law', 'Legal Research and Writing', 
          'Fine Arts', 'Performing Arts', 'Visual Arts', 'Art History', 'Creative Writing', 
          'Architectural Design', 'Structural Engineering', 'Urban Planning', 'Sustainable Architecture', 'History of Architecture' 
        ),
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
        FOREIGN KEY (company_id) REFERENCESs Company(company_id),
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
    insert_query = "INSERT INTO Location (location_id, address, city, postcode) VALUES (%s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, locations)
        connection.commit()
        print(f"Inserted {len(locations)} records into the Location table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

    return location_ids

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

# this is not finished yet
def generate_and_insert_faculties():
    faculties = [
        (1, 1, 'NKUA Faculty of Arts', 5551234,
         'arts_head@example.com', 11, 'Head of NKUA Faculty of Arts'),
        (2, 1, 'NKUA Faculty of Sciences', 5555678,
         'sciences_head@example.com', 12, 'Head of NKUA Faculty of Sciences'),
        (3, 1, 'NKUA Faculty of Law', 5559876,
         'law_head@example.com', 13, 'Head of NKUA Faculty of Law'),
        (4, 1, 'NKUA Faculty of Medicine', 5554321,
         'medicine_head@example.com', 14, 'Head of NKUA Faculty of Medicine'),
        (5, 1, 'NKUA Faculty of Engineering', 5558765,
         'engineering_head@example.com', 15, 'Head of NKUA Faculty of Engineering'),
        (6, 1, 'NKUA Faculty of Architecture', 5553456,
         'architecture_head@example.com', 16, 'Head of NKUA Faculty of Architecture'),

        (7, 2, 'NTUA School of Civil Engineering', 5552345,
         'civil_eng_head@example.com', 17, 'Head of NTUA School of Civil Engineering'),
        (8, 2, 'NTUA School of Mechanical Engineering', 5558765,
         'mechanical_eng_head@example.com', 18, 'Head of NTUA School of Mechanical Engineering'),
        (9, 2, 'NTUA School of Electrical and Computer Engineering', 5555432,
         'ece_head@example.com', 19, 'Head of NTUA School of Electrical and Computer Engineering'),
        (10, 2, 'NTUA School of Chemical Engineering', 5557890,
         'chemical_eng_head@example.com', 20, 'Head of NTUA School of Chemical Engineering'),
        (11, 2, 'NTUA School of Rural and Surveying Engineering', 5552109,
         'rural_eng_head@example.com', 21, 'Head of NTUA School of Rural and Surveying Engineering'),
        (12, 2, 'NTUA School of Applied Mathematical and Physical Sciences', 5553210,
         'applied_sciences_head@example.com', 22, 'Head of NTUA School of Applied Mathematical and Physical Sciences'),

        (13, 3, 'AUEB Department of Business Administration', 5554321,
         'business_admin_head@example.com', 23, 'Head of AUEB Department of Business Administration'),
        (14, 3, 'AUEB Department of Economics', 5555678,
         'economics_head@example.com', 24, 'Head of AUEB Department of Economics'),
        (15, 3, 'AUEB Department of International and European Economic Studies', 5557890,
         'intl_econ_studies_head@example.com', 25, 'Head of AUEB Department of International and European Economic Studies'),
        (16, 3, 'AUEB Department of Marketing and Communication', 5558765,
         'marketing_comm_head@example.com', 26, 'Head of AUEB Department of Marketing and Communication'),
        (17, 3, 'AUEB Department of Accounting and Finance', 5559876,
         'accounting_finance_head@example.com', 27, 'Head of AUEB Department of Accounting and Finance'),
        (18, 3, 'AUEB Department of Management Science and Technology', 5555432,
         'management_science_head@example.com', 28, 'Head of AUEB Department of Management Science and Technology'),

        (19, 4, 'UoP Department of Banking and Financial Management', 5553456,
         'banking_finance_head@example.com', 29, 'Head of UoP Department of Banking and Financial Management'),
        (20, 4, 'UoP Department of Business Administration', 5552109,
         'uop_business_admin_head@example.com', 30, 'Head of UoP Department of Business Administration'),
        (21, 4, 'UoP Department of Maritime Studies', 5553210,
         'maritime_studies_head@example.com', 31, 'Head of UoP Department of Maritime Studies'),
        (22, 4, 'UoP Department of International and European Studies', 5554321,
         'intl_european_studies_head@example.com', 32, 'Head of UoP Department of International and European Studies'),
        (23, 4, 'UoP Department of Digital Systems', 5555678,
         'digital_systems_head@example.com', 33, 'Head of UoP Department of Digital Systems'),

        (24, 5, 'Panteion Department of Political Science and History', 5557890,
         'political_history_head@example.com', 34, 'Head of Panteion Department of Political Science and History'),
        (25, 5, 'Panteion Department of Sociology', 5558765,
         'sociology_head@example.com', 35, 'Head of Panteion Department of Sociology'),
        (26, 5, 'Panteion Department of Social Policy', 5555432,
         'social_policy_head@example.com', 36, 'Head of Panteion Department of Social Policy'),
        (27, 5, 'Panteion Department of Communication, Media, and Culture', 5559876,
         'media_culture_head@example.com', 37, 'Head of Panteion Department of Communication, Media, and Culture'),
        (28, 5, 'Panteion Department of Psychology', 5552109,
         'psychology_head@example.com', 38, 'Head of Panteion Department of Psychology'),

        (29, 6, 'Harokopio Department of Dietetics and Nutritional Science', 5553210,
         'dietetics_nutrition_head@example.com', 39, 'Head of Harokopio Department of Dietetics and Nutritional Science'),
        (30, 6, 'Harokopio Department of Informatics and Telematics', 5554321,
         'informatics_telematics_head@example.com', 40, 'Head of Harokopio Department of Informatics and Telematics'),
        (31, 6, 'Harokopio Department of Home Economics and Ecology', 5555678,
         'home_economics_ecology_head@example.com', 41, 'Head of Harokopio Department of Home Economics and Ecology'),
        (32, 6, 'Harokopio Department of Geography', 5557890,
         'geography_head@example.com', 42, 'Head of Harokopio Department of Geography'),

        (33, 7, 'AUA School of Agricultural Sciences', 5559876,
         'agricultural_sciences_head@example.com', 43, 'Head of AUA School of Agricultural Sciences'),
        (34, 7, 'AUA School of Food, Biotechnology, and Development', 5558765,
         'food_biotech_head@example.com', 44, 'Head of AUA School of Food, Biotechnology, and Development'),
        (35, 7, 'AUA School of Natural Resources and Agricultural Engineering', 5555432,
         'natural_resources_eng_head@example.com', 45, 'Head of AUA School of Natural Resources and Agricultural Engineering'),

        (36, 8, 'UniWA Department of Business Administration', 5552109,
         'uniwa_business_admin_head@example.com', 46, 'Head of UniWA Department of Business Administration'),
        (37, 8, 'UniWA Department of Informatics and Computer Engineering', 5553210,
         'informatics_comp_eng_head@example.com', 47, 'Head of UniWA Department of Informatics and Computer Engineering'),
        (38, 8, 'UniWA Department of Civil Engineering', 5554321,
         'civil_eng_head@example.com', 48, 'Head of UniWA Department of Civil Engineering'),
        (39, 8, 'UniWA Department of Electrical and Computer Engineering', 5555678,
         'ece_head@example.com', 49, 'Head of UniWA Department of Electrical and Computer Engineering'),

        (40, 9, 'UoP Department of Computer Science and Technology', 5557890,
         'uop_comp_sci_head@example.com', 50, 'Head of UoP Department of Computer Science and Technology'),
        (41, 9, 'UoP Department of Environmental and Natural Resources Management', 5558765,
         'env_natural_resources_head@example.com', 51, 'Head of UoP Department of Environmental and Natural Resources Management'),
        (42, 9, 'UoP Department of Economics, Sports Science, and Tourism', 5555432,
         'econ_sports_tourism_head@example.com', 52, 'Head of UoP Department of Economics, Sports Science, and Tourism'),
        (43, 9, 'UoP Department of History, Archaeology, and Cultural Resources Management', 5559876,
         'history_archaeology_head@example.com', 53, 'Head of UoP Department of History, Archaeology, and Cultural Resources Management'),

        (44, 10, 'HOU School of Science and Technology', 5552109,
         'hou_science_tech_head@example.com', 54, 'Head of HOU School of Science and Technology'),
        (45, 10, 'HOU School of Humanities', 5553210,
         'hou_humanities_head@example.com', 55, 'Head of HOU School of Humanities'),
        (46, 10, 'HOU School of Social Sciences', 5554321,
         'hou_social_sciences_head@example.com', 56, 'Head of HOU School of Social Sciences'),
        (47, 10, 'HOU School of Applied Arts', 5555678,
         'hou_applied_arts_head@example.com', 57, 'Head of HOU School of Applied Arts'),

    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Faculty(faculty_id, university_id, faculty_name, contact_phone, contact_email, location_id, head_of_faculty) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, faculties)
    connection.commit()
    print(
        f"Inserted {len(faculties)} records into the Faculty table.")

def generate_and_insert_educationLevel():
    education_levels = [
        (1, 'Bachelors', 'Level 6', 'Description for Bachelor', 180),
        (2, 'Masters', 'Level 7', 'Description for Master', 120),
        (3, 'Phd', 'Level 8', 'Description for Doctor', 240),
        (4, 'Associates', 'Level 6', 'Description for Associate', 90),
        (5, 'Post Graduate Diploma', 'Level 7',
         'Description for Post Graduate Diploma', 60),
        (6, 'Under Graduate Diploma', 'Level 6',
         'Description for Under Graduate Diploma', 120),
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO EducationLevel (level_id, level_name, level, description, ects_requirements) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, education_levels)
    connection.commit()
    print(
        f"Inserted {len(education_levels)} records into the EducationLevel table.")

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

    insert_query = "INSERT INTO Degree (degree_id, education_level_id, degree_name) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, degrees)
    connection.commit()
    print(f"Inserted {len(degrees)} records into the EducationLevel table.")

# SOS! NEED TO CHANGE THE PROGRAMS TO INCLUDE FACULTIES FROM 19-23 WHICH IS THE UOP FACULTY ID
# DO THE SAME FOR OTHER PROGRAMS - DIVERSE THE 3RD ID BY A LOT.
def generate_and_insert_Program():

    programs_list = [
        (1, 8, 23, 'Masters in Advanced Information Systems',
         2022, 'Remote', '4', 'Full Time', 'Technology'),
        (2, 8, 1, 'Masters in Business Analytics', 2023,
         'Hybrid', '5', 'Part Time', 'Business & Finance'),
        (3, 17, 2, 'Ph.D. in Environmental Engineering Research',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (4, 1, 3, 'Bachelor of Arts in Political Science and International Relations',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (5, 9, 4, 'Master of Law in Intellectual Property',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (6, 20, 5, 'Associate Degree in Business and Finance',
         2022, 'Hybrid', '2', 'Full Time', 'Business & Finance'),
        (7, 8, 1, 'Masters in Technology Management',
         2023, 'Remote', '5', 'Part Time', 'Technology'),
        (8, 8, 2, 'Masters in Marketing Analytics', 2022,
         'Physical', '4', 'Full Time', 'Business & Finance'),
        (9, 17, 3, 'Ph.D. in Civil Engineering Structures',
         2021, 'Hybrid', '7', 'Part Time', 'Technology'),
        (10, 1, 4, 'Bachelor of Arts in English Literature',
         2022, 'Physical', '6', 'Full Time', 'Arts'),
        (11, 9, 5, 'Master of Science in Criminal Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (12, 20, 1, 'Associate Degree in IT Management',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (13, 8, 2, 'Masters in Financial Management', 2023,
         'Physical', '5', 'Full Time', 'Business & Finance'),
        (14, 17, 3, 'Ph.D. in Renewable Energy Engineering',
         2021, 'Hybrid', '8', 'Part Time', 'Technology'),
        (15, 1, 47, 'Bachelor of Arts in History',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (16, 9, 5, 'Master of Law in International Human Rights',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (17, 20, 1, 'Associate Degree in Computer Science',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (18, 8, 1, 'Masters in Data Science', 2023,
         'Remote', '4', 'Part Time', 'Technology'),
        (19, 17, 2, 'Ph.D. in Aerospace Engineering',
         2021, 'Physical', '7', 'Full Time', 'Technology'),
        (20, 1, 3, 'Bachelor of Arts in Sociology',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (21, 9, 4, 'Master of Law in Environmental Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (22, 20, 5, 'Associate Degree in Business Administration',
         2022, 'Physical', '2', 'Full Time', 'Business & Finance'),
        (23, 8, 23, 'Masters in Information Technology',
         2023, 'Hybrid', '5', 'Full Time', 'Technology'),
        (24, 8, 22, 'Masters in Human Resource Management', 2022,
         'Remote', '4', 'Part Time', 'Business & Finance'),
        (25, 17, 3, 'Ph.D. in Mechanical Engineering',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (26, 1, 4, 'Bachelor of Arts in Psychology',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (27, 9, 5, 'Master of Law in Corporate Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (28, 20, 23, 'Associate Degree in Software Development',
         2022, 'Physical', '2', 'Full Time', 'Technology'),
        (29, 8, 2, 'Masters in Business Administration', 2023,
         'Hybrid', '5', 'Part Time', 'Business & Finance'),
        (30, 17, 3, 'Ph.D. in Electrical Engineering',
         2021, 'Physical', '7', 'Full Time', 'Technology'),
        (31, 1, 4, 'Bachelor of Arts in Philosophy',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (32, 9, 5, 'Master of Law in Intellectual Property Law',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (33, 20, 1, 'Associate Degree in Network Security',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (34, 8, 2, 'Masters in Marketing Management', 2023,
         'Remote', '4', 'Part Time', 'Business & Finance'),
        (35, 17, 3, 'Ph.D. in Computer Engineering',
         2021, 'Hybrid', '8', 'Full Time', 'Technology'),
        (36, 1, 4, 'Bachelor of Arts in Creative Writing',
         2022, 'Physical', '6', 'Full Time', 'Arts'),
        (37, 9, 5, 'Master of Law in Criminal Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (38, 20, 23, 'Associate Degree in Mobile App Development',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (39, 8, 2, 'Masters in Financial Analysis', 2023,
         'Physical', '5', 'Full Time', 'Business & Finance'),
        (40, 17, 3, 'Ph.D. in Software Engineering',
         2021, 'Hybrid', '7', 'Part Time', 'Technology'),
        (41, 1, 4, 'Bachelor of Arts in Political Science',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (42, 9, 5, 'Master of Law in International Business Law',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (43, 20, 23, 'Associate Degree in Information Technology Management',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (44, 8, 1, 'Masters in Business and IT', 2023,
         'Remote', '5', 'Part Time', 'Business & Finance'),
        (45, 17, 2, 'Ph.D. in Artificial Intelligence',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (46, 1, 3, 'Bachelor of Arts in Economics',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (47, 9, 4, 'Master of Law in Environmental Law and Policy',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (48, 20, 5, 'Associate Degree in Business and Finance Administration',
         2022, 'Physical', '2', 'Full Time', 'Business & Finance'),
        (49, 8, 1, 'Masters in Information Systems Management',
         2023, 'Hybrid', '4', 'Part Time', 'Technology'),
        (50, 8, 2, 'Masters in Human Resource Development', 2022,
         'Physical', '5', 'Full Time', 'Business & Finance'),
        (51, 2, 23, 'Bachelor of Science in Computer Science',
         2022, 'Physical', '8', 'Full Time', 'Technology'),
        (52, 2, 7, 'Bachelor of Science in Biology',
         2023, 'Hybrid', '8', 'Full Time', 'Technology'),
        (53, 1, 8, 'Bachelor of Arts in Media Studies',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (54, 3, 9, 'Bachelor of Law in Corporate Law',
         2023, 'Physical', '6', 'Full Time', 'Law'),
        (55, 5, 10, 'Bachelor of Engineering in Mechanical Engineering',
         2022, 'Hybrid', '8', 'Full Time', 'Technology'),
        (56, 6, 6, 'Bachelor of Architecture in Urban Design',
         2023, 'Remote', '10', 'Full Time', 'Architecture'),
        (57, 2, 7, 'Bachelor of Science in Environmental Technology',
         2022, 'Physical', '8', 'Part Time', 'Technology'),
        (58, 1, 8, 'Bachelor of Arts in Psychology',
         2023, 'Hybrid', '6', 'Full Time', 'Arts'),
        (59, 3, 9, 'Bachelor of Law in International Law',
         2022, 'Remote', '6', 'Part Time', 'Law'),
        (60, 5, 10, 'Bachelor of Engineering in Civil Engineering',
         2023, 'Physical', '8', 'Full Time', 'Technology'),
        (61, 2, 23, 'Bachelor of Science in Mathematics',
         2022, 'Hybrid', '8', 'Part Time', 'Technology'),
        (62, 1, 7, 'Bachelor of Arts in Sociology',
         2023, 'Remote', '6', 'Full Time', 'Arts'),
        (63, 3, 8, 'Bachelor of Law in Human Rights Law',
         2022, 'Physical', '6', 'Full Time', 'Law'),
        (64, 5, 9, 'Bachelor of Engineering in Electrical Engineering',
         2023, 'Hybrid', '8', 'Full Time', 'Technology'),
        (65, 6, 10, 'Bachelor of Architecture in Landscape Architecture',
         2022, 'Remote', '10', 'Part Time', 'Architecture'),
        (66, 2, 6, 'Bachelor of Science in Physics',
         2023, 'Physical', '8', 'Full Time', 'Technology'),
        (67, 1, 7, 'Bachelor of Arts in Anthropology',
         2022, 'Hybrid', '6', 'Part Time', 'Arts'),
        (68, 3, 8, 'Bachelor of Law in Environmental Law',
         2023, 'Remote', '6', 'Full Time', 'Law'),
        (69, 5, 9, 'Bachelor of Engineering in Aerospace Engineering',
         2022, 'Physical', '8', 'Full Time', 'Technology'),
        (70, 6, 10, 'Bachelor of Architecture in Sustainable Architecture',
         2023, 'Hybrid', '10', 'Part Time', 'Architecture'),
        (71, 2, 6, 'Bachelor of Science in Chemistry',
         2022, 'Remote', '8', 'Full Time', 'Technology'),
        (72, 1, 7, 'Bachelor of Arts in Fine Arts',
         2023, 'Physical', '6', 'Part Time', 'Arts'),
        (73, 3, 8, 'Bachelor of Law in Patent Law',
         2022, 'Hybrid', '6', 'Full Time', 'Law'),
        (74, 5, 9, 'Bachelor of Engineering in Biomedical Engineering',
         2023, 'Remote', '8', 'Part Time', 'Technology'),
        (75, 6, 10, 'Bachelor of Architecture in Interior Architecture',
         2022, 'Physical', '10', 'Full Time', 'Architecture'),
        (76, 2, 6, 'Bachelor of Science in Geology',
         2023, 'Hybrid', '8', 'Full Time', 'Technology'),
        (77, 1, 7, 'Bachelor of Arts in Music',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (78, 3, 8, 'Bachelor of Law in Criminal Law',
         2023, 'Physical', '6', 'Part Time', 'Law'),
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Program (program_id, awarded_degree, faculty_id, program_name, year_started, teaching_type, semesters, pace, subject_type) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)"
    cursor.executemany(insert_query, programs_list)
    connection.commit()
    print(
        f"Inserted {len(programs_list)} records into the Program table.")

def generate_and_insert_Programterm():

    program_terms = [
        (1, 1, '2023-01-01', '2023-12-31', 100,
         '2023 cohort for Masters in Advanced Information Systems'),
        (2, 2, '2023-09-01', '2024-05-31', 80,
         'Fall 2023 cohort for Masters in Business Analytics'),
        (3, 3, '2023-09-01', '2027-05-31', 50,
         '2023 cohort for Ph.D. in Environmental Engineering Research'),
        (4, 4, '2023-09-01', '2026-05-31', 120,
         '2023 cohort for Bachelor of Arts in Political Science and International Relations'),
        (5, 5, '2023-09-01', '2024-05-31', 75,
         'Fall 2023 cohort for Master of Law in Intellectual Property'),
        (6, 6, '2023-01-01', '2023-12-31', 60,
         '2023 cohort for Associate Degree in Business and Finance'),
        (7, 7, '2023-09-01', '2024-05-31', 85,
         'Fall 2023 cohort for Masters in Technology Management'),
        (8, 8, '2023-01-01', '2023-12-31', 90,
         '2023 cohort for Masters in Marketing Analytics'),
        (9, 9, '2023-09-01', '2027-05-31', 40,
         '2023 cohort for Ph.D. in Civil Engineering Structures'),
        (10, 10, '2023-09-01', '2026-05-31', 110,
         '2023 cohort for Bachelor of Arts in English Literature'),
        (11, 1, '2024-01-01', '2024-12-31', 100,
         '2024 cohort for Masters in Advanced Information Systems'),
        (12, 2, '2024-09-01', '2025-05-31', 80,
         'Fall 2024 cohort for Masters in Business Analytics'),
        (13, 3, '2024-09-01', '2028-05-31', 50,
         '2024 cohort for Ph.D. in Environmental Engineering Research'),
        (14, 4, '2024-09-01', '2027-05-31', 120,
         '2024 cohort for Bachelor of Arts in Political Science and International Relations'),
        (15, 5, '2024-09-01', '2025-05-31', 75,
         'Fall 2024 cohort for Master of Law in Intellectual Property'),
        (16, 6, '2024-01-01', '2024-12-31', 60,
         '2024 cohort for Associate Degree in Business and Finance'),
        (17, 7, '2024-09-01', '2025-05-31', 85,
         'Fall 2024 cohort for Masters in Technology Management'),
        (18, 8, '2024-01-01', '2024-12-31', 90,
         '2024 cohort for Masters in Marketing Analytics'),
        (19, 9, '2024-09-01', '2028-05-31', 40,
         '2024 cohort for Ph.D. in Civil Engineering Structures'),
        (20, 10, '2024-09-01', '2027-05-31', 110,
         '2024 cohort for Bachelor of Arts in English Literature'),
        (21, 1, '2025-01-01', '2025-12-31', 100,
         '2025 cohort for Masters in Advanced Information Systems'),
        (22, 2, '2025-09-01', '2026-05-31', 80,
         'Fall 2025 cohort for Masters in Business Analytics'),
        (23, 3, '2025-09-01', '2029-05-31', 50,
         '2025 cohort for Ph.D. in Environmental Engineering Research'),
        (24, 4, '2025-09-01', '2028-05-31', 120,
         '2025 cohort for Bachelor of Arts in Political Science and International Relations'),
        (25, 5, '2025-09-01', '2026-05-31', 75,
         'Fall 2025 cohort for Master of Law in Intellectual Property'),
        (26, 6, '2025-01-01', '2025-12-31', 60,
         '2025 cohort for Associate Degree in Business and Finance'),
        (27, 7, '2025-09-01', '2026-05-31', 85,
         'Fall 2025 cohort for Masters in Technology Management'),
        (28, 8, '2025-01-01', '2025-12-31', 90,
         '2025 cohort for Masters in Marketing Analytics'),
        (29, 9, '2026-09-01', '2030-05-31', 40,
         '2026 cohort for Ph.D. in Civil Engineering Structures'),
        (30, 10, '2026-09-01', '2030-05-31', 110,
         '2026 cohort for Bachelor of Arts in English Literature'),
        (31, 1, '2026-01-01', '2026-12-31', 100,
         '2026 cohort for Masters in Advanced Information Systems'),
        (32, 2, '2026-09-01', '2027-05-31', 80,
         'Fall 2026 cohort for Masters in Business Analytics'),
        (33, 3, '2026-09-01', '2030-05-31', 50,
         '2026 cohort for Ph.D. in Environmental Engineering Research'),
        (34, 4, '2026-09-01', '2029-05-31', 120,
         '2026 cohort for Bachelor of Arts in Political Science and International Relations'),
        (35, 5, '2026-09-01', '2027-05-31', 75,
         'Fall 2026 cohort for Master of Law in Intellectual Property'),
        (36, 6, '2026-01-01', '2026-12-31', 60,
         '2026 cohort for Associate Degree in Business and Finance'),
        (37, 7, '2026-09-01', '2027-05-31', 85,
         'Fall 2026 cohort for Masters in Technology Management'),
        (38, 8, '2026-01-01', '2026-12-31', 90,
         '2026 cohort for Masters in Marketing Analytics'),
        (39, 9, '2027-09-01', '2031-05-31', 40,
         '2027 cohort for Ph.D. in Civil Engineering Structures'),
        (40, 10, '2027-09-01', '2031-05-31', 110,
         '2027 cohort for Bachelor of Arts in English Literature'),
        (41, 1, '2027-01-01', '2027-12-31', 100,
         '2027 cohort for Masters in Advanced Information Systems'),
        (42, 2, '2027-09-01', '2028-05-31', 80,
         'Fall 2027 cohort for Masters in Business Analytics'),
        (43, 3, '2027-09-01', '2031-05-31', 50,
         '2027 cohort for Ph.D. in Environmental Engineering Research'),
        (44, 4, '2027-09-01', '2030-05-31', 120,
         '2027 cohort for Bachelor of Arts in Political Science and International Relations'),
        (45, 5, '2027-09-01', '2028-05-31', 75,
         'Fall 2027 cohort for Master of Law in Intellectual Property'),
        (46, 6, '2027-01-01', '2027-12-31', 60,
         '2027 cohort for Associate Degree in Business and Finance'),
        (47, 7, '2027-09-01', '2028-05-31', 85,
         'Fall 2027 cohort for Masters in Technology Management'),
        (48, 8, '2027-01-01', '2027-12-31', 90,
         '2027 cohort for Masters in Marketing Analytics'),
        (49, 9, '2028-09-01', '2032-05-31', 40,
         '2028 cohort for Ph.D. in Civil Engineering Structures'),
        (50, 10, '2028-09-01', '2032-05-31', 110,
         '2028 cohort for Bachelor of Arts in English Literature'),
        (51, 1, '2028-01-01', '2028-12-31', 100,
         '2028 cohort for Masters in Advanced Information Systems'),
        (52, 2, '2028-09-01', '2029-05-31', 80,
         'Fall 2028 cohort for Masters in Business Analytics'),
        (53, 3, '2028-09-01', '2032-05-31', 50,
         '2028 cohort for Ph.D. in Environmental Engineering Research'),
        (54, 4, '2028-09-01', '2031-05-31', 120,
         '2028 cohort for Bachelor of Arts in Political Science and International Relations'),
        (55, 5, '2028-09-01', '2029-05-31', 75,
         'Fall 2028 cohort for Master of Law in Intellectual Property'),
        (56, 6, '2028-01-01', '2028-12-31', 60,
         '2028 cohort for Associate Degree in Business and Finance'),
        (57, 7, '2028-09-01', '2029-05-31', 85,
         'Fall 2028 cohort for Masters in Technology Management'),
        (58, 8, '2028-01-01', '2028-12-31', 90,
         '2028 cohort for Masters in Marketing Analytics'),
        (59, 9, '2029-09-01', '2033-05-31', 40,
         '2029 cohort for Ph.D. in Civil Engineering Structures'),
        (60, 10, '2029-09-01', '2033-05-31', 110,
         '2029 cohort for Bachelor of Arts in English Literature'),
        (61, 1, '2029-01-01', '2029-12-31', 100,
         '2029 cohort for Masters in Advanced Information Systems'),
        (62, 2, '2029-09-01', '2030-05-31', 80,
         'Fall 2029 cohort for Masters in Business Analytics'),
        (63, 3, '2029-09-01', '2033-05-31', 50,
         '2029 cohort for Ph.D. in Environmental Engineering Research'),
        (64, 4, '2029-09-01', '2032-05-31', 120,
         '2029 cohort for Bachelor of Arts in Political Science and International Relations'),
        (65, 5, '2029-09-01', '2030-05-31', 75,
         'Fall 2029 cohort for Master of Law in Intellectual Property'),
        (66, 6, '2029-01-01', '2029-12-31', 60,
         '2029 cohort for Associate Degree in Business and Finance'),
        (67, 7, '2029-09-01', '2030-05-31', 85,
         'Fall 2029 cohort for Masters in Technology Management'),
        (68, 8, '2029-01-01', '2029-12-31', 90,
         '2029 cohort for Masters in Marketing Analytics'),
        (69, 9, '2030-09-01', '2034-05-31', 40,
         '2030 cohort for Ph.D. in Civil Engineering Structures'),
        (70, 10, '2030-09-01', '2034-05-31', 110,
         '2030 cohort for Bachelor of Arts in English Literature'),
        (71, 1, '2030-01-01', '2030-12-31', 100,
         '2030 cohort for Masters in Advanced Information Systems'),
        (72, 2, '2030-09-01', '2031-05-31', 80,
         'Fall 2030 cohort for Masters in Business Analytics'),
        (73, 3, '2030-09-01', '2034-05-31', 50,
         '2030 cohort for Ph.D. in Environmental Engineering Research'),
        (74, 4, '2030-09-01', '2033-05-31', 120,
         '2030 cohort for Bachelor of Arts in Political Science and International Relations'),
        (75, 5, '2030-09-01', '2031-05-31', 75,
         'Fall 2030 cohort for Master of Law in Intellectual Property'),
        (76, 6, '2030-01-01', '2030-12-31', 60,
         '2030 cohort for Associate Degree in Business and Finance'),
        (77, 7, '2030-09-01', '2031-05-31', 85,
         'Fall 2030 cohort for Masters in Technology Management'),
        (78, 8, '2030-01-01', '2030-12-31', 90,
         '2030 cohort for Masters in Marketing Analytics'),
        (79, 9, '2031-09-01', '2035-05-31', 40,
         '2031 cohort for Ph.D. in Civil Engineering Structures'),
        (80, 10, '2031-09-01', '2035-05-31', 110,
         '2031 cohort for Bachelor of Arts in English Literature'),
        (81, 1, '2031-01-01', '2031-12-31', 100,
         '2031 cohort for Masters in Advanced Information Systems'),
        (82, 2, '2031-09-01', '2032-05-31', 80,
         'Fall 2031 cohort for Masters in Business Analytics'),
        (83, 3, '2031-09-01', '2035-05-31', 50,
         '2031 cohort for Ph.D. in Environmental Engineering Research'),
        (84, 4, '2031-09-01', '2034-05-31', 120,
         '2031 cohort for Bachelor of Arts in Political Science and International Relations'),
        (85, 5, '2031-09-01', '2032-05-31', 75,
         'Fall 2031 cohort for Master of Law in Intellectual Property'),
        (86, 6, '2031-01-01', '2031-12-31', 60,
         '2031 cohort for Associate Degree in Business and Finance'),
        (87, 7, '2031-09-01', '2032-05-31', 85,
         'Fall 2031 cohort for Masters in Technology Management'),
        (88, 8, '2031-01-01', '2031-12-31', 90,
         '2031 cohort for Masters in Marketing Analytics'),
        (89, 9, '2032-09-01', '2036-05-31', 40,
         '2032 cohort for Ph.D. in Civil Engineering Structures'),
        (90, 10, '2032-09-01', '2036-05-31', 110,
         '2032 cohort for Bachelor of Arts in English Literature'),
        (91, 1, '2032-01-01', '2032-12-31', 100,
         '2032 cohort for Masters in Advanced Information Systems'),
        (92, 2, '2032-09-01', '2033-05-31', 80,
         'Fall 2032 cohort for Masters in Business Analytics'),
        (93, 3, '2032-09-01', '2036-05-31', 50,
         '2032 cohort for Ph.D. in Environmental Engineering Research'),
        (94, 4, '2032-09-01', '2035-05-31', 120,
         '2032 cohort for Bachelor of Arts in Political Science and International Relations'),
        (95, 5, '2032-09-01', '2033-05-31', 75,
         'Fall 2032 cohort for Master of Law in Intellectual Property'),
        (96, 6, '2032-01-01', '2032-12-31', 60,
         '2032 cohort for Associate Degree in Business and Finance'),
        (97, 7, '2032-09-01', '2033-05-31', 85,
         'Fall 2032 cohort for Masters in Technology Management'),
        (98, 8, '2032-01-01', '2032-12-31', 90,
         '2032 cohort for Masters in Marketing Analytics'),
        (99, 9, '2032-09-01', '2036-05-31', 40,
         '2032 cohort for Ph.D. in Civil Engineering Structures'),
        (100, 10, '2032-09-01', '2036-05-31', 110,
         '2032 cohort for Bachelor of Arts in English Literature'),
        (101, 1, '2033-01-01', '2033-12-31', 100,
         '2033 cohort for Masters in Advanced Information Systems'),
        (102, 2, '2033-09-01', '2034-05-31', 80,
         'Fall 2033 cohort for Masters in Business Analytics'),
        (103, 3, '2033-09-01', '2037-05-31', 50,
         '2033 cohort for Ph.D. in Environmental Engineering Research'),
        (104, 4, '2033-09-01', '2037-05-31', 120,
         '2033 cohort for Bachelor of Arts in Political Science and International Relations'),
        (105, 5, '2033-09-01', '2034-05-31', 75,
         'Fall 2033 cohort for Master of Law in Intellectual Property'),
        (106, 6, '2033-01-01', '2033-12-31', 60,
         '2033 cohort for Associate Degree in Business and Finance'),
        (107, 7, '2033-09-01', '2034-05-31', 85,
         'Fall 2033 cohort for Masters in Technology Management'),
        (108, 8, '2033-01-01', '2033-12-31', 90,
         '2033 cohort for Masters in Marketing Analytics'),
        (109, 9, '2033-09-01', '2037-05-31', 40,
         '2033 cohort for Ph.D. in Civil Engineering Structures'),
        (110, 10, '2033-09-01', '2037-05-31', 110,
         '2033 cohort for Bachelor of Arts in English Literature'),
        (111, 1, '2034-01-01', '2034-12-31', 100,
         '2034 cohort for Masters in Advanced Information Systems'),
        (112, 2, '2034-09-01', '2035-05-31', 80,
         'Fall 2034 cohort for Masters in Business Analytics'),
        (113, 3, '2034-09-01', '2038-05-31', 50,
         '2034 cohort for Ph.D. in Environmental Engineering Research'),
        (114, 4, '2034-09-01', '2038-05-31', 120,
         '2034 cohort for Bachelor of Arts in Political Science and International Relations'),
        (115, 11, '2034-09-01', '2038-05-31',
         75, 'Fall 2034 cohort for Program 11'),
        (116, 12, '2034-01-01', '2034-12-31', 60, '2034 cohort for Program 12'),
        (117, 13, '2034-09-01', '2035-05-31',
         85, 'Fall 2034 cohort for Program 13'),
        (118, 14, '2034-01-01', '2034-12-31', 90, '2034 cohort for Program 14'),
        (119, 15, '2034-09-01', '2038-05-31', 40, '2034 cohort for Program 15'),
        (120, 16, '2034-09-01', '2038-05-31', 110, '2034 cohort for Program 16'),
        (121, 17, '2035-01-01', '2035-12-31', 100, '2035 cohort for Program 17'),
        (122, 18, '2035-09-01', '2036-05-31',
         80, 'Fall 2035 cohort for Program 18'),
        (123, 19, '2035-09-01', '2039-05-31', 50, '2035 cohort for Program 19'),
        (124, 20, '2035-09-01', '2039-05-31', 120, '2035 cohort for Program 20'),
        (125, 21, '2035-09-01', '2036-05-31',
         75, 'Fall 2035 cohort for Program 21'),
        (126, 22, '2035-01-01', '2035-12-31', 60, '2035 cohort for Program 22'),
        (127, 23, '2035-09-01', '2036-05-31',
         85, 'Fall 2035 cohort for Program 23'),
        (128, 24, '2035-01-01', '2035-12-31', 90, '2035 cohort for Program 24'),
        (129, 25, '2035-09-01', '2039-05-31', 40, '2035 cohort for Program 25'),
        (130, 26, '2035-09-01', '2039-05-31', 110, '2035 cohort for Program 26'),
        (131, 27, '2036-01-01', '2036-12-31', 100, '2036 cohort for Program 27'),
        (132, 28, '2036-09-01', '2037-05-31',
         80, 'Fall 2036 cohort for Program 28'),
        (133, 29, '2036-09-01', '2040-05-31', 50, '2036 cohort for Program 29'),
        (134, 30, '2036-09-01', '2040-05-31', 120, '2036 cohort for Program 30'),
        (135, 31, '2036-09-01', '2040-05-31', 75, '2036 cohort for Program 31'),
        (136, 32, '2036-01-01', '2036-12-31', 60, '2036 cohort for Program 32'),
        (137, 33, '2036-09-01', '2037-05-31',
         85, 'Fall 2036 cohort for Program 33'),
        (138, 34, '2036-01-01', '2036-12-31', 90, '2036 cohort for Program 34'),
        (139, 35, '2036-09-01', '2040-05-31', 40, '2036 cohort for Program 35'),
        (140, 36, '2036-09-01', '2040-05-31', 110, '2036 cohort for Program 36'),
        (141, 37, '2037-01-01', '2037-12-31', 100, '2037 cohort for Program 37'),
        (142, 38, '2037-09-01', '2038-05-31',
         80, 'Fall 2037 cohort for Program 38'),
        (143, 39, '2037-09-01', '2041-05-31', 50, '2037 cohort for Program 39'),
        (144, 40, '2037-09-01', '2041-05-31', 120, '2037 cohort for Program 40'),
        (145, 41, '2037-09-01', '2038-05-31',
         75, 'Fall 2037 cohort for Program 41'),
        (146, 42, '2037-01-01', '2037-12-31', 60, '2037 cohort for Program 42'),
        (147, 43, '2037-09-01', '2038-05-31',
         85, 'Fall 2037 cohort for Program 43'),
        (148, 44, '2037-01-01', '2037-12-31', 90, '2037 cohort for Program 44'),
        (149, 45, '2037-09-01', '2041-05-31', 40, '2037 cohort for Program 45'),
        (150, 46, '2037-09-01', '2041-05-31', 110, '2037 cohort for Program 46'),
        (151, 47, '2038-01-01', '2038-12-31', 100, '2038 cohort for Program 47'),
        (152, 48, '2038-09-01', '2039-05-31',
         80, 'Fall 2038 cohort for Program 48'),
        (153, 49, '2038-09-01', '2042-05-31', 50, '2038 cohort for Program 49'),
        (154, 50, '2038-09-01', '2042-05-31', 120, '2038 cohort for Program 50'),
        (155, 51, '2038-09-01', '2039-05-31',
         75, 'Fall 2038 cohort for Program 51'),
        (156, 52, '2038-01-01', '2038-12-31', 60, '2038 cohort for Program 52'),
        (157, 53, '2038-09-01', '2039-05-31',
         85, 'Fall 2038 cohort for Program 53'),
        (158, 54, '2038-01-01', '2038-12-31', 90, '2038 cohort for Program 54'),
        (159, 55, '2038-09-01', '2042-05-31', 40, '2038 cohort for Program 55'),
        (160, 56, '2038-09-01', '2042-05-31', 110, '2038 cohort for Program 56'),
        (161, 57, '2039-01-01', '2039-12-31', 100, '2039 cohort for Program 57'),
        (162, 58, '2039-09-01', '2040-05-31',
         80, 'Fall 2039 cohort for Program 58'),
        (163, 59, '2039-09-01', '2043-05-31', 50, '2039 cohort for Program 59'),
        (164, 60, '2039-09-01', '2043-05-31', 120, '2039 cohort for Program 60'),
        (165, 61, '2039-09-01', '2040-05-31',
         75, 'Fall 2039 cohort for Program 61'),
        (166, 62, '2039-01-01', '2039-12-31', 60, '2039 cohort for Program 62'),
        (167, 63, '2039-09-01', '2040-05-31',
         85, 'Fall 2039 cohort for Program 63'),
        (168, 64, '2039-01-01', '2039-12-31', 90, '2039 cohort for Program 64'),
        (169, 65, '2039-09-01', '2043-05-31', 40, '2039 cohort for Program 65'),
        (170, 66, '2039-09-01', '2043-05-31', 110, '2039 cohort for Program 66'),
        (171, 67, '2040-01-01', '2040-12-31', 100, '2040 cohort for Program 67'),
        (172, 68, '2040-09-01', '2041-05-31',
         80, 'Fall 2040 cohort for Program 68'),
        (173, 69, '2040-09-01', '2044-05-31', 50, '2040 cohort for Program 69'),
        (174, 70, '2040-09-01', '2044-05-31', 120, '2040 cohort for Program 70'),
        (175, 71, '2040-09-01', '2041-05-31',
         75, 'Fall 2040 cohort for Program 71'),
        (176, 72, '2040-01-01', '2040-12-31', 60, '2040 cohort for Program 72'),
        (177, 73, '2040-09-01', '2041-05-31',
         85, 'Fall 2040 cohort for Program 73'),
        (178, 74, '2040-01-01', '2040-12-31', 90, '2040 cohort for Program 74'),
        (179, 75, '2040-09-01', '2044-05-31', 40, '2040 cohort for Program 75'),
        (180, 76, '2040-09-01', '2044-05-31', 110, '2040 cohort for Program 76'),
        (181, 77, '2041-01-01', '2041-12-31', 100, '2041 cohort for Program 77'),
        (182, 78, '2041-09-01', '2042-05-31',
         80, 'Fall 2041 cohort for Program 78'),
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Program_Term (program_term_id, program_id, start_date, end_date, max_capacity, description) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, program_terms)
    connection.commit()
    print(
        f"Inserted {len(program_terms)} records into the Program_Term table.")

def generate_and_insert_modules():

    modules_list = [
        (1, 1, 'Introduction to Financial Management',
         'Financial Management', 3, 'Fall'),
        (2, 2, 'Principles of Accounting', 'Accounting Principles', 4, 'Fall'),
        (3, 4, 'Business Ethics in the Modern World', 'Business Ethics', 3, 'Spring'),
        (4, 8, 'Marketing Strategies for Success',
         'Marketing Strategies', 3, 'Spring'),
        (5, 6, 'Entrepreneurship Fundamentals', 'Entrepreneurship', 4, 'Summer'),
        (6, 7, 'Front-end Web Development', 'Front-end Development', 3, 'Fall'),
        (7, 7, 'Back-end Web Development', 'Back-end Development', 3, 'Fall'),
        (8, 23, 'Database Management Essentials',
         'Database Management', 4, 'Spring'),
        (9, 23, 'Mobile App Development Workshop',
         'Mobile App Development', 4, 'Spring'),
        (10, 17, 'Cybersecurity Fundamentals', 'Cybersecurity', 3, 'Summer'),
        (11, 5, 'Introduction to Criminal Law', 'Criminal Law', 3, 'Fall'),
        (12, 11, 'Contract Law Basics', 'Contract Law', 3, 'Fall'),
        (13, 21, 'Constitutional Law in Practice',
         'Constitutional Law', 4, 'Spring'),
        (14, 16, 'International Law Perspectives',
         'International Law', 4, 'Spring'),
        (15, 16, 'Legal Research and Writing Workshop',
         'Legal Research and Writing', 3, 'Summer'),
        (16, 4, 'Exploring Fine Arts', 'Fine Arts', 3, 'Fall'),
        (17, 36, 'Introduction to Performing Arts', 'Performing Arts', 3, 'Fall'),
        (18, 36, 'Visual Arts Appreciation', 'Visual Arts', 4, 'Spring'),
        (19, 15, 'Art History: From Renaissance to Modernism',
         'Art History', 4, 'Spring'),
        (20, 36, 'Creative Writing Workshop', 'Creative Writing', 3, 'Summer'),
        (21, 56, 'Architectural Design Principles',
         'Architectural Design', 3, 'Fall'),
        (22, 55, 'Structural Engineering Fundamentals',
         'Structural Engineering', 3, 'Fall'),
        (23, 70, 'Urban Planning Strategies', 'Urban Planning', 4, 'Spring'),
        (24, 70, 'Sustainable Architecture Workshop',
         'Sustainable Architecture', 4, 'Spring'),
        (25, 56, 'History of Architecture', 'History of Architecture', 3, 'Summer'),
        (26, 29, 'Advanced Financial Management',
         'Financial Management', 4, 'Fall'),
        (27, 29, 'Managerial Accounting Practices',
         'Accounting Principles', 4, 'Fall'),
        (28, 29, 'Corporate Social Responsibility in Business',
         'Business Ethics', 3, 'Spring'),
        (29, 8, 'Digital Marketing Strategies',
         'Marketing Strategies', 4, 'Spring'),
        (30, 29, 'Innovation and Technology Entrepreneurship',
         'Entrepreneurship', 4, 'Summer'),
        (31, 23, 'Advanced Front-end Development',
         'Front-end Development', 4, 'Fall'),
        (32, 23, 'Back-end System Architecture', 'Back-end Development', 4, 'Fall'),
        (33, 18, 'Database Design and Optimization',
         'Database Management', 4, 'Spring'),
        (34, 23, 'Mobile App Security and Privacy',
         'Mobile App Development', 3, 'Spring'),
        (35, 23, 'Advanced Cybersecurity Concepts', 'Cybersecurity', 4, 'Summer'),
        (36, 11, 'Criminal Procedure and Evidence', 'Criminal Law', 4, 'Fall'),
        (37, 11, 'Business Contracts and Negotiation', 'Contract Law', 3, 'Fall'),
        (38, 11, 'Constitutional Law Challenges',
         'Constitutional Law', 4, 'Spring'),
        (39, 11, 'International Business Law', 'International Law', 4, 'Spring'),
        (40, 11, 'Legal Writing and Advocacy',
         'Legal Research and Writing', 3, 'Summer'),
        (41, 15, 'Modern Art Movements', 'Fine Arts', 3, 'Fall'),
        (42, 15, 'Theater Production Techniques', 'Performing Arts', 4, 'Fall'),
        (43, 15, 'Contemporary Visual Arts', 'Visual Arts', 3, 'Spring'),
        (44, 15, 'Art Criticism and Analysis', 'Art History', 4, 'Spring'),
        (45, 15, 'Advanced Creative Writing Workshop',
         'Creative Writing', 4, 'Summer'),
        (46, 70, 'Advanced Architectural Design Studio',
         'Architectural Design', 4, 'Fall'),
        (47, 55, 'Structural Analysis and Design',
         'Structural Engineering', 4, 'Fall'),
        (48, 70, 'Urban Development and Renewal', 'Urban Planning', 3, 'Spring'),
        (49, 70, 'Sustainable Building Practices',
         'Sustainable Architecture', 4, 'Spring'),
        (50, 70, 'Contemporary Trends in Architecture',
         'History of Architecture', 3, 'Summer'),
        (51, 4, 'Global Political Systems', 'Political Science', 4, 'Fall'),
        (52, 4, 'International Relations Theory',
         'International Relations', 4, 'Spring'),
        (53, 10, 'Literary Analysis and Criticism', 'English Literature', 3, 'Fall'),
        (54, 10, 'Contemporary World Literature',
         'English Literature', 3, 'Spring'),
        (55, 20, 'Sociological Theories', 'Sociology', 3, 'Fall'),
        (56, 20, 'Social Research Methods', 'Sociology', 4, 'Spring'),
        (57, 26, 'Psychological Perspectives', 'Psychology', 3, 'Fall'),
        (58, 26, 'Cognitive Psychology', 'Psychology', 4, 'Spring'),
        (59, 36, 'Creative Writing Techniques', 'Creative Writing', 4, 'Fall'),
        (60, 36, 'Screenwriting Fundamentals', 'Creative Writing', 4, 'Spring'),
        (61, 41, 'Political Theory', 'Political Science', 4, 'Fall'),
        (62, 41, 'Public Policy Analysis', 'Political Science', 4, 'Spring'),
        (63, 46, 'Economic Theory', 'Economics', 4, 'Fall'),
        (64, 46, 'Global Economy and Markets', 'Economics', 4, 'Spring'),
        (65, 31, 'Philosophy of Science', 'Philosophy', 3, 'Fall'),
        (66, 31, 'Ethics and Morality', 'Philosophy', 3, 'Spring'),
        (67, 3, 'Sustainable Engineering Practices',
         'Environmental Engineering', 4, 'Fall'),
        (68, 3, 'Water Resources Engineering',
         'Environmental Engineering', 4, 'Spring'),
        (69, 9, 'Structural Dynamics in Civil Engineering',
         'Civil Engineering', 4, 'Fall'),
        (70, 9, 'Geotechnical Engineering Principles',
         'Civil Engineering', 4, 'Spring'),
        (71, 14, 'Renewable Energy Technologies',
         'Renewable Energy Engineering', 4, 'Fall'),
        (72, 14, 'Energy Systems and Sustainability',
         'Renewable Energy Engineering', 4, 'Spring'),
        (73, 19, 'Aerospace Propulsion Systems',
         'Aerospace Engineering', 4, 'Fall'),
        (74, 19, 'Flight Mechanics and Control',
         'Aerospace Engineering', 4, 'Spring'),
        (75, 25, 'Thermodynamics in Mechanical Engineering',
         'Mechanical Engineering', 4, 'Fall'),
        (76, 25, 'Fluid Mechanics and Dynamics',
         'Mechanical Engineering', 4, 'Spring'),
        (77, 30, 'Electrical Circuits and Systems',
         'Electrical Engineering', 4, 'Fall'),
        (78, 30, 'Digital Signal Processing',
         'Electrical Engineering', 4, 'Spring'),
        (79, 35, 'Computer Systems Architecture',
         'Computer Engineering', 4, 'Fall'),
        (80, 35, 'Embedded Systems Design', 'Computer Engineering', 4, 'Spring'),
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Modules(module_id, program_term_id, module_name, module_subject, module_points, semester) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, modules_list)
    connection.commit()
    print(f"Inserted {len(modules_list)} records into the Modules table.")

bachelor_program_term_ids = [
    4, 10, 14, 20, 24, 30, 34, 40, 44, 50,
    54, 60, 64, 70, 74, 80, 84, 90, 94, 100,
    104, 110, 114, 119, 124, 130, 135, 140, 145, 150,
    155, 156, 157, 158, 159, 160, 161, 162, 163, 164,
    165, 166, 167, 168, 169, 170, 171, 172, 173, 174,
    175, 176, 177, 178, 179, 180, 181, 182
]

master_program_term_ids = []

# ENROLLS STUDENTS ONLY FOR BACHELOR DEGREES AND NONE RELATED TO UNIPI

def generate_and_insert_enrollments(num):
    enrollments = []

    # Generate fake data
    for i in range(1, num + 1):
        student_id = fake.unique.random_int(min=1, max=100)
        bachelor_program_id = random.choice(bachelor_program_term_ids)
        registration_date = fake.date_between(
            start_date="-2y", end_date="today")

        # Add enrollment for bachelor program
        enrollment = (
            i,                        # enrollment_id
            student_id,               # student_id
            bachelor_program_id,      # program_term_id
            registration_date,        # registration_date
        )
        enrollments.append(enrollment)

        # Optionally enroll in master programs
        # for _ in range(random.randint(1, 3)):  # Assuming 1 to 3 master programs
        #     master_program_id = random.choice(master_program_term_ids)
        #     enrollment = (
        #         i,                    # enrollment_id
        #         student_id,           # student_id
        #         master_program_id,    # program_term_id
        #         registration_date,    # registration_date
        #     )
        #     enrollments.append(enrollment)

    # Create a cursor object
    cursor = connection.cursor()

    # SQL query for inserting data
    insert_query = "INSERT INTO Enrollment (enrollment_id, student_id, program_term_id, registration_date) VALUES (%s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, enrollments)
        connection.commit()
        print(
            f"Inserted {len(enrollments)} records into the Enrollment table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def generate_and_insert_companies(num_companies):
    cursor = connection.cursor()

    companies = []

    for i in range(1, num_companies + 1):
        company = (
            i,                           # company_id
            fake.company(),               # company_name
            # location_id (Assuming you have 100 locations)
            random.randint(1, 100),
            random.randint(10, 1000),    # employees (You can adjust the range)
            random.choice(['Telecommunications', 'Hospitality', 'Shipping',
                          'Engineering', 'Software', 'Auditing', 'Banking', 'Other']),  # industry
        )
        companies.append(company)

    # Assuming your table has columns (company_id, company_name, location_id, employees, industry)
    insert_query = "INSERT INTO Company (company_id, company_name, location_id, employees, industry) VALUES (%s, %s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, companies)
        connection.commit()
        print(f"Inserted {len(companies)} records into the Company table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def generate_and_insert_job_titles(num_job_titles):
    cursor = connection.cursor()

    job_titles = []

    for i in range(1, num_job_titles + 1):
        job_title = (
            i,  # title_id
            fake.job(),  # title_name
            random.choice(['SoftwareEngineering', 'accounting', 'Shipping',
                          'DataScience', 'Business', 'Sales', 'Consulting']),  # job_type
            fake.text(max_nb_chars=255),  # description
        )
        job_titles.append(job_title)

    # Assuming your table has columns (title_id, title_name, job_type, description)
    insert_query = "INSERT INTO JobTitle (title_id, title_name, job_type, description) VALUES (%s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, job_titles)
        connection.commit()
        print(f"Inserted {len(job_titles)} records into the JobTitle table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()



        
##### ALL THESE WORK ######
# generate_and_insert_locations(100)
# generate_and_insert_students(100)
# location_ids = generate_and_insert_locations(100)
# generate_and_insert_universities(10, location_ids)
# generate_and_insert_educationLevel()
# generate_and_insert_degree()
# generate_and_insert_faculties()
# generate_and_insert_Program()
# generate_and_insert_Programterm()
# generate_and_insert_modules()
# generate_and_insert_enrollments(100)
# generate_and_insert_companies(10)
# generate_and_insert_job_titles(10)


##### NOT TESTED YET ######
# def generate_and_insert_student_module_results()
# def generate_and_insert_student_graduation()
# def generate_and_insert_work_experience(num_records):
#     work_experiences = []

#     # Generate fake data
#     for i in range(1, num_records + 1):
#         student_id = random.choice(student_ids)
#         company_id = random.choice(company_ids)
#         job_title_id = random.choice(job_title_ids)
#         job_category = random.choice(job_categories)
#         start_date = fake.date_between(start_date="-5y", end_date="-1y")
#         end_date = start_date + \
#             timedelta(days=random.randint(150, 365))  # Random duration
#         description = fake.sentence(nb_words=6)
#         responsibilities = fake.sentence(nb_words=6)

#         work_experience = (
#             i,                          # experience_id
#             student_id,                 # student_id
#             company_id,                 # company_id
#             job_title_id,               # job_title_id
#             job_category,               # job_category
#             start_date,                 # start_date
#             end_date,                   # end_date
#             description,                # description
#             responsibilities,           # responsibilities
#         )
#         work_experiences.append(work_experience)

#     # Create a cursor object
#     cursor = connection.cursor()

#     # SQL query for inserting data
#     insert_query = """
#     INSERT INTO WorkExperience 
#     (experience_id, student_id, company_id, job_title_id, job_category, start_date, end_date, description, responsibilities) 
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """

#     try:
#         cursor.executemany(insert_query, work_experiences)
#         connection.commit()
#         print(
#             f"Inserted {len(work_experiences)} records into the WorkExperience table.")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         cursor.close()
        


# Close the connection
connection.close()
