--1. Εύρεση φοιτητών που δεν έχουν εργασιακή εμπειρία για το επιλεγμένο διάστημα σε ένα επιλεγμένο τμήμα.

DELIMITER $$
CREATE PROCEDURE FacultyStudentsWithoutWorkInPeriod(
    IN facultyName VARCHAR(255),
    IN startDate DATE,
    IN endDate DATE
)
BEGIN
    SELECT DISTINCT s.student_id, s.first_name, s.last_name, s.email
    FROM Student s
    JOIN Enrollment e ON s.student_id = e.student_id
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Faculty f ON p.faculty_id = f.faculty_id
    LEFT JOIN WorkExperience we ON s.student_id = we.student_id
        AND (
            (we.start_date BETWEEN startDate AND endDate)
            OR
            (we.end_date BETWEEN startDate AND endDate)
        )
    WHERE f.faculty_name = facultyName
        AND we.student_id IS NULL;
END$$
DELIMITER ;

CALL FacultyStudentsWithoutWorkInPeriod('UoP Department of Digital Systems', '1900-08-01', '2500-08-01');

--2. Εύρεση μέσου όρου βαθμού αποφοίτησης ανα πρόγραμμα σπουδών για ένα δοθέν τμήμα. 

DELIMITER $$
CREATE PROCEDURE GetAverageGradesByProgramInFaculty(IN
    inputFacultyName VARCHAR(255)
)
BEGIN
    SELECT
        p.program_name,
        AVG(g.final_grade) AS `ΜΟ Τελικού Βαθμού`
    FROM Graduation g
    JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Faculty f ON p.faculty_id = f.faculty_id
    WHERE f.faculty_name = inputFacultyName
    GROUP BY p.program_name
    ORDER BY `ΜΟ Τελικού Βαθμού` DESC;
END$$
DELIMITER ;

CALL GetAverageGradesByProgramInFaculty('UoP Department of Digital Systems');

--3. Ποσοστό επιτυχίας εύρεσης εργασίας ανάλογα με το πτυχίο των αποφοίτων για ένα δοθέν επίπεδο σπουδών.

DELIMITER $$
CREATE PROCEDURE GetSuccessRatesByEducationLevel(IN inputEducationLevel VARCHAR(255))
BEGIN
    SELECT
        D.degree_name,
        COUNT(DISTINCT S.student_id) AS Σύνολο_Αποφοίτων,
        COUNT(DISTINCT W.student_id) AS Απόφοιτοι_Με_Εμπειρία,
        IF(COUNT(DISTINCT S.student_id) > 0, (COUNT(DISTINCT W.student_id) / COUNT(DISTINCT S.student_id)) * 100, 0) AS Ποσοστό_Επιτυχίας
    FROM
        EducationLevel EL
    JOIN Degree D ON EL.level_id = D.education_level_id
    JOIN Program P ON D.degree_id = P.awarded_degree
    JOIN Program_Term PT ON P.program_id = PT.program_id
    JOIN Enrollment E ON PT.program_term_id = E.program_term_id
    JOIN Student S ON E.student_id = S.student_id
    LEFT JOIN WorkExperience W ON S.student_id = W.student_id
    WHERE EL.level_name = inputEducationLevel
    GROUP BY D.degree_name
    ORDER BY Ποσοστό_Επιτυχίας DESC;
END$$
DELIMITER ;

CALL GetSuccessRatesByEducationLevel('Bachelors');


--4. Για ένα δοθέν τμήμα, επιστροφή εργασιακών τίτλων των αποφοίτων και πλήθος αυτών ανά πρόγραμμα σπουδών. 

DELIMITER $$
CREATE PROCEDURE getJobTitleHiringByProgram(IN inputFacultyName VARCHAR(255))
BEGIN
 SELECT
    p.program_name,
    jt.title_name AS job_title,
    COUNT(*) AS Προσλήψεις
 FROM Student s
 JOIN Enrollment e ON s.student_id = e.student_id
 JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
 JOIN Program p ON pt.program_id = p.program_id
 JOIN Faculty f ON p.faculty_id = f.faculty_id
 JOIN WorkExperience we ON s.student_id = we.student_id
 JOIN JobTitle jt ON we.job_title_id = jt.title_id
 WHERE f.faculty_name = inputFacultyName
 GROUP BY p.program_name, jt.title_name
 ORDER BY p.program_name, COUNT(*) DESC;
END$$
DELIMITER ;

--5. Για ένα δοθέν κωδικό φοιτητή, αναφορά για τις εγγραφές του σε προγράμματα σπουδών και εργασιακές εμπειρίες που έχει αποκτήσει. 

