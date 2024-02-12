# pip install mysql-connector-python & faker
from mysql.connector import connect, Error
import mysql.connector
from faker import Faker
import random
from datetime import timedelta, datetime

fake = Faker('el_GR')  # Set the locale to Greek (Greece)

# Working perfect 
def create_database_and_tables(connection):
    create_db_tables = [
    """
	CREATE TABLE IF NOT EXISTS Location (
        location_id INT PRIMARY KEY,
        address VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        postcode INT NOT NULL
    );
    """,
    """      
	CREATE TABLE IF NOT EXISTS University (
        university_id INT PRIMARY KEY,
        university_name VARCHAR(255) NOT NULL,
        founded_year YEAR NOT NULL,
        website VARCHAR(255),
        location_id INT NOT NULL,
        FOREIGN KEY (location_id) REFERENCES Location(location_id)
    );
    """,
    """
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
    """,
    """
    CREATE TABLE IF NOT EXISTS EducationLevel (
        level_id INT PRIMARY KEY,
        level_name ENUM('Bachelors', 'Masters', 'Phd', 'Associates', 'Post Graduate Diploma', 'Under Graduate Diploma'),
        level ENUM('Level 6', 'Level 7', 'Level 8'),
        description VARCHAR(255),
        ects_requirements INT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Degree (
        degree_id INT PRIMARY KEY,
        education_level_id INT NOT NULL,
        degree_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (education_level_id) REFERENCES EducationLevel(level_id)
    );
    """,
    """
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
    """,
    """
    CREATE TABLE IF NOT EXISTS Program_Term (
        program_term_id INT PRIMARY KEY,
        program_id INT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        max_capacity INT NOT NULL,
        description VARCHAR(255), 
        FOREIGN KEY (program_id) REFERENCES Program(program_id)
    );
    """,
    """
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
    """,
    """
	CREATE TABLE IF NOT EXISTS Student (
        student_id INT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        father_name VARCHAR(255),
        email VARCHAR(255) NOT NULL,
        date_of_birth DATE NOT NULL
    );
    """,
    """ 
   CREATE TABLE IF NOT EXISTS StudentModuleParticipation (
        stud_mod_id INT PRIMARY KEY,
        module_id INT NOT NULL,
        student_id INT NOT NULL,
        FOREIGN KEY (module_id) REFERENCES Modules(module_id),
        FOREIGN KEY (student_id) REFERENCES Student(student_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Enrollment (
        enrollment_id INT PRIMARY KEY,
        student_id INT NOT NULL,
        program_term_id INT NOT NULL,
        registration_date DATE NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (program_term_id) REFERENCES Program_Term(program_term_id)
    );
    """,
    """

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
    """,
    """
    
    CREATE TABLE IF NOT EXISTS Company (
        company_id INT PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL,
        location_id INT NOT NULL,
        employees INT NOT NULL,
        industry ENUM('Telecommunications', 'Hospitality', 'Shipping', 'Engineering', 'Software', 'Auditing', 'Banking', 'Other'),
        FOREIGN KEY (location_id) REFERENCES Location(location_id)
    );
    """,
    """

    CREATE TABLE IF NOT EXISTS JobTitle (
        title_id INT PRIMARY KEY,
        title_name VARCHAR(255) NOT NULL,
        job_type ENUM('Internship', 'Apprenticeship ', 'Permanent'),
        job_category ENUM('SoftwareEngineering', 'accounting', 'Shipping', 'DataScience', 'Business', 'Sales', 'Consulting'),
        description VARCHAR(255) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS WorkExperience (
        experience_id INT PRIMARY KEY,
        student_id INT NOT NULL,
        company_id INT NOT NULL,
        job_title_id INT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        description VARCHAR(255) NOT NULL,
        responsibilities VARCHAR(255) NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (company_id) REFERENCES Company(company_id),
        FOREIGN KEY (job_title_id) REFERENCES JobTitle(title_id)
    );
    """
    ]

    try:
        cursor = connection.cursor()
        for create_table_query in create_db_tables:
            cursor.execute(create_table_query)
        connection.commit()  # Commit after all tables are created
    except Error as e:
        print(e)
    finally:
        cursor.close()



