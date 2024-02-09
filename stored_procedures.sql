Αποθηκευμένες Διαδικασίες (Stored Procedures)

Ενημέρωση εργασιακής εμπειρίας φοιτητή: Επιτρέπει την εύκολη ενημέρωση των καταχωρήσεων εργασιακής εμπειρίας για τους φοιτητές, βοηθώντας στη διατήρηση ενημερωμένων των αρχείων τους στη βάση δεδομένων.

Καταμέτρηση εργασιακών εμπειριών ανά εταιρία: Παρέχει ένα συγκεντρωτικό αριθμό των εργασιακών εμπειριών που προσφέρονται από κάθε εταιρία, επιτρέποντας την αξιολόγηση της συμβολής κάθε εταιρίας στην πρακτική εκπαίδευση των φοιτητών.

Ανάλυση στατιστικών στοιχείων για προγράμματα σπουδών: Συγκεντρώνει στατιστικά στοιχεία για τα προγράμματα σπουδών, όπως αριθμός φοιτητών, ποσοστά επιτυχίας και ακαδημαϊκές επιδόσεις, παρέχοντας ένα εργαλείο για τη βελτίωση και την ανάπτυξη των προγραμμάτων.

Αυτές οι προτάσεις περιλαμβάνουν τόσο τη διαχείριση δεδομένων όσο και την ανάλυση για βελτίωση και αξιολόγηση των προσφερόμενων προγραμμάτων και της συνεισφοράς τους στην εκπαίδευση και την εργασιακή εμπειρία των φοιτητών.

• Να βρεθεί το ποσοστό αποφοίτων ανά έτος, ανά Τμήμα και ανά πρόγραμμα
σπουδών.
• Να βρεθούν οι κατηγορίες απασχόλησης (σε ποσοστό) όπου εργάζονται οι
απόφοιτοι του κάθε Τμήματος.
• Να εντοπιστούν οι απόφοιτοι με «χρονικά κενά» στην επαγγελματική τους
καριέρα, μεγαλύτερα από κάποιο δοθέν διάστημα.
• Να βρεθούν οι απόφοιτοι που φοιτούσαν ταυτόχρονα σε παραπάνω από
ένα Τμήματα, δηλαδή υπάρχει τομή στα διαστήματα φοίτησής τους.


-- 1 Εισαγωγή νέου φοιτητή: Διευκολύνει την εισαγωγή νέων φοιτητών στη βάση δεδομένων, αυτοματοποιώντας τη διαδικασία καταχώρισης των απαραίτητων πληροφοριών για κάθε φοιτητή.


ALSO MAKE SURE THAT THE OPTIONAL RELATIONSHIPS ARE DEPICTED IN THE SCHEMA WITH REMOVING THE NOT NULL PARAMETER. 



DELIMITER //

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
END//

DELIMITER ;


-- παραδειγμα

CALL InsertStudent(10001, 'Φίλιππος', 'Ρίχτερ', 'Δημήτριος', 'me@philipposrichter.com', '1989-01-08');




-- 2 πληθος φοιτητων ανα προγραμμα σπουδων και ανά χρονία

DELIMITER //

CREATE PROCEDURE GetStudentCountsByProgramAndYear(IN university_name VARCHAR(255))
BEGIN
    SELECT 
        p.program_name,
        YEAR(e.registration_date) AS enrollment_year,
        COUNT(*) AS total_students
    FROM Enrollment e
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Faculty f ON p.faculty_id = f.faculty_id
    JOIN University u ON f.university_id = u.university_id AND u.university_name = university_name
    GROUP BY p.program_name, enrollment_year
    ORDER BY p.program_name, enrollment_year;
END //

DELIMITER ;


-- παραδειγμα

CALL GetStudentCountsByProgramAndYear('University of Piraeus');


-- return all work experiences related to students who have had an enrollment in any faculty of the University of Piraeus


-- not working for %. 
DELIMITER $$

