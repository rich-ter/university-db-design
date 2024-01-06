CREATE TABLE Student (
  student_id INT PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  father_name VARCHAR(255),
  email VARCHAR(255) NOT NULL,
  date_of_birth DATE NOT NULL
);

CREATE TABLE WorkExperience (
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

CREATE TABLE Company (
  company_id INT PRIMARY KEY,
  company_name VARCHAR(255) NOT NULL,
  location_id INT NOT NULL,
  employees INT NOT NULL,
  industry ENUM('Telecommunications', 'Hospitality', 'Shipping', 'Engineering', 'Software', 'Auditing', 'Banking', 'Other'),
  FOREIGN KEY (location_id) REFERENCES Location(location_id)
);

CREATE TABLE JobTitle (
  title_id INT PRIMARY KEY,
  title_name VARCHAR(255) NOT NULL,
  job_type ENUM('SoftwareEngineering', 'accounting', 'Shipping', 'DataScience', 'Business', 'Sales', 'Consulting'),
  description VARCHAR(255) NOT NULL
);

CREATE TABLE Enrollment (
  enrollment_id INT PRIMARY KEY,
  student_id INT NOT NULL,
  program_term_id INT NOT NULL,
  registration_date DATE NOT NULL,
  graduation_id INT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (program_term_id) REFERENCES Program_Term(program_term_id),
  FOREIGN KEY (graduation_id) REFERENCES Graduation(graduation_id)
);

CREATE TABLE Graduation (
  graduation_id INT PRIMARY KEY,
  final_grade INT NOT NULL,
  graduation_date DATE NOT NULL,
  top_of_class BOOLEAN NOT NULL,
  location_id INT NOT NULL,
  FOREIGN KEY (location_id) REFERENCES Location(location_id)
);

CREATE TABLE Program (
  program_id INT PRIMARY KEY,
  awarded_degree INT not null,
  faculty_id INT NOT NULL,
  program_name VARCHAR(255) NOT NULL,
  year_started YEAR NOT NULL,
  teaching_type ENUM('Physical', 'Remote', 'Hybrid'),
  semesters INT NOT NULL,
  FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
  FOREIGN KEY (awarded_degree) REFERENCES Degree(degree_id),
);

CREATE TABLE EducationLevel (
  level_id INT PRIMARY KEY,
  level_name ENUM('Bachelors', 'Masters', 'Phd'),
  description VARCHAR(255),
  entrance_requirements VARCHAR(255) NOT NULL
);

CREATE TABLE Modules (
  module_id INT PRIMARY KEY,
  program_term_id INT NOT NULL,
  module_name VARCHAR(255) NOT NULL,
  module_subject VARCHAR(255) NOT NULL,
  module_points INT NOT NULL,
  semester VARCHAR(255) NOT NULL,
  FOREIGN KEY (program_term_id) REFERENCES Program_Term(program_term_id)
);

CREATE TABLE StudentModuleResults (
  result_id INT PRIMARY KEY,
  module_id INT NOT NULL,
  student_id INT NOT NULL,
  result_grade VARCHAR(255) NOT NULL,
  passed BOOLEAN,
  FOREIGN KEY (module_id) REFERENCES Modules(module_id),
  FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

CREATE TABLE Program_Term (
  program_term_id INT PRIMARY KEY,
  program_id INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  max_capacity INT NOT NULL,
  registered_students INT,
  FOREIGN KEY (program_id) REFERENCES Program(program_id)
);

CREATE TABLE Faculty (
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

CREATE TABLE University (
  university_id INT PRIMARY KEY,
  university_name VARCHAR(255),
  founded_year YEAR,
  website VARCHAR(255),
  location_id INT,
  faculty_count INT,
  FOREIGN KEY (location_id) REFERENCES Location(location_id)
);

CREATE TABLE Location (
  location_id INT PRIMARY KEY,
  address VARCHAR(255) NOT NULL,
  city VARCHAR(255) NOT NULL,
  postcode INT NOT NULL
);

CREATE TABLE Degree (
  degree_id INT PRIMARY KEY,
  education_level_id INT NOT NULL,
  degree_name VARCHAR(255) NOT NULL,
  credits_required INT NOT NULL,
  FOREIGN KEY (education_level_id) REFERENCES EducationLevel(level_id)
);


------------------