def create_stored_procedures(connection):
    stored_procedures = [
        """
        CREATE PROCEDURE InsertStudent(
            IN first_name VARCHAR(255),
            IN last_name VARCHAR(255),
            IN father_name VARCHAR(255),
            IN email VARCHAR(255),
            IN date_of_birth DATE
        )
        BEGIN
            INSERT INTO Student (first_name, last_name, father_name, email, date_of_birth)
            VALUES (first_name, last_name, father_name, email, date_of_birth);
        END;
        """,
        """
        CREATE PROCEDURE FindStudentsWithoutWorkExperience(
            IN facultyName VARCHAR(255),
            IN universityName VARCHAR(255),
            IN monthsAgo INT
        )
        BEGIN
            SELECT DISTINCT s.student_id, s.first_name, s.last_name, s.email
            FROM Student s
            JOIN Enrollment e ON s.student_id = e.student_id
            JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
            JOIN Program p ON pt.program_id = p.program_id
            JOIN Faculty f ON p.faculty_id = f.faculty_id
            JOIN University u ON f.university_id = u.university_id
            LEFT JOIN WorkExperience w ON s.student_id = w.student_id AND w.start_date > DATE_SUB(CURDATE(), INTERVAL monthsAgo MONTH)
            WHERE w.student_id IS NULL
            AND f.faculty_name = facultyName
            AND u.university_name = universityName
            ORDER BY s.last_name, s.first_name;
        END;
        """
    ]

    cursor = connection.cursor()
    try:
        for procedure in stored_procedures:
            cursor.execute(procedure)
        print("Stored procedures created successfully.")
    except Error as e:
        print(f"Error creating stored procedures: {e}")
    finally:
        cursor.close()


def create_triggers(connection):
    pass


def create_indexes(connection):
    pass

def create_views_roles(connection):
    pass







# Working perfect 
def generate_and_insert_locations(connection, num):
    locations = []
    location_ids = []

    for i in range(1, num + 1):
        location = (
            i,                           
            fake.address(),              
            fake.city(),                 # city
            fake.random_int(min=10000, max=99999)  
        )
        locations.append(location)
        location_ids.append(i)

    cursor = connection.cursor()

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