DELIMITER $$
CREATE PROCEDURE `GetStudentProgressReport`(IN student_id_input INT)
BEGIN
    DECLARE student_first_name VARCHAR(255);
    DECLARE student_last_name VARCHAR(255);


    SELECT first_name, last_name
    INTO student_first_name, student_last_name
    FROM Student
    WHERE student_id = student_id_input;


    SELECT CONCAT('Progress Report for Student: ', student_first_name, ' ', student_last_name) AS 'Student Information';


    SELECT E.enrollment_id, p.program_name, pt.start_date AS 'Program Start Date', pt.end_date AS 'Program End Date', g.final_grade
    FROM Enrollment e
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    LEFT JOIN Graduation g ON e.enrollment_id = g.enrollment_id
    WHERE e.student_id = student_id_input;


    SELECT
        w.start_date AS 'Start Date',
        w.end_date AS 'End Date',
        c.company_name AS 'Company',
        jt.title_name AS 'Job Title',
        w.description AS 'Description',
        w.responsibilities AS 'Responsibilities'
    FROM WorkExperience w
    JOIN Company c ON w.company_id = c.company_id
    JOIN JobTitle jt ON w.job_title_id = jt.title_id
    WHERE w.student_id = student_id_input;
END$$
DELIMITER ;

--6. Για ένα δοθέν χρονικό διάστημα και τμήμα πανεπιστημίου, επιστροφή του πλήθους εργασιακών εμπειριών ανά τομέα απασχόλησης αποφοίτων.  

DELIMITER $$
CREATE PROCEDURE GraduateExperiencePerIndustryForGivenTimeAndFaculty(
    IN in_start_year INT,
    IN in_end_year INT,
    IN in_faculty_name VARCHAR(255)
)
BEGIN
    SELECT
        c.industry AS Sector,
        COUNT(DISTINCT we.student_id) AS NumberOfGraduates
    FROM
        WorkExperience we
    JOIN Company c ON we.company_id = c.company_id
    JOIN (
        SELECT DISTINCT e.student_id
        FROM Graduation g
        JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
        JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
        JOIN Program p ON pt.program_id = p.program_id
        JOIN Faculty f ON p.faculty_id = f.faculty_id
        WHERE YEAR(g.graduation_date) BETWEEN in_start_year AND in_end_year
        AND f.faculty_name = in_faculty_name
    ) AS Graduates ON we.student_id = Graduates.student_id
    GROUP BY c.industry
    ORDER BY NumberOfGraduates DESC;
END$$
DELIMITER ;

--7. Απόφοιτοι που εγγράφηκαν ταυτόχρονα σε παραπάνω από ένα προγράμματα σπουδών την ίδια ημερομηνία.
DELIMITER $$
CREATE PROCEDURE FindConcurrentEnrollments()
BEGIN
    SELECT e1.student_id, COUNT(DISTINCT e1.program_term_id) AS concurrent_enrollments
    FROM Enrollment e1
    JOIN Enrollment e2 ON e1.student_id = e2.student_id
                       AND e1.enrollment_id <> e2.enrollment_id
                       AND e1.registration_date = e2.registration_date
    GROUP BY e1.student_id
    HAVING concurrent_enrollments > 1;
END$$
DELIMITER ;

--8. Για ένα δοθέν όνομα Πανεπιστημίου, και χρονικό εύρος, αναφορά για τα προγράμματα σπουδών, τα τμήματα αυτών και τις σχετικές εγγραφές φοιτητών. 

DELIMITER $$
CREATE PROCEDURE `GenerateUniversityProgramReport`(
    IN `university_name` VARCHAR(255),
    IN `start_date` DATE,
    IN `end_date` DATE
)
BEGIN
    SELECT
        p.subject_type,
        COUNT(DISTINCT pt.program_term_id) AS number_of_program_terms,
        COUNT(e.enrollment_id) AS number_of_enrollments
    FROM
        University u
        JOIN Faculty f ON u.university_id = f.university_id
        JOIN Program p ON f.faculty_id = p.faculty_id
        JOIN Program_Term pt ON p.program_id = pt.program_id
        LEFT JOIN Enrollment e ON pt.program_term_id = e.program_term_id
    WHERE
        u.university_name = university_name
        AND pt.start_date >= start_date
        AND pt.end_date <= end_date
    GROUP BY
        p.subject_type;
    SELECT
        p.program_name,
        COUNT(DISTINCT pt.program_term_id) AS number_of_program_terms,
        COUNT(e.enrollment_id) AS registrations
    FROM
        University u
        JOIN Faculty f ON u.university_id = f.university_id
        JOIN Program p ON f.faculty_id = p.faculty_id
        JOIN Program_Term pt ON p.program_id = pt.program_id
        LEFT JOIN Enrollment e ON pt.program_term_id = e.program_term_id
    WHERE
        u.university_name = university_name
        AND pt.start_date >= start_date
        AND pt.end_date <= end_date
    GROUP BY
        p.program_name;
END$$
DELIMITER ;


