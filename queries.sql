-- 1. ΣΩΣΤΟ Ανάκτηση αριθμού εγγραφών ανά πρόγραμμα σπουδών (για όλα τα χρόνια): Επιστρέφει τον συνολικό αριθμό φοιτητών για κάθε πρόγραμμα, βοηθώντας να κατανοηθεί η δημοφιλία κάθε προγράμματος.
SELECT p.program_id, p.program_name, COUNT(e.student_id) AS total_students
FROM Program p
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Enrollment e ON pt.program_term_id = e.program_term_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY p.program_id, p.program_name;


-- 2. ΣΩΣΤΟ: ποσοστό κάθε εταιρίας που προσφέρει τις περισσότερες εργασιακές εμπειρίες
SELECT c.company_name, COUNT(we.experience_id) AS number_of_experiences, ROUND((COUNT(we.experience_id) * 100.0 / total.total_count), 2) AS percentage_of_total_experiences
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


-- 4. ΣΩΣΤΟ:query που τον συνολικο αριθμό μαθημάτων ανά πρόγραμμα σπουδών ανα πανεπιστημιο και τμημα
SELECT u.university_name AS Πανεπιστήμιο, f.faculty_name AS Σχολή, p.program_name AS Πρόγραμμα_Σπουδών,
    COUNT(m.module_id) AS Συνολικός_Αριθμός_Μαθημάτων
FROM University u
JOIN Faculty f ON u.university_id = f.university_id
JOIN Program p ON f.faculty_id = p.faculty_id
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Modules m ON pt.program_term_id = m.program_term_id
GROUP BY u.university_name, f.faculty_name, p.program_name
ORDER BY u.university_name, f.faculty_name, p.program_name;


-- ΣΩΣΤΟ - CHECK AGAIN, αριθμος προγραματων ανα επιπεδο σπουδων για το πανεπιστημιο πειραιως 
SELECT 
    el.level_name,
    COUNT(p.program_id) AS NumberOfPrograms
FROM Program p
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
JOIN Degree d ON p.awarded_degree = d.degree_id
JOIN EducationLevel el ON d.education_level_id = el.level_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY el.level_name
ORDER BY NumberOfPrograms DESC;

-- Ποσοστο μαθητών που αποφοίτησαν με άριστα ανά πανεπιστήμιο.

SELECT u.university_name, COUNT(CASE WHEN g.top_of_class THEN 1 ELSE NULL END) * 100.0 / COUNT(*) AS Top_Percentage
FROM Graduation g
JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
JOIN Program p ON pt.program_id = p.program_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
GROUP BY u.university_name
ORDER BY Top_Percentage DESC;

-- πιο συχνες τιτλοι εργασιων που είχαν οι φοιτητες 

SELECT jt.title_name AS job_title, COUNT(we.job_title_id) AS job_count, ROUND((COUNT(we.job_title_id) * 100.0 / (SELECT COUNT(*) FROM WorkExperience)), 2) AS percentage
FROM WorkExperience we
JOIN JobTitle jt ON we.job_title_id = jt.title_id
GROUP BY jt.title_name
ORDER BY job_count DESC;



-- ΣΩΣΤΟ ? Το ίδιο με παραπάνω αλλα με τις συνολικές εγγραφές που υπάρχουν σε κάθε επίπεδο.
SELECT 
    el.level_name,
    COUNT(DISTINCT p.program_id) AS NumberOfPrograms,
    COUNT(e.enrollment_id) AS TotalEnrollments
FROM Program p
JOIN Degree d ON p.awarded_degree = d.degree_id
JOIN EducationLevel el ON d.education_level_id = el.level_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
LEFT JOIN Program_Term pt ON p.program_id = pt.program_id
LEFT JOIN Enrollment e ON pt.program_term_id = e.program_term_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY el.level_name
ORDER BY NumberOfPrograms DESC;


--

SELECT l.city, COUNT(DISTINCT c.company_id) AS num_of_companies
FROM Company c
JOIN Location l ON c.location_id = l.location_id
GROUP BY l.city
ORDER BY num_of_companies DESC
LIMIT 10;



---------------------------------


--other queries i had made before most prob delete


students who graduated from a course related to the University of Piraeus and haven't had work experience after 1 year of graduating,

SELECT DISTINCT s.student_id, s.first_name, s.last_name
FROM Student s
JOIN Enrollment e ON s.student_id = e.student_id
JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
JOIN Program p ON pt.program_id = p.program_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
LEFT JOIN Graduation g ON e.enrollment_id = g.enrollment_id
LEFT JOIN WorkExperience we ON s.student_id = we.student_id AND we.start_date > DATE_ADD(g.graduation_date, INTERVAL 1 YEAR)
WHERE u.university_name = 'University of Piraeus'
AND g.graduation_id IS NOT NULL
AND we.experience_id IS NULL;


ποσοστό εγγραφών ανά τμήμα (Faculty) του Πανεπιστημίου Πειραιά

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






ποσοστό και το πλήθος των φοιτητών που έχουν βρει εργασιακή εμπειρία ανά subject_type των προγραμμάτων σπουδών,

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


ποσοστό τύπου εργασιακής εμπειρίας για τους αποφοίτους του Πανεπιστημίου Πειραιώς,

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

ποσοστό φοιτητών που έχουν εργασιακή εμπειρία ανά τίτλο σπουδών (degree)

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


 ποσοστό κάθε εταιρίας που προσφέρει τις περισσότερες εργασιακές εμπειρίες

SELECT 
    c.company_name,
    COUNT(we.experience_id) AS number_of_experiences,
    ROUND((COUNT(we.experience_id) * 100.0 / (SELECT COUNT(*) FROM WorkExperience)), 2) AS percentage_of_total_experiences
FROM Company c
JOIN WorkExperience we ON c.company_id = we.company_id
GROUP BY c.company_name
ORDER BY number_of_experiences DESC;
