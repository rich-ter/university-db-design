--------- TABLE STUDENT ---------
CREATE INDEX idx_student_last_name ON Student(last_name);
CREATE INDEX idx_student_first_name ON Student(first_name);
CREATE UNIQUE INDEX idx_student_email_unique ON Student(email);

--------- TABLE ENROLLMENT ---------
CREATE INDEX idx_enrollment_student ON Enrollment(student_id);
CREATE INDEX idx_enrollment_program_term ON Enrollment(program_term_id);
CREATE INDEX idx_enrollment_registration_date ON Enrollment(registration_date);

--------- TABLE PROGRAM TERM ---------
CREATE INDEX idx_program_term_program ON Program_Term(program_id);
CREATE INDEX idx_program_term_start_date ON Program_Term(start_date);
CREATE INDEX idx_program_term_end_Date ON Program_Term(end_date);

--------- TABLE PROGRAM ---------
CREATE INDEX idx_program_faculty ON Program(faculty_id);
CREATE INDEX idx_program_awarded_degree ON Program(awarded_degree);
CREATE INDEX idx_program_name ON Program(program_name);


--------- TABLE DEGREE ---------
CREATE INDEX idx_degree_education_level ON Degree(education_level_id);

--------- TABLE FACULTY ---------
CREATE INDEX idx_faculty_university ON Faculty(university_id);
CREATE INDEX idx_faculty_location ON Faculty(location_id);
CREATE INDEX idx_faculty_name ON Faculty(faculty_name);


--------- TABLE UNIVERSITY ---------
CREATE INDEX idx_university_location ON University(location_id);
CREATE INDEX idx_university_name ON University(university_name);


--------- TABLE WORK EXPERIENCE ---------
CREATE INDEX idx_work_experience_student ON WorkExperience(student_id);
CREATE INDEX idx_work_experience_company ON WorkExperience(company_id);
CREATE INDEX idx_work_experience_job_title ON WorkExperience(job_title_id);
CREATE INDEX idx_work_experience_start_date ON WorkExperience(start_date);
CREATE INDEX idx_work_experience_end_date ON WorkExperience(end_date);

--------- TABLE JOB TITLE ---------
CREATE INDEX idx_job_title_name ON JobTitle(title_name);

--------- TABLE MODULES ---------
CREATE INDEX idx_module_program_term ON Modules(program_term_id);
CREATE INDEX idx_module_name ON Modules(module_name);

--------- TABLE STUDENTMODULEPARTICIPATION ---------
CREATE INDEX idx_student_module_part_stud ON StudentModuleParticipation(student_id);
CREATE INDEX idx_student_module_part_mod ON StudentModuleParticipation(module_id);

--------- TABLE GRADUATION ---------
CREATE INDEX idx_graduation_enrollment ON Graduation(enrollment_id);
CREATE INDEX idx_graduation_final_grade ON Graduation(final_grade);
CREATE INDEX idx_graduation_final_grade ON Graduation(location_id);
