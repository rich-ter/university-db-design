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


-- TO CALL 

SELECT * FROM NotAffiliatedWithUniPi;




