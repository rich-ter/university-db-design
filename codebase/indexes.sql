--------- TABLE STUDENT ---------
CREATE INDEX idx_student_last_name ON Student(last_name);
CREATE INDEX idx_student_first_name ON Student(first_name);
CREATE UNIQUE INDEX idx_student_email_unique ON Student(email);

--------- TABLE UNIVERSITY ---------
CREATE INDEX idx_university_location ON University(location_id);

--------- TABLE FACULTY ---------
CREATE INDEX idx_faculty_university ON Faculty(university_id);
CREATE INDEX idx_faculty_location ON Faculty(location_id);

--------- TABLE PROGRAM ---------
CREATE INDEX idx_program_faculty ON Program(faculty_id);
CREATE INDEX idx_program_awarded_degree ON Program(awarded_degree);

--------- TABLE PROGRAM TERM ---------
CREATE INDEX idx_program_term_program ON Program_Term(program_id);

--------- TABLE ENROLLMENT ---------
CREATE INDEX idx_enrollment_student ON Enrollment(student_id);
CREATE INDEX idx_enrollment_program_term ON Enrollment(program_term_id);
CREATE INDEX idx_enrollment_registration_date ON Enrollment(registration_date);

--------- TABLE WORK EXPERIENCE ---------
CREATE INDEX idx_work_experience_student ON WorkExperience(student_id);
CREATE INDEX idx_work_experience_company ON WorkExperience(company_id);
CREATE INDEX idx_work_experience_job_title ON WorkExperience(job_title_id);

