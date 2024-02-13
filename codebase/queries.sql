-- 1. Πλήθος εγγραφών ανά πρόγραμμα σπουδών για το πανεπιστημιο Πειραια 
SELECT p.program_id, p.program_name, COUNT(e.student_id) AS Σύνολο Εγγραφών
FROM Program p
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Enrollment e ON pt.program_term_id = e.program_term_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
WHERE u.university_name = 'University of Piraeus'
GROUP BY p.program_id, p.program_name;

-- 2. Πλήθος και ποσοστό παροχής εργασιακών εμπειριών ανα εταιρια 
SELECT c.company_name, COUNT(we.experience_id) AS Αριθμός Προσλήψεων, ROUND((COUNT(we.experience_id) * 100.0 / total.total_count), 2) AS Ποσοστό σε σχέση με τις προσλήψεις
FROM Company c
JOIN WorkExperience we ON c.company_id = we.company_id
CROSS JOIN (SELECT COUNT(*) as total_count FROM WorkExperience) total
GROUP BY c.company_name, total.total_count
ORDER BY number_of_experiences DESC;

-- 3. Ποσοστο αριστούχων μαθητών ανά πανεπιστήμιο
SELECT u.university_name, COUNT(CASE WHEN g.top_of_class THEN 1 ELSE NULL END) * 100.0 / COUNT(*) AS % Αριστούχοι
FROM Graduation g
JOIN Enrollment e ON g.enrollment_id = e.enrollment_id
JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
JOIN Program p ON pt.program_id = p.program_id
JOIN Faculty f ON p.faculty_id = f.faculty_id
JOIN University u ON f.university_id = u.university_id
GROUP BY u.university_name
ORDER BY Top_Percentage DESC;

-- 4. Πλήθος μαθημάτων ανά πρόγραμμα σπουδών ανα πανεπιστήμιο
SELECT u.university_name AS Πανεπιστήμιο, p.program_name AS Πρόγραμμα_Σπουδών,
    COUNT(m.module_id) AS Συνολικός_Αριθμός_Μαθημάτων
FROM University u
JOIN Faculty f ON u.university_id = f.university_id
JOIN Program p ON f.faculty_id = p.faculty_id
JOIN Program_Term pt ON p.program_id = pt.program_id
JOIN Modules m ON pt.program_term_id = m.program_term_id
GROUP BY u.university_name, f.faculty_name, p.program_name
ORDER BY u.university_name, f.faculty_name, p.program_name;

-- 5. Πληθος και ποσοστο εργασιακων τίτλων ανά αύξουσα σειρά 
SELECT jt.title_name AS `Θέση_Εργασίας`, COUNT(we.job_title_id) AS `Πλήθος`, ROUND((COUNT(we.job_title_id) * 100.0 / (SELECT COUNT(*) FROM WorkExperience)), 2) AS `% Συνόλου`
FROM WorkExperience we
JOIN JobTitle jt ON we.job_title_id = jt.title_id
GROUP BY jt.title_name
ORDER BY `Πλήθος` DESC;

-- 6. 10 πόλεις με τις περισσότερες εταιρείες 
SELECT l.city AS Πόλη, COUNT(DISTINCT c.company_id) AS Πλήθος_Εταιρειών
FROM Company c
JOIN Location l ON c.location_id = l.location_id
GROUP BY l.city
ORDER BY Πλήθος_Εταιρειών DESC
LIMIT 10;


