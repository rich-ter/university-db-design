


-- 1. ΣΩΣΤΟ Ανάκτηση αριθμού εγγραφών ανά πρόγραμμα σπουδών: Επιστρέφει τον συνολικό αριθμό φοιτητών για κάθε πρόγραμμα, βοηθώντας να κατανοηθεί η δημοφιλία κάθε προγράμματος.

SELECT p.program_id,
       p.program_name,
       COUNT(e.student_id) AS total_students
FROM Program p
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Enrollment e ON pt.program_term_id = e.program_term_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY p.program_id, p.program_name;


-- 2. ΣΩΣΤΟ: ποσοστό κάθε εταιρίας που προσφέρει τις περισσότερες εργασιακές εμπειρίες
SELECT 
    c.company_name,
    COUNT(we.experience_id) AS number_of_experiences,
    ROUND((COUNT(we.experience_id) * 100.0 / total.total_count), 2) AS percentage_of_total_experiences
FROM Company c
JOIN WorkExperience we ON c.company_id = we.company_id
CROSS JOIN (SELECT COUNT(*) as total_count FROM WorkExperience) total
GROUP BY c.company_name, total.total_count
ORDER BY number_of_experiences DESC;


-- 3. ΣΩΣΤΟ:query που γυρναεί όλα τα προγράμματα σπουδών του Πανεπιστημίου του Πειραιώς

SELECT p.*
FROM Program p
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
WHERE u.university_name = 'University of Piraeus';


--------------------------------------------------------------------------------------------------------------------------


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

