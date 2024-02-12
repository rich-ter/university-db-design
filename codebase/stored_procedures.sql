--Εύρεση φοιτητών που δεν έχουν εργασιακή εμπειρία για το επιλεγμένο διάστημα σε ένα επιλεγμένο τμήμα.

DELIMITER $$
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
END$$
DELIMITER ;

--Εύρεση μέσου όρου βαθμού αποφοίτησης ανα πρόγραμμα σπουδών για ένα δόθεν τμήμα. Is this math right? Wtf is avg on final grade?


DELIMITER $$
CREATE PROCEDURE GetAverageGradesByProgramInFaculty(IN
    inputFacultyName VARCHAR(255)
)
BEGIN
    SELECT
        p.program_name,
        AVG(g.final_grade) AS AverageFinalGrade
    FROM Graduation g
    JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Faculty f ON p.faculty_id = f.faculty_id
    WHERE f.faculty_name = inputFacultyName
    GROUP BY p.program_name
    ORDER BY AverageFinalGrade DESC;
END$$
DELIMITER ;

-- Ποσοστο αποφοιτων που βρηκαν εργασία αναλογα με το δοθεν προγραμμα σπουδων

DELIMITER $$
CREATE PROCEDURE GetSuccessRatesByEducationLevel(IN inputEducationLevel VARCHAR(255))
BEGIN
    SELECT
        D.degree_name AS DegreeType,
        COUNT(DISTINCT S.student_id) AS TotalGraduates,
        COUNT(DISTINCT W.student_id) AS StudentsWithWorkExperience,
        IF(COUNT(DISTINCT S.student_id) > 0, (COUNT(DISTINCT W.student_id) / COUNT(DISTINCT S.student_id)) * 100, 0) AS SuccessRate
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
    ORDER BY SuccessRate DESC;
END$$
DELIMITER ;

-- Για ένα δοθέν τμήμα, επιστροφη του πιο γνωστου εργασιακου τίτλου με βάση των αριθμό των προσλήψεων και αυτος ο αριθμος ανα πρόγραμμα σπουδών.

DELIMITER $$
CREATE PROCEDURE getJobTitleHiringByProgram(IN
    inputFacultyName VARCHAR(255)
)
BEGIN
 SELECT
    program_name,
    title_name AS most_common_job_title,
    Προσλήψεις
FROM (
    SELECT p.program_name, jt.title_name, COUNT(*) AS Προσλήψεις,
        DENSE_RANK() OVER (PARTITION BY p.program_name ORDER BY COUNT(*) DESC) AS rnk
    FROM Faculty f
    JOIN Program p ON f.faculty_id = p.faculty_id
    JOIN Enrollment e ON p.program_id = e.program_term_id
    JOIN Student s ON e.student_id = s.student_id
    JOIN WorkExperience we ON s.student_id = we.student_id
    JOIN JobTitle jt ON we.job_title_id = jt.title_id
    WHERE f.faculty_name = inputFacultyName
    GROUP BY p.program_name, jt.title_name
) AS ranked_titles
WHERE rnk = 1
ORDER BY program_name, Προσλήψεις DESC;
END$$


DELIMITER ;

--Για ένα δοθέν κωδικό φοιτητή, αναφορά για τις εγγραφές του σε προγράμματα σπουδών και εργασιακές εμπειρίες που έχει αποκτήσει. 

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

--Για ένα δόθεν χρονικό διάστημα και τμήμα πανεπιστημίου, επιστροφή των εργασιακών εμπειριών των αποφοίτων. ΑΥΤΟ ΕΙΝΑΙ ΛΑΘΟΣ ΜΕ ΤΗΝ ΗΜΕΡΟΜΗΝΙΑ 

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

-- Απόφοιτοι που εγγράφηκαν ταυτόχρονα σε παραπάνω από ένα Τμήματα.

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

-- GenerateUniversityProgramReport

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
END$$
DELIMITER ;