# Working perfect 
def generate_and_insert_students(connection, num):
    students = []

    for i in range(1, num + 1):
        student = (
            i,                           
            fake.first_name(),           
            fake.last_name(),            
            fake.first_name(),           
            fake.email(),                
            fake.date_of_birth(),       
        )
        students.append(student)

    cursor = connection.cursor()

    insert_query = "INSERT INTO Student (student_id, first_name, last_name, father_name, email, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, students)
        connection.commit()
        print(f"Inserted {len(students)} records into the Student table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Working perfect 
def generate_and_insert_universities(connection):
    universities = []

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

    for i, university_name in enumerate(athens_universities, start=1):
        university = (
            i,                                    
            university_name,                      
            fake.random_int(min=1902, max=2024),   
            fake.url(),                            
            fake.random_int(min=1, max=100),   
        )
        universities.append(university)

    cursor = connection.cursor()

    insert_query = "INSERT INTO University (university_id, university_name, founded_year, website, location_id) VALUES (%s, %s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, universities)
        connection.commit()
        print(
            f"Inserted {len(universities)} records into the University table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Working perfect 
def generate_and_insert_faculties(connection):
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

# Working perfect 
def generate_and_insert_educationLevel(connection):
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

# Working perfect 
def generate_and_insert_degree(connection):

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

# Working perfect 
def generate_and_insert_Program(connection):

    programs_list = [
        (1, 8, 23, 'Masters in Advanced Information Systems',
         2022, 'Remote', '4', 'Full Time', 'Technology'),
        (2, 8, 20, 'Masters in Business Analytics', 2023,
         'Hybrid', '5', 'Part Time', 'Business & Finance'),
        (3, 17, 2, 'Ph.D. in Environmental Engineering Research',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (4, 1, 3, 'Bachelor of Arts in Political Science and International Relations',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (5, 9, 4, 'Master of Law in Intellectual Property',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (6, 20, 20, 'Associate Degree in Business and Finance',
         2022, 'Hybrid', '2', 'Full Time', 'Business & Finance'),
        (7, 8, 23, 'Masters in Technology Management',
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
        (13, 8, 19, 'Masters in Financial Management', 2023,
         'Physical', '5', 'Full Time', 'Business & Finance'),
        (14, 17, 3, 'Ph.D. in Renewable Energy Engineering',
         2021, 'Hybrid', '8', 'Part Time', 'Technology'),
        (15, 1, 47, 'Bachelor of Arts in History',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (16, 9, 5, 'Master of Law in International Human Rights',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (17, 20, 23, 'Associate Degree in Computer Science',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (18, 8, 1, 'Masters in Data Science', 2023,
         'Remote', '4', 'Part Time', 'Technology'),
        (19, 17, 2, 'Ph.D. in Aerospace Engineering',
         2021, 'Physical', '7', 'Full Time', 'Technology'),
        (20, 1, 3, 'Bachelor of Arts in Sociology',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (21, 9, 4, 'Master of Law in Environmental Law',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (22, 20, 19, 'Associate Degree in Business Administration',
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
        (33, 20, 23, 'Associate Degree in Network Security',
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
        (40, 17, 23, 'Ph.D. in Software Engineering',
         2021, 'Hybrid', '7', 'Part Time', 'Technology'),
        (41, 1, 4, 'Bachelor of Arts in Political Science',
         2022, 'Remote', '6', 'Full Time', 'Arts'),
        (42, 9, 5, 'Master of Law in International Business Law',
         2023, 'Physical', '4', 'Part Time', 'Law'),
        (43, 20, 23, 'Associate Degree in Information Technology Management',
         2022, 'Hybrid', '2', 'Full Time', 'Technology'),
        (44, 8, 1, 'Masters in Business and IT', 2023,
         'Remote', '5', 'Part Time', 'Business & Finance'),
        (45, 17, 23, 'Ph.D. in Artificial Intelligence',
         2021, 'Physical', '8', 'Full Time', 'Technology'),
        (46, 1, 3, 'Bachelor of Arts in Economics',
         2022, 'Hybrid', '6', 'Full Time', 'Arts'),
        (47, 9, 4, 'Master of Law in Environmental Law and Policy',
         2023, 'Remote', '4', 'Part Time', 'Law'),
        (48, 20, 5, 'Associate Degree in Business and Finance Administration',
         2022, 'Physical', '2', 'Full Time', 'Business & Finance'),
        (49, 8, 23, 'Masters in Information Systems Management',
         2023, 'Hybrid', '4', 'Part Time', 'Technology'),
        (50, 8, 20, 'Masters in Human Resource Development', 2022,
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

# Working perfect 
def generate_and_insert_Programterm(connection):
    bachelors_program_term_to_term = [
        (179, 75), (174, 70), (169, 65), (160, 56), (178, 74), 
        (173, 69), (168, 64), (164, 60), (159, 55), (182, 78), 
        (177, 73), (172, 68), (167, 63), (163, 59), (158, 54), 
        (180, 76), (175, 71), (170, 66), (165, 61), (161, 57), 
        (156, 52), (155, 51), (181, 77), (176, 72), (171, 67), 
        (166, 62), (162, 58), (157, 53), (150, 46), (145, 41), 
        (140, 36), (135, 31), (130, 26), (124, 20), (119, 15), 
        (10, 10), (20, 10), (30, 10), (40, 10), (50, 10), 
        (60, 10), (70, 10), (80, 10), (90, 10), (100, 10), 
        (110, 10), (4, 4), (14, 4), (24, 4), (34, 4), 
        (44, 4), (54, 4), (64, 4), (74, 4), (84, 4), 
        (94, 4), (104, 4), (114, 4)
    ]


    masters_program_term_to_term = [
        ('151', '47'), ('146', '42'), ('141', '37'), ('136', '32'), ('131', '27'), 
        ('125', '21'), ('120', '16'), ('115', '11'), ('5', '5'), ('15', '5'), 
        ('25', '5'), ('35', '5'), ('45', '5'), ('55', '5'), ('65', '5'), 
        ('75', '5'), ('85', '5'), ('95', '5'), ('105', '5'), ('154', '50'), 
        ('153', '49'), ('148', '44'), ('143', '39'), ('138', '34'), ('133', '29'), 
        ('128', '24'), ('127', '23'), ('122', '18'), ('117', '13'), ('8', '8'), 
        ('18', '8'), ('28', '8'), ('38', '8'), ('48', '8'), ('58', '8'), 
        ('68', '8'), ('78', '8'), ('88', '8'), ('98', '8'), ('108', '8'), 
        ('7', '7'), ('17', '7'), ('27', '7'), ('37', '7'), ('47', '7'), 
        ('57', '7'), ('67', '7'), ('77', '7'), ('87', '7'), ('97', '7'), 
        ('107', '7'), ('2', '2'), ('12', '2'), ('22', '2'), ('32', '2'), 
        ('42', '2'), ('52', '2'), ('62', '2'), ('72', '2'), ('82', '2'), 
        ('92', '2'), ('102', '2'), ('112', '2'), ('1', '1'), ('11', '1'), 
        ('21', '1'), ('31', '1'), ('41', '1'), ('51', '1'), ('61', '1'), 
        ('71', '1'), ('81', '1'), ('91', '1'), ('101', '1'), ('111', '1')
    ]

    phd_program_term_to_term = [
        ('149', '45'), ('144', '40'), ('139', '35'), ('134', '30'), ('129', '25'), 
        ('123', '19'), ('118', '14'), ('9', '9'), ('19', '9'), ('29', '9'), 
        ('39', '9'), ('49', '9'), ('59', '9'), ('69', '9'), ('79', '9'), 
        ('89', '9'), ('99', '9'), ('109', '9'), ('3', '3'), ('13', '3'), 
        ('23', '3'), ('33', '3'), ('43', '3'), ('53', '3'), ('63', '3'), 
        ('73', '3'), ('83', '3'), ('93', '3'), ('103', '3'), ('113', '3')
    ]

    associates_program_term_to_term = [
    ('152', '48'),
    ('147', '43'),
    ('142', '38'),
    ('137', '33'),
    ('132', '28'),
    ('126', '22'),
    ('121', '17'),
    ('116', '12'),
    ('6', '6'),
    ('16', '6'),
    ('26', '6'),
    ('36', '6'),
    ('46', '6'),
    ('56', '6'),
    ('66', '6'),
    ('76', '6'),
    ('86', '6'),
    ('96', '6'),
    ('106', '6')
    ]

    
    # Function to insert program_term_to_term pairs for Bachelor's program

    def insert_bachelors_program_term_to_term(bachelors_program_term_to_term):
        bachelor_program_terms = []
        for program_term, program in bachelors_program_term_to_term:
            start_date = datetime(2005, 1, 1)
            end_date = datetime(2016, 12, 31)
        # Generate a date between the start and end dates
            start_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
            end_date = start_date + timedelta(days=365)  # Add one year to the start date
            max_capacity = random.randint(20, 50)
            description = fake.sentence()
            
            bachelor_program_terms.append((program_term, program, start_date, end_date, max_capacity, description))

        cursor = connection.cursor()

        insert_query = "INSERT INTO Program_Term (program_term_id, program_id, start_date, end_date, max_capacity, description) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, bachelor_program_terms)
        connection.commit()
        print(
        f"Inserted {len(bachelor_program_terms)} bachelors records into the Program_Term table.")


    def insert_masters_program_term_to_term(masters_program_term_to_term):
        masters_program_terms = []
        for program_term, program in masters_program_term_to_term:
            start_date = datetime(2016, 1, 1)
            end_date = datetime(2021, 12, 31)
        # Generate a date between the start and end dates
            start_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
            end_date = start_date + timedelta(days=365)
            max_capacity = random.randint(20, 50)
            description = fake.sentence()
            
            masters_program_terms.append((program_term, program, start_date, end_date, max_capacity, description))

        cursor = connection.cursor()
        insert_query = "INSERT INTO Program_Term (program_term_id, program_id, start_date, end_date, max_capacity, description) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, masters_program_terms)
        connection.commit()
        print(f"Inserted {len(masters_program_terms)} master's records into the Program_Term table.")

    def insert_phd_program_term_to_term(phd_program_term_to_term):
        phd_program_terms = []
        for program_term, program in phd_program_term_to_term:
            start_date = datetime(2022, 1, 1)
            end_date = datetime(2023, 12, 31)
            start_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
            end_date = start_date + timedelta(days=365)
            max_capacity = random.randint(20, 50)
            description = fake.sentence()
            
            phd_program_terms.append((program_term, program, start_date, end_date, max_capacity, description))

        cursor = connection.cursor()
        insert_query = "INSERT INTO Program_Term (program_term_id, program_id, start_date, end_date, max_capacity, description) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, phd_program_terms)
        connection.commit()
        print(f"Inserted {len(phd_program_terms)} PhD records into the Program_Term table.")


    def insert_associates_program_term_to_term(associates_program_term_to_term):
        associates_program_terms = []
        for program_term, program in associates_program_term_to_term:
            # Define the start and end dates
            start_date = datetime(2005, 1, 1)
            end_date = datetime(2016, 12, 31)
            # Generate a date between the start and end dates
            start_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
            # Calculate the end date one year after the start date
            end_date = start_date + timedelta(days=365)
            max_capacity = random.randint(20, 50)
            description = fake.sentence()
            
            associates_program_terms.append((program_term, program, start_date, end_date, max_capacity, description))

        cursor = connection.cursor()
        insert_query = "INSERT INTO Program_Term (program_term_id, program_id, start_date, end_date, max_capacity, description) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, associates_program_terms)
        connection.commit()
        print(f"Inserted {len(associates_program_terms)} associates records into the Program_Term table.")

    # Insert Bachelor's program term to term pairs
    insert_bachelors_program_term_to_term(bachelors_program_term_to_term)
    
    # Insert Masters program term to term pairs
    insert_masters_program_term_to_term(masters_program_term_to_term)
    
    # Insert PhD program term to term pairs
    insert_phd_program_term_to_term(phd_program_term_to_term)

    insert_associates_program_term_to_term(associates_program_term_to_term)

# CHECK AGAIN AND ADD MORE WHEN GPT4 AVIALABLE.
# MAKE SURE THAT THE PROGRAM_TERM_IDS MATCH THE UOP COURSES IN MOST CASES.
def generate_and_insert_modules(connection):

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
        (51, 4, 'Global Political Systems', 'Art History', 4, 'Fall'),
        (52, 4, 'International Relations Theory', 'International Law', 4, 'Spring'),
        (53, 10, 'Literary Analysis and Criticism', 'Art History', 3, 'Fall'),
        (54, 10, 'Contemporary World Literature', 'Art History', 3, 'Spring'),
        # (55, 20, 'Sociological Theories', 'Sociology', 3, 'Fall'),
        # (56, 20, 'Social Research Methods', 'Sociology', 4, 'Spring'),
        # (57, 26, 'Psychological Perspectives', 'Psychology', 3, 'Fall'),
        # (58, 26, 'Cognitive Psychology', 'Psychology', 4, 'Spring'),
        # (59, 36, 'Creative Writing Techniques', 'Creative Writing', 4, 'Fall'),
        # (60, 36, 'Screenwriting Fundamentals', 'Creative Writing', 4, 'Spring'),
        # (61, 41, 'Political Theory', 'Political Science', 4, 'Fall'),
        # (62, 41, 'Public Policy Analysis', 'Political Science', 4, 'Spring'),
        # (63, 46, 'Economic Theory', 'Economics', 4, 'Fall'),
        # (64, 46, 'Global Economy and Markets', 'Economics', 4, 'Spring'),
        # (65, 31, 'Philosophy of Science', 'Philosophy', 3, 'Fall'),
        # (66, 31, 'Ethics and Morality', 'Philosophy', 3, 'Spring'),
        # (67, 3, 'Sustainable Engineering Practices', 'Sustainable Architecture', 4, 'Fall'),
        # (68, 3, 'Water Resources Engineering', 'Sustainable Architecture', 4, 'Spring'),
        # (69, 9, 'Structural Dynamics in Civil Engineering', 'Structural Engineering', 4, 'Fall'),
        # (70, 9, 'Geotechnical Engineering Principles', 'Structural Engineering', 4, 'Spring'),
        # (71, 14, 'Renewable Energy Technologies', 'Sustainable Architecture', 4, 'Fall'),
        # (72, 14, 'Energy Systems and Sustainability', 'Sustainable Architecture', 4, 'Spring'),
        # (73, 19, 'Aerospace Propulsion Systems', 'Architectural Design', 4, 'Fall'),
        # (74, 19, 'Flight Mechanics and Control', 'Architectural Design', 4, 'Spring'),
        # (75, 25, 'Thermodynamics in Mechanical Engineering', 'Architectural Design', 4, 'Fall'),
        # (76, 25, 'Fluid Mechanics and Dynamics', 'Architectural Design', 4, 'Spring'),
        # (77, 30, 'Electrical Circuits and Systems', 'Urban Planning', 4, 'Fall'),
        # (78, 30, 'Digital Signal Processing', 'Urban Planning', 4, 'Spring'),
        # (79, 35, 'Computer Systems Architecture', 'Urban Planning', 4, 'Fall'),
        # (80, 35, 'Embedded Systems Design', 'Urban Planning', 4, 'Spring'),
    ]

    cursor = connection.cursor()

    insert_query = "INSERT INTO Modules(module_id, program_term_id, module_name, module_subject, module_points, semester) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(insert_query, modules_list)
    connection.commit()
    print(f"Inserted {len(modules_list)} records into the Modules table.")

# CHECK AGAIN I AM NOT SURE IF DATA ARE CORRECT. MAKE SURE TO MATCH STUDENTS WITH MODULES 
# ALSO ACCORDING TO WHAT THEY HAVE SIGNED UP TO? 
# NEEDS FIXING
#HERE WE USE PARAMETER FROM MODULES ABOVE 
def generate_and_insert_student_module_participation(connection, num):
    student_module_participations = []
    module_id_range = list(range(1, 54))  # Example range, adjust based on your data
    student_id_range = list(range(1, num))  # Example range, adjust based on your data

    for i in range(num):
        module_id = random.choice(module_id_range)
        student_id = random.choice(student_id_range)

        student_module_participation = (
            i,  # experience_id
            module_id,
            student_id,
        )
        student_module_participations.append(student_module_participation)

    cursor = connection.cursor()
    insert_query = """
    INSERT INTO StudentModuleParticipation 
    (stud_mod_id, module_id, student_id) 
    VALUES (%s, %s, %s)
    """

    try:
        cursor.executemany(insert_query, student_module_participations)
        connection.commit()
        print(f"Inserted {len(student_module_participations)} records into the StudentModuleParticipation table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


bachelor_program_term_ids = [
    4, 10, 14, 20, 24, 30, 34, 40, 44, 50,
    54, 60, 64, 70, 74, 80, 84, 90, 94, 100,
    104, 110, 114, 119, 124, 130, 135, 140, 145, 150,
    155, 156, 157, 158, 159, 160, 161, 162, 163, 164,
    165, 166, 167, 168, 169, 170, 171, 172, 173, 174,
    175, 176, 177, 178, 179, 180, 181, 182
]

master_program_term_ids = [
    1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111,
    2, 12, 22, 32, 42, 52, 62, 72, 82, 92, 102, 112,
    5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105,
    7, 17, 27, 37, 47, 57, 67, 77, 87, 97, 107,
    8, 18, 28, 38, 48, 58, 68, 78, 88, 98, 108,
    115, 117, 120, 122, 125, 127, 128, 131, 133, 136, 138, 141, 143, 146, 148, 151, 153, 154
]

phd_program_term_ids = [
    3, 13, 23, 33, 43, 53, 63, 73, 83, 93, 103, 113,
    9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109,
    118, 123, 129, 134, 139, 144, 149
]

program_term_related_to_uni_pi_ids = [
    117, 126, 2, 12, 22, 32, 42, 52, 62, 72, 82, 92, 102, 112,
    6, 16, 26, 36, 46, 56, 66, 76, 86, 96, 106, 154, 128, 1,
    11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111, 7, 17, 27,
    37, 47, 57, 67, 77, 87, 97, 107, 121, 127, 132, 137, 142,
    144, 147, 149, 153, 155, 165
]

# check again if students involved with unipi. check if no errors 
def generate_and_insert_enrollments(connection, num_students):
    enrollments = []
    enrollment_id_counter = 1

    students = [fake.random_int(min=1, max=10000) for _ in range(num_students)]

    # Enroll every student in a UniPi program
    for student_id in range(1,9999):
        uni_pi_program_term_id = random.choice(program_term_related_to_uni_pi_ids)
        uni_pi_registration_date = fake.date_between(start_date="-4y", end_date="-3y")

        enrollments.append(
            (enrollment_id_counter, student_id, uni_pi_program_term_id, uni_pi_registration_date)
        )
        enrollment_id_counter += 1

    # Enroll all students in a Bachelor program
    for student_id in  range(1,10001):
        bachelor_program_term_id = random.choice(bachelor_program_term_ids)
        bachelor_registration_date = fake.date_between(start_date="-3y", end_date="-2y")

        enrollments.append(
            (enrollment_id_counter, student_id, bachelor_program_term_id, bachelor_registration_date)
        )
        enrollment_id_counter += 1

    # Select half of the students for Master's programs
    master_students = random.sample(students, len(students) // 2)
    for student_id in master_students:
        master_program_term_id = random.choice(master_program_term_ids)
        master_registration_date = fake.date_between(start_date="-2y", end_date="-1y")

        enrollments.append(
            (enrollment_id_counter, student_id, master_program_term_id, master_registration_date)
        )
        enrollment_id_counter += 1

    # Select half of the Master's students for Ph.D. programs
    phd_students = random.sample(master_students, len(master_students) // 2)
    for student_id in phd_students:
        phd_program_term_id = random.choice(phd_program_term_ids)
        phd_registration_date = fake.date_between(start_date="-1y", end_date="today")

        enrollments.append(
            (enrollment_id_counter, student_id, phd_program_term_id, phd_registration_date)
        )
        enrollment_id_counter += 1

    # Insert enrollments into the database
    cursor = connection.cursor()
    insert_query = "INSERT INTO Enrollment (enrollment_id, student_id, program_term_id, registration_date) VALUES (%s, %s, %s, %s)"
    try:
        cursor.executemany(insert_query, enrollments)
        connection.commit()
        print(f"Inserted {len(enrollments)} records into the Enrollment table successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Working perfect 
def generate_and_insert_companies(connection, num):
    cursor = connection.cursor()

    companies = []

    for i in range(1, num + 1):
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

# Working perfect 
def generate_and_insert_job_titles(connection, num):
    cursor = connection.cursor()

    job_titles = []

    for i in range(1, num + 1):
        job_title = (
            i,  # title_id
            fake.job(),  # title_name
            random.choice(['SoftwareEngineering', 'accounting', 'Shipping',
                          'DataScience', 'Business', 'Sales', 'Consulting']),  # job_type
            random.choice(['Internship', 'Apprenticeship ', 'Permanent']),
            fake.text(max_nb_chars=255),  # description
        )
        job_titles.append(job_title)

    # Assuming your table has columns (title_id, title_name, job_type, description)
    insert_query = "INSERT INTO JobTitle (title_id, title_name, job_category, job_type, description) VALUES (%s, %s, %s, %s, %s)"

    try:
        cursor.executemany(insert_query, job_titles)
        connection.commit()
        print(f"Inserted {len(job_titles)} records into the JobTitle table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Working perfect 
def generate_and_insert_graduations(connection, num):
    graduations = []
    location_id_range = list(range(1, 12000))  # Assuming you have 99 possible locations

    # Generate graduation data based on enrollment ids
    for enrollment_id in range(1, num + 1):
        final_grade = random.randint(60, 100)  # Assume grade range is 60 to 100
        graduation_date = fake.date_between(start_date="today", end_date="+4y")
        top_of_class = random.choice([True, False])
        location_id = random.choice(location_id_range)

        graduation = (
            enrollment_id,             
            enrollment_id,              
            final_grade,                
            graduation_date,            
            top_of_class,               
            location_id,                
        )
        graduations.append(graduation)

    cursor = connection.cursor()
    insert_query = """
    INSERT INTO Graduation 
    (graduation_id, enrollment_id, final_grade, graduation_date, top_of_class, location_id) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(insert_query, graduations)
        connection.commit()
        print(f"Inserted {len(graduations)} records into the Graduation table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Working but fix the ranges here to be real.
# NEEDS STUDENT,COMPANY,JOB TITLE DATA

def generate_and_insert_work_experiences(connection, num):
    work_experiences = []
    student_id_range = list(range(1, 10000))  # Example range, adjust based on your data
    company_id_range = list(range(1, 300))  # Example range, adjust based on your data
    job_title_id_range = list(range(1, 800))  # Example range, adjust based on your data

    for i, _ in enumerate(range(num), start=1):
        student_id = random.choice(student_id_range)
        company_id = random.choice(company_id_range)
        job_title_id = random.choice(job_title_id_range)
        start_date = fake.date_between(start_date="-5y", end_date="today")
        end_date = fake.date_between(start_date=start_date, end_date="+2y")
        description = fake.sentence(nb_words=10)
        responsibilities = fake.sentence(nb_words=15)

        # Append the counter 'i' as experience_id
        work_experience = (
            i,                         # Counter for experience_id
            student_id,               
            company_id,               
            job_title_id,            
            start_date,               
            end_date,                
            description,              
            responsibilities,         
        )
        work_experiences.append(work_experience)

    # Assuming 'connection' is your MySQL database connection
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO WorkExperience 
    (experience_id, student_id, company_id, job_title_id, start_date, end_date, description, responsibilities) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(insert_query, work_experiences)
        connection.commit()
        print(f"Inserted {len(work_experiences)} records into the Work Experience table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()



