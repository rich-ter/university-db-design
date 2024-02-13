--------- TABLE LOCATION ---------
-- INSERT
INSERT INTO Location (location_id, address, city, postcode) 
VALUES (location_id_value, 'address_value', 'city_value', postcode_value);

-- DELETE
DELETE FROM Location WHERE location_id = location_id_value;

-- UPDATE
UPDATE Location SET address = 'new_address_value' WHERE location_id = location_id_value;

--------- TABLE UNIVERSITY ---------
-- INSERT
INSERT INTO University (university_id, university_name, founded_year, website, location_id) 
VALUES (university_id_value, 'university_name_value', founded_year_value, 'website_value', location_id_value);

-- DELETE
DELETE FROM University WHERE university_id = university_id_value;

-- UPDATE
UPDATE University SET university_name = 'new_university_name_value' WHERE university_id = university_id_value;

--------- TABLE FACULTY ---------
-- INSERT
INSERT INTO Faculty (faculty_id, university_id, faculty_name, contact_phone, contact_email, location_id, head_of_faculty) 
VALUES (faculty_id_value, university_id_value, 'faculty_name_value', contact_phone_value, 'contact_email_value', location_id_value, 'head_of_faculty_value');

-- DELETE
DELETE FROM Faculty WHERE faculty_id = faculty_id_value;

-- UPDATE
UPDATE Faculty SET faculty_name = 'new_faculty_name_value' WHERE faculty_id = faculty_id_value;

--------- TABLE EDUCATION LEVEL ---------
-- INSERT
INSERT INTO EducationLevel (level_id, level_name, level, description, ects_requirements) 
VALUES (level_id_value, 'level_name_value', 'level_value', 'description_value', ects_requirements_value);

-- DELETE
DELETE FROM EducationLevel WHERE level_id = level_id_value;

-- UPDATE
UPDATE EducationLevel SET level_name = 'new_level_name_value' WHERE level_id = level_id_value;

--------- TABLE DEGREE ---------
-- INSERT
INSERT INTO Degree (degree_id, education_level_id, degree_name) 
VALUES (degree_id_value, education_level_id_value, 'degree_name_value');

-- DELETE
DELETE FROM Degree WHERE degree_id = degree_id_value;

-- UPDATE
UPDATE Degree SET degree_name = 'new_degree_name_value' WHERE degree_id = degree_id_value;

--------- TABLE PROGRAM ---------
-- INSERT
INSERT INTO Program (program_id, awarded_degree, faculty_id, program_name, year_started, teaching_type, pace, subject_type, semesters) 
VALUES (program_id_value, awarded_degree_value, faculty_id_value, 'program_name_value', year_started_value, 'teaching_type_value', 'pace_value', 'subject_type_value', semesters_value);

-- DELETE
DELETE FROM Program WHERE program_id = program_id_value;

-- UPDATE
UPDATE Program SET program_name = 'new_program_name_value' WHERE program_id = program_id_value;

--------- TABLE PROGRAM TERM ---------
-- INSERT
INSERT INTO Program_Term (program_term_id, program_id, start_date, end_date, max_capacity, description) 
VALUES (program_term_id_value, program_id_value, 'start_date_value', 'end_date_value', max_capacity_value, 'description_value');

-- DELETE
DELETE FROM Program_Term WHERE program_term_id = program_term_id_value;

-- UPDATE
UPDATE Program_Term SET description = 'new_description_value' WHERE program_term_id = program_term_id_value;

--------- TABLE MODULES ---------
-- INSERT
INSERT INTO Modules (module_id, program_term_id, module_name, module_subject, module_points, semester) 
VALUES (module_id_value, program_term_id_value, module_name_value, module_subject_value, module_points_value, semester_value);

-- DELETE
DELETE FROM Modules WHERE module_id = module_id_value;

-- UPDATE
UPDATE Modules SET module_name = new_module_name_value WHERE module_id = module_id_value;

--------- TABLE STUDENT ---------
-- INSERT
INSERT INTO Student (student_id, first_name, last_name, father_name, email, date_of_birth) 
VALUES (student_id_value, first_name_value, last_name_value, father_name_value, email_value, date_of_birth_value);

-- DELETE
DELETE FROM Student WHERE student_id = student_id_value;

-- UPDATE
UPDATE Student SET first_name = new_first_name_value WHERE student_id = student_id_value;

--------- TABLE STUDENT MODULE PARTICIPATION ---------
-- INSERT
INSERT INTO StudentModuleParticipation (stud_mod_id, module_id, student_id) 
VALUES (stud_mod_id_value, module_id_value, student_id_value);

-- DELETE
DELETE FROM StudentModuleParticipation WHERE stud_mod_id = stud_mod_id_value;

-- UPDATE
UPDATE StudentModuleParticipation SET module_id = new_module_id_value WHERE stud_mod_id = stud_mod_id_value;

--------- TABLE ENROLLMENT ---------
-- INSERT
INSERT INTO Enrollment (enrollment_id, student_id, program_term_id, registration_date) 
VALUES (enrollment_id_value, student_id_value, program_term_id_value, registration_date_value);

-- DELETE
DELETE FROM Enrollment WHERE enrollment_id = enrollment_id_value;

-- UPDATE
UPDATE Enrollment SET registration_date = new_registration_date_value WHERE enrollment_id = enrollment_id_value;

--------- TABLE GRADUATION ---------
-- INSERT
INSERT INTO Graduation (graduation_id, enrollment_id, final_grade, graduation_date, top_of_class, location_id) 
VALUES (graduation_id_value, enrollment_id_value, final_grade_value, graduation_date_value, top_of_class_value, location_id_value);

-- DELETE
DELETE FROM Graduation WHERE graduation_id = graduation_id_value;

-- UPDATE
UPDATE Graduation SET final_grade = new_final_grade_value WHERE graduation_id = graduation_id_value;

--------- TABLE COMPANY ---------
-- INSERT
INSERT INTO Company (company_id, company_name, location_id, employees, industry) 
VALUES (company_id_value, company_name_value, location_id_value, employees_value, industry_value);

-- DELETE
DELETE FROM Company WHERE company_id = company_id_value;

-- UPDATE
UPDATE Company SET company_name = new_company_name_value WHERE company_id = company_id_value;

--------- TABLE JOB TITLE ---------
-- INSERT
INSERT INTO JobTitle (title_id, title_name, job_type, job_category, description) 
VALUES (title_id_value, title_name_value, job_type_value, job_category_value, description_value);

-- DELETE
DELETE FROM JobTitle WHERE title_id = title_id_value;

-- UPDATE
UPDATE JobTitle SET title_name = new_title_name_value WHERE title_id = title_id_value;

--------- TABLE WORK EXPERIENCE ---------
-- INSERT
INSERT INTO WorkExperience (experience_id, student_id, company_id, job_title_id, start_date, end_date, description, responsibilities) 
VALUES (experience_id_value, student_id_value, company_id_value, job_title_id_value, start_date_value, end_date_value, description_value, responsibilities_value);

-- DELETE
DELETE FROM WorkExperience WHERE experience_id = experience_id_value;

-- UPDATE
UPDATE WorkExperience SET description = new_description_value WHERE experience_id = experience_id_value;
