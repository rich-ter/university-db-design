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


-- 4. ΣΩΣΤΟ:query που τον συνολικο αριθμό μαθημάτων ανά πρόγραμμα σπουδών για το πανεπιστήμιο πειραιως
SELECT 
    p.program_name,
    COUNT(m.module_id) AS TotalModules
FROM Modules m
JOIN Program_Term pt ON m.program_term_id = pt.program_term_id
JOIN Program p ON pt.program_id = p.program_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY p.program_name
ORDER BY TotalModules DESC;


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