CREATE PROCEDURE GetFacultyJobCategoryPercentages(IN universityName VARCHAR(255), IN enrollmentYear YEAR)
BEGIN
    SELECT 
        f.faculty_name,
        we.job_category,
        COUNT(*) AS total_jobs_in_category,
        (COUNT(*) / (SELECT COUNT(*)
                     FROM WorkExperience we2
                     INNER JOIN Student s2 ON we2.student_id = s2.student_id
                     INNER JOIN Enrollment e2 ON s2.student_id = e2.student_id
                     INNER JOIN Program_Term pt2 ON e2.program_term_id = pt2.program_term_id
                     INNER JOIN Program p2 ON pt2.program_id = p2.program_id
                     INNER JOIN Faculty f2 ON p2.faculty_id = f2.faculty_id
                     INNER JOIN University u2 ON f2.university_id = u2.university_id
                     WHERE u2.university_name = universityName
                     AND YEAR(pt2.start_date) = enrollmentYear
                     AND f2.faculty_id = f.faculty_id) * 100) AS percentage
    FROM WorkExperience we
    INNER JOIN Student s ON we.student_id = s.student_id
    INNER JOIN Enrollment e ON s.student_id = e.student_id
    INNER JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    INNER JOIN Program p ON pt.program_id = p.program_id
    INNER JOIN Faculty f ON p.faculty_id = f.faculty_id
    INNER JOIN University u ON f.university_id = u.university_id
    WHERE u.university_name = universityName
    AND YEAR(pt.start_date) = enrollmentYear
    GROUP BY f.faculty_name, we.job_category
    ORDER BY f.faculty_name, percentage DESC;
END$$

DELIMITER ;

-- παραδειγμα

CALL GetFacultyJobCategoryPercentages('University of Piraeus', 2021);


-- ποσοστό κατηγοριών εργασιακής εμπειρίας ανά κατηγορία τμήματος πανεπιστημίου


CREATE PROCEDURE FindJobTitlePercentageForFaculty (
    IN faculty_name VARCHAR(255),
    IN university_name VARCHAR(255)
)
BEGIN
    SELECT 
        jt.title_name AS job_title,
        COUNT(we.job_title_id) AS job_count,
        ROUND((COUNT(we.job_title_id) * 100.0 / (SELECT COUNT(*) FROM WorkExperience WHERE student_id IN (SELECT student_id FROM Enrollment WHERE program_term_id IN (SELECT program_term_id FROM Program_Term WHERE program_id IN (SELECT program_id FROM Program WHERE faculty_id = (SELECT faculty_id FROM Faculty WHERE faculty_name = faculty_name) AND faculty_id IN (SELECT faculty_id FROM Faculty WHERE university_id = (SELECT university_id FROM University WHERE university_name = university_name))))))), 2) AS percentage
    FROM WorkExperience we
    JOIN JobTitle jt ON we.job_title_id = jt.title_id
    WHERE we.student_id IN (SELECT student_id FROM Enrollment WHERE program_term_id IN (SELECT program_term_id FROM Program_Term WHERE program_id IN (SELECT program_id FROM Program WHERE faculty_id = (SELECT faculty_id FROM Faculty WHERE faculty_name = faculty_name) AND faculty_id IN (SELECT faculty_id FROM Faculty WHERE university_id = (SELECT university_id FROM University WHERE university_name = university_name))))))
    GROUP BY jt.title_name
    ORDER BY percentage DESC;
END;






-------------------------------------------------------------------------------------------------------------------------




-- 2. Ανάκτηση ποσοστό φοιτητών ανά τμήμα πανεπιστημίου.

SELECT 
    f.faculty_name,
    COUNT(e.student_id) AS total_students,
    COUNT(e.student_id) / total.total_students * 100 AS percentage
FROM Faculty f
JOIN University u ON f.university_id = u.university_id
JOIN Program p ON f.faculty_id = p.faculty_id
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Enrollment e ON pt.program_term_id = e.program_term_id
JOIN (
    SELECT COUNT(e.student_id) AS total_students
    FROM University u
    JOIN Faculty f ON u.university_id = f.university_id
    JOIN Program p ON f.faculty_id = p.faculty_id
    JOIN Program_Term pt ON p.program_id = pt.program_id
    JOIN Enrollment e ON pt.program_term_id = e.program_term_id
    WHERE u.university_name = 'University of Piraeus'
) AS total ON 1=1
WHERE u.university_name = 'University of Piraeus'
GROUP BY f.faculty_name;



--- Φοιτητες οι οποιοι ειναι ανεργοι ακομα και μετα απο 1 χρονο αποφοιτησης τους. 


