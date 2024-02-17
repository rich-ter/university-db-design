-- VIEWS
CREATE VIEW NotAffiliatedWithUniPi AS
SELECT s.student_id, s.first_name, s.last_name
FROM Student s
WHERE NOT EXISTS (
    SELECT 1
    FROM Enrollment e
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Faculty f ON p.faculty_id = f.faculty_id
    JOIN University u ON f.university_id = u.university_id
    WHERE s.student_id = e.student_id
    AND u.university_name = 'University of Piraeus'
);

CREATE VIEW ProgramTermsPerYear AS
SELECT p.program_id, p.program_name, YEAR(pt.start_date) AS year, COUNT(pt.program_term_id) AS term_count
FROM Program p
JOIN Program_Term pt ON p.program_id = pt.program_id
WHERE YEAR(pt.start_date) BETWEEN 2013 AND 2023
GROUP BY p.program_id, p.program_name, YEAR(pt.start_date)
ORDER BY YEAR(pt.start_date) ASC, p.program_id; -- Sorted by year from earliest to latest, then by program_id


CREATE VIEW FacultyProgramsCountView AS
SELECT f.faculty_id, f.faculty_name, COUNT(p.program_id) AS program_count
FROM Faculty f
JOIN Program p ON f.faculty_id = p.faculty_id
GROUP BY f.faculty_id, f.faculty_name;


CREATE VIEW CompanyExperienceCountView AS
SELECT c.company_id, c.company_name, c.industry, COUNT(we.experience_id) AS total_experiences
FROM Company c
LEFT JOIN WorkExperience we ON c.company_id = we.company_id
GROUP BY c.company_id, c.company_name, c.industry
ORDER BY total_experiences DESC;

-- ROLES 
CREATE ROLE 'Administrator';
CREATE ROLE 'AcademicStaff';
CREATE ROLE 'DataAnalyst';
CREATE ROLE 'CompanyRepresentative';
CREATE ROLE 'StudentServicesOfficer';

GRANT ALL PRIVILEGES ON *.* TO 'Administrator';

GRANT SELECT, INSERT, UPDATE ON `Modules` TO 'AcademicStaff';

GRANT SELECT ON `University` TO 'DataAnalyst';
GRANT SELECT ON `Faculty` TO 'DataAnalyst';
GRANT SELECT ON `Program` TO 'DataAnalyst';
GRANT SELECT ON `Modules` TO 'DataAnalyst';
GRANT SELECT ON `Student` TO 'DataAnalyst';
GRANT SELECT ON `Enrollment` TO 'DataAnalyst';
GRANT SELECT ON `Company` TO 'DataAnalyst';
GRANT SELECT ON `WorkExperience` TO 'DataAnalyst';

GRANT SELECT, INSERT, UPDATE ON `Company` TO 'CompanyRepresentative';
GRANT SELECT, INSERT, UPDATE ON `WorkExperience` TO 'CompanyRepresentative';

GRANT SELECT, INSERT, UPDATE ON `Student` TO 'StudentServicesOfficer';
GRANT SELECT, INSERT, UPDATE ON `Enrollment` TO 'StudentServicesOfficer';
GRANT SELECT, INSERT, UPDATE ON `Graduation` TO 'StudentServicesOfficer';

GRANT 'Administrator' TO 'username'@'host';

FLUSH PRIVILEGES;


