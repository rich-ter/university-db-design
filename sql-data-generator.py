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


# generate 100 locations


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


def generate_and_insert_Program():

    programs_list = [
        (1, 2, 1, 'Masters in Advanced Information Systems',
         2022, 'Remote', '4', 'Full Time', 'Technology'),
        (2, 2, 1, 'Masters in Business Analytics', 2023,
         'Hybrid', '5', 'Part Time', 'Business & Finance'),
        (3, 3, 2, 'Ph.D. in Environmental Engineering Research',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (4, 1, 3, 'Bachelor of Arts in Political Science and International Relations',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (5, 2, 4, 'Master of Law in Intellectual Property',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (6, 4, 5, 'Associate Degree in Business and Finance',
         2022, 'Hybrid', '2', 'Full Time', 'Business & Finance'),
        (7, 2, 1, 'Masters in Technology Management',
         2023, 'Remote', '5', 'Part Time', 'Technology'),
        (8, 2, 2, 'Masters in Marketing Analytics', 2022,
         'Physical', '4', 'Full Time', 'Business & Finance'),
        (9, 3, 3, 'Ph.D. in Civil Engineering Structures',
         2021, 'Hybrid', '7', 'Part Time', 'Technology'),
        (10, 1, 4, 'Bachelor of Arts in English Literature',
         2022, 'Physical', '6', 'Full Time', 'Arts'),
        (11, 2, 5, 'Master of Science in Criminal Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (12, 4, 1, 'Associate Degree in IT Management',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (13, 2, 2, 'Masters in Financial Management', 2023,
         'Physical', '5', 'Full Time', 'Business & Finance'),
        (14, 3, 3, 'Ph.D. in Renewable Energy Engineering',
         2021, 'Hybrid', '8', 'Part Time', 'Technology'),
        (15, 1, 4, 'Bachelor of Arts in History',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (16, 2, 5, 'Master of Law in International Human Rights',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (17, 4, 1, 'Associate Degree in Computer Science',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (18, 2, 1, 'Masters in Data Science', 2023,
         'Remote', '4', 'Part Time', 'Technology'),
        (19, 3, 2, 'Ph.D. in Aerospace Engineering', 2021,
         'Physical', '7', 'Full Time', 'Technology'),
        (20, 1, 3, 'Bachelor of Arts in Sociology',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (21, 2, 4, 'Master of Law in Environmental Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (22, 4, 5, 'Associate Degree in Business Administration',
         2022, 'Physical', '2', 'Full Time', 'Business & Finance'),
        (23, 2, 1, 'Masters in Information Technology',
         2023, 'Hybrid', '5', 'Full Time', 'Technology'),
        (24, 2, 2, 'Masters in Human Resource Management', 2022,
         'Remote', '4', 'Part Time', 'Business & Finance'),
        (25, 3, 3, 'Ph.D. in Mechanical Engineering',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (26, 1, 4, 'Bachelor of Arts in Psychology',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (27, 2, 5, 'Master of Law in Corporate Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (28, 4, 1, 'Associate Degree in Software Development',
         2022, 'Physical', '2', 'Full Time', 'Technology'),
        (29, 2, 1, 'Masters in Business Administration', 2023,
         'Hybrid', '5', 'Part Time', 'Business & Finance'),
        (30, 3, 2, 'Ph.D. in Electrical Engineering',
         2021, 'Physical', '7', 'Full Time', 'Technology'),
        (31, 1, 3, 'Bachelor of Arts in Philosophy',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (32, 2, 4, 'Master of Law in Intellectual Property Law',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (33, 4, 5, 'Associate Degree in Network Security',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (34, 2, 1, 'Masters in Marketing Management', 2023,
         'Remote', '4', 'Part Time', 'Business & Finance'),
        (35, 3, 3, 'Ph.D. in Computer Engineering',
         2021, 'Hybrid', '8', 'Full Time', 'Technology'),
        (36, 1, 4, 'Bachelor of Arts in Creative Writing',
         2022, 'Physical', '6', 'Full Time', 'Arts'),
        (37, 2, 5, 'Master of Law in Criminal Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (38, 4, 1, 'Associate Degree in Mobile App Development',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (39, 2, 2, 'Masters in Financial Analysis', 2023,
         'Physical', '5', 'Full Time', 'Business & Finance'),
        (40, 3, 3, 'Ph.D. in Software Engineering',
         2021, 'Hybrid', '7', 'Part Time', 'Technology'),
        (41, 1, 4, 'Bachelor of Arts in Political Science',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (42, 2, 5, 'Master of Law in International Business Law',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (43, 4, 1, 'Associate Degree in Information Technology Management',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (44, 2, 1, 'Masters in Business and IT', 2023,
         'Remote', '5', 'Part Time', 'Business & Finance'),
        (45, 3, 2, 'Ph.D. in Artificial Intelligence',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (46, 1, 3, 'Bachelor of Arts in Economics',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (47, 2, 4, 'Master of Law in Environmental Law and Policy',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (48, 4, 5, 'Associate Degree in Business and Finance Administration',
         2022, 'Physical', '2', 'Full Time', 'Business & Finance'),
        (49, 2, 1, 'Masters in Information Systems Management',
         2023, 'Hybrid', '4', 'Part Time', 'Technology'),
        (50, 2, 2, 'Masters in Human Resource Development', 2022,
         'Physical', '5', 'Full Time', 'Business & Finance')
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Program (program_id, awarded_degree, faculty_id, program_name, year_started, teaching_type, semesters, pace, subject_type) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)"
    cursor.executemany(insert_query, programs_list)
    connection.commit()
    print(
        f"Inserted {len(programs_list)} records into the EducationLevel table.")


# def generate_and_insert_Programterm():

    # program_terms = [
    #     (1, 1, '2022-09-01', '2023-05-31', 4, 0),
    #     (2, 1, '2023-09-01', '2024-05-31', 4, 0),
    #     (3, 1, '2024-09-01', '2025-05-31', 4, 0)
    #     (4, 2, '2023-09-01', '2024-05-31', 5, 0),
    #     (5, 2, '2024-09-01', '2025-05-31', 5, 0),
    #     (6, 2, '2025-09-01', '2026-05-31', 5, 0)
    #     (7, 3, '2021-09-01', '2025-08-31', 8, 0),
    #     (8, 3, '2025-09-01', '2029-08-31', 8, 0),
    #     (9, 3, '2029-09-01', '2033-08-31', 8, 0)
    #     (10, 4, '2022-09-01', '2025-05-31', 6, 0),
    #     (11, 4, '2025-09-01', '2028-05-31', 6, 0),
    #     (12, 4, '2028-09-01', '2031-05-31', 6, 0)
    #     (13, 5, '2023-09-01', '2024-05-31', 4, 0),
    #     (14, 5, '2024-09-01', '2025-05-31', 4, 0),
    #     (15, 5, '2025-09-01', '2026-05-31', 4, 0)
    #     (16, 6, '2022-09-01', '2024-05-31', 2, 0),
    #     (17, 6, '2024-09-01', '2026-05-31', 2, 0),
    #     (18, 6, '2026-09-01', '2028-05-31', 2, 0)
    #     (19, 7, '2023-09-01', '2024-05-31', 5, 0),
    #     (20, 7, '2024-09-01', '2025-05-31', 5, 0),
    #     (21, 7, '2025-09-01', '2026-05-31', 5, 0)
    #     (22, 8, '2022-09-01', '2023-05-31', 4, 0),
    #     (23, 8, '2023-09-01', '2024-05-31', 4, 0),
    #     (24, 8, '2024-09-01', '2025-05-31', 4, 0)
    #     (25, 9, '2021-09-01', '2028-08-31', 7, 0),
    #     (26, 9, '2028-09-01', '2035-08-31', 7, 0),
    #     (27, 9, '2035-09-01', '2042-08-31', 7, 0)
    #     (28, 10, '2022-09-01', '2025-05-31', 6, 0),
    #     (29, 10, '2025-09-01', '2028-05-31', 6, 0),
    #     (30, 10, '2028-09-01', '2031-05-31', 6, 0)
    #     (31, 11, '2023-09-01', '2024-05-31', 4, 0),
    #     (32, 11, '2024-09-01', '2025-05-31', 4, 0),
    #     (33, 11, '2025-09-01', '2026-05-31', 4, 0)
    #     (34, 12, '2022-09-01', '2024-05-31', 2, 0),
    #     (35, 12, '2024-09-01', '2026-05-31', 2, 0),
    #     (36, 12, '2026-09-01', '2028-05-31', 2, 0)
    #     (37, 13, '2023-09-01', '2024-05-31', 5, 0),
    #     (38, 13, '2024-09-01', '2025-05-31', 5, 0),
    #     (39, 13, '2025-09-01', '2026-05-31', 5, 0),
    #     (40, 14, '2021-09-01', '2028-08-31', 8, 0),
    #     (41, 14, '2028-09-01', '2035-08-31', 8, 0),
    #     (42, 14, '2035-09-01', '2042-08-31', 8, 0)
    #     (43, 15, '2022-09-01', '2025-05-31', 6, 0),
    #     (44, 15, '2025-09-01', '2028-05-31', 6, 0),
    #     (45, 15, '2028-09-01', '2031-05-31', 6, 0)
    #     (46, 16, '2023-09-01', '2024-05-31', 4, 0),
    #     (47, 16, '2024-09-01', '2025-05-31', 4, 0),
    #     (48, 16, '2025-09-01', '2026-05-31', 4, 0)
    #     (49, 17, '2022-09-01', '2024-05-31', 2, 0),
    #     (50, 17, '2024-09-01', '2026-05-31', 2, 0),
    #     (51, 17, '2026-09-01', '2028-05-31', 2, 0)
    #     (52, 18, '2023-09-01', '2024-05-31', 4, 0),
    #     (53, 18, '2024-09-01', '2025-05-31', 4, 0),
    #     (54, 18, '2025-09-01', '2026-05-31', 4, 0)
    #     (55, 19, '2021-09-01', '2028-08-31', 7, 0),
    #     (56, 19, '2028-09-01', '2035-08-31', 7, 0),
    #     (57, 19, '2035-09-01', '2042-08-31', 7, 0)
    #     (58, 20, '2022-09-01', '2025-05-31', 6, 0),
    #     (59, 20, '2025-09-01', '2028-05-31', 6, 0),
    #     (60, 20, '2028-09-01', '2031-05-31', 6, 0)
    #     (61, 21, '2023-09-01', '2025-05-31', 4, 0),
    #     (62, 21, '2025-09-01', '2027-05-31', 4, 0)
    #     (63, 22, '2022-09-01', '2024-05-31', 2, 0),
    #     (64, 22, '2024-09-01', '2026-05-31', 2, 0)
    #     (65, 23, '2023-09-01', '2025-05-31', 5, 0),
    #     (66, 23, '2025-09-01', '2027-05-31', 5, 0)
    #     (67, 24, '2022-09-01', '2024-05-31', 4, 0),
    #     (68, 24, '2024-09-01', '2026-05-31', 4, 0)
    #     (69, 25, '2021-09-01', '2024-05-31', 8, 0),
    #     (70, 25, '2024-09-01', '2027-05-31', 8, 0)
    #     (71, 26, '2022-09-01', '2025-05-31', 6, 0),
    #     (72, 26, '2025-09-01', '2028-05-31', 6, 0)
    #     (73, 27, '2023-09-01', '2025-05-31', 4, 0),
    #     (74, 27, '2025-09-01', '2027-05-31', 4, 0)
    #     (75, 28, '2022-09-01', '2024-05-31', 2, 0),
    #     (76, 28, '2024-09-01', '2026-05-31', 2, 0)
    #     (77, 29, '2023-09-01', '2025-05-31', 5, 0),
    #     (78, 29, '2025-09-01', '2027-05-31', 5, 0)
    #     (79, 30, '2021-09-01', '2024-05-31', 7, 0),
    #     (80, 30, '2024-09-01', '2027-05-31', 7, 0)
    #     (81, 31, '2022-09-01', '2025-05-31', 6, 0),
    #     (82, 31, '2025-09-01', '2028-05-31', 6, 0)
    #     (83, 32, '2023-09-01', '2025-05-31', 4, 0),
    #     (84, 32, '2025-09-01', '2027-05-31', 4, 0)
    #     (85, 33, '2022-09-01', '2024-05-31', 2, 0),
    #     (86, 33, '2024-09-01', '2026-05-31', 2, 0)
    #     (87, 34, '2023-09-01', '2025-05-31', 4, 0),
    #     (88, 34, '2025-09-01', '2027-05-31', 4, 0)
    #     (89, 35, '2021-09-01', '2024-05-31', 8, 0),
    #     (90, 35, '2024-09-01', '2027-05-31', 8, 0)
    #     (91, 36, '2022-09-01', '2025-05-31', 6, 0),
    #     (92, 36, '2025-09-01', '2028-05-31', 6, 0)
    #     (93, 37, '2023-09-01', '2025-05-31', 4, 0),
    #     (94, 37, '2025-09-01', '2027-05-31', 4, 0)
    #     (95, 38, '2022-09-01', '2024-05-31', 2, 0),
    #     (96, 38, '2024-09-01', '2026-05-31', 2, 0)
    #     (97, 39, '2023-09-01', '2025-05-31', 5, 0),
    #     (98, 39, '2025-09-01', '2027-05-31', 5, 0)
    #     (99, 40, '2021-09-01', '2024-05-31', 7, 0),
    #     (100, 40, '2024-09-01', '2027-05-31', 7, 0)
    #     (101, 41, '2022-09-01', '2025-05-31', 6, 0),
    #     (102, 41, '2025-09-01', '2028-05-31', 6, 0)
    #     (103, 42, '2023-09-01', '2025-05-31', 4, 0),
    #     (104, 42, '2025-09-01', '2027-05-31', 4, 0)
    #     (105, 43, '2022-09-01', '2024-05-31', 2, 0),
    #     (106, 43, '2024-09-01', '2026-05-31', 2, 0)
    #     (107, 44, '2023-09-01', '2025-05-31', 5, 0),
    #     (108, 44, '2025-09-01', '2027-05-31', 5, 0)
    #     (109, 45, '2021-09-01', '2024-05-31', 8, 0),
    #     (110, 45, '2024-09-01', '2027-05-31', 8, 0)
    #     (111, 46, '2022-09-01', '2025-05-31', 6, 0),
    #     (112, 46, '2025-09-01', '2028-05-31', 6, 0)
    #     (113, 47, '2023-09-01', '2025-05-31', 4, 0),
    #     (114, 47, '2025-09-01', '2027-05-31', 4, 0)
    #     (115, 48, '2022-09-01', '2024-05-31', 2, 0),
    #     (116, 48, '2024-09-01', '2026-05-31', 2, 0)
    #     (117, 49, '2023-09-01', '2025-05-31', 4, 0),
    #     (118, 50, '2022-09-01', '2024-05-31', 5, 0),
    #     (119, 50, '2024-09-01', '2026-05-31', 5, 0)
    #     (120, 45, '2021-09-01', '2024-05-31', 8, 0),
    #     (121, 45, '2024-09-01', '2027-05-31', 8, 0)
    #     (122, 46, '2022-09-01', '2025-05-31', 6, 0),
    #     (123, 46, '2025-09-01', '2028-05-31', 6, 0)
    #     (124, 47, '2023-09-01', '2025-05-31', 4, 0),
    #     (125, 47, '2025-09-01', '2027-05-31', 4, 0)
    #     (126, 48, '2022-09-01', '2024-05-31', 2, 0),
    #     (127, 48, '2024-09-01', '2026-05-31', 2, 0)
    #     (128, 49, '2023-09-01', '2025-05-31', 4, 0),
    #     (129, 49, '2025-09-01', '2027-05-31', 4, 0)
    #     (130, 50, '2022-09-01', '2024-05-31', 5, 0),
    #     (131, 50, '2024-09-01', '2026-05-31', 5, 0),
    # ]

    # Program_Term(
    #     program_term_id INT PRIMARY KEY,
    #     program_id INT NOT NULL,
    #     start_date DATE NOT NULL,
    #     end_date DATE NOT NULL,
    #     max_capacity INT NOT NULL,
    #     registered_students INT,
    #     FOREIGN KEY(program_id) REFERENCES Program(program_id)
    # )

# create_database_and_tables()

##### ALL THESE WORK ######
# generate_and_insert_locations(100)
# generate_and_insert_students(100)
# location_ids = generate_and_insert_locations(100)
# generate_and_insert_universities(10, location_ids)
# generate_and_insert_educationLevel()
# generate_and_insert_degree()
# generate_and_insert_faculties()
# generate_and_insert_Program()

##### NOT TESTED YET ######
# def generate_and_insert_modules()

# def generate_and_insert_student_module_results()

# def generate_and_insert_student_enrollment()

# def generate_and_insert_student_graduation()

# def generate_and_insert_student_company()

# def generate_and_insert_student_jobtitle()

# def generate_and_insert_student_workexperience()


# Close the connection
connection.close()