-- ποσοστό εγγραφών ανά τμήμα (Faculty) του Πανεπιστημίου Πειραιά
SELECT f.faculty_name,
    COUNT(e.enrollment_id) AS total_enrollments,
    (COUNT(e.enrollment_id) * 100.0 / (SELECT COUNT(en.enrollment_id) 
                                        FROM Enrollment en
                                        JOIN Program_Term pt ON en.program_term_id = pt.program_term_id
                                        JOIN Program p ON pt.program_id = p.program_id
                                        JOIN Faculty fa ON p.faculty_id = fa.faculty_id
                                        JOIN University u ON fa.university_id = u.university_id
                                        WHERE u.university_name = 'University of Piraeus')) AS percentage_of_total
FROM Faculty f
JOIN Program p ON f.faculty_id = p.faculty_id
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Enrollment e ON pt.program_term_id = e.program_term_id
JOIN University u ON f.university_id = u.university_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY f.faculty_name
ORDER BY total_enrollments DESC;

-- ποσοστό και το πλήθος των φοιτητών που έχουν βρει εργασιακή εμπειρία ανά subject_type των προγραμμάτων σπουδών,

SELECT 
    p.subject_type,
    COUNT(DISTINCT e.student_id) AS total_students,
    COUNT(DISTINCT we.student_id) AS students_with_work_experience,
    (COUNT(DISTINCT we.student_id) / COUNT(DISTINCT e.student_id)) * 100 AS percentage_with_work_experience
FROM Program p
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Enrollment e ON pt.program_term_id = e.program_term_id
LEFT JOIN WorkExperience we ON e.student_id = we.student_id
GROUP BY p.subject_type
ORDER BY p.subject_type;

-- ποσοστό τύπου εργασιακής εμπειρίας για τους αποφοίτους του Πανεπιστημίου Πειραιώς, 

SELECT 
    we.job_category,
    COUNT(we.experience_id) AS experience_count,
    (COUNT(we.experience_id) * 100.0 / (SELECT COUNT(*) 
                                        FROM WorkExperience we
                                        JOIN Student s ON we.student_id = s.student_id
                                        JOIN Enrollment e ON s.student_id = e.student_id
                                        JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
                                        JOIN Program p ON pt.program_id = p.program_id
                                        JOIN Faculty f ON p.faculty_id = f.faculty_id
                                        JOIN University u ON f.university_id = u.university_id
                                        WHERE u.university_name = 'University of Piraeus')) AS percentage
FROM WorkExperience we
JOIN Student s ON we.student_id = s.student_id
JOIN Enrollment e ON s.student_id = e.student_id
JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
JOIN Program p ON pt.program_id = p.program_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY we.job_category
ORDER BY experience_count DESC;

 -- ποσοστό φοιτητών που έχουν εργασιακή εμπειρία ανά τίτλο σπουδών (degree)
SELECT 
    d.degree_name,
    COUNT(DISTINCT e.student_id) AS total_students,
    COUNT(DISTINCT we.student_id) AS students_with_work_experience,
    ROUND((COUNT(DISTINCT we.student_id) * 100.0 / COUNT(DISTINCT e.student_id)), 2) AS percentage_with_work_experience
FROM Enrollment e
JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
JOIN Program p ON pt.program_id = p.program_id
JOIN Degree d ON p.awarded_degree = d.degree_id
LEFT JOIN WorkExperience we ON e.student_id = we.student_id
GROUP BY d.degree_name
ORDER BY percentage_with_work_experience DESC, total_students DESC;













Εύρεση του ποσοστού αποφοίτων που βρήκαν εργασία: Υπολογίζει το ποσοστό των αποφοίτων που έχουν εργασιακή εμπειρία, δίνοντας μια εικόνα της επιτυχίας του πανεπιστημίου στην προετοιμασία των φοιτητών για την αγορά εργασίας.

Εύρεση του μέσου βαθμού αποφοίτησης ανά επίπεδο σπουδών: Αναλύει την ακαδημαϊκή επίδοση των αποφοίτων βάσει του επιπέδου των σπουδών τους, παρέχοντας στοιχεία για την αξιολόγηση της ποιότητας της εκπαίδευσης.

