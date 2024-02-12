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
        description VARCHAR(255), 
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
   CREATE TABLE IF NOT EXISTS StudentModuleParticipation (
        stud_mod_id INT PRIMARY KEY,
        module_id INT NOT NULL,
        student_id INT NOT NULL,
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
        job_type ENUM('Internship', 'Apprenticeship ', 'Permanent'),
        job_category ENUM('SoftwareEngineering', 'accounting', 'Shipping', 'DataScience', 'Business', 'Sales', 'Consulting'),
        description VARCHAR(255) NOT NULL
    );
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