
-- 1 
DELIMITER $$

CREATE TRIGGER BeforeStudentInsertOrUpdate
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid email format: must contain an @ character';
    END IF;
END$$

DELIMITER ;






INSERT INTO Student (student_id, first_name, last_name, email, date_of_birth)
VALUES (1, 'test', 'test', 'invalidemail.com', '2000-01-01');



-- 2 

DELIMITER $$

CREATE TRIGGER BeforeEnrollInAdvancedProgram
BEFORE INSERT ON Enrollment
FOR EACH ROW
BEGIN
    DECLARE hasBachelors INT;

    -- Check if the student being enrolled in a Master's or PhD program has a prior Bachelor's enrollment
    SELECT COUNT(*) INTO hasBachelors
    FROM Enrollment e
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Degree d ON p.awarded_degree = d.degree_id
    JOIN EducationLevel el ON d.education_level_id = el.level_id
    WHERE e.student_id = NEW.student_id
    AND el.level_name = 'Bachelors';

    -- Check the level of the program being enrolled in
    SELECT IF(el.level_name IN ('Masters', 'Phd'), TRUE, FALSE) INTO @isAdvanced
    FROM Program_Term pt
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Degree d ON p.awarded_degree = d.degree_id
    JOIN EducationLevel el ON d.education_level_id = el.level_id
    WHERE pt.program_term_id = NEW.program_term_id;

    -- Prevent the INSERT if it's an advanced program and the student has no Bachelor's enrollment
    IF @isAdvanced AND hasBachelors = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student must be enrolled in a Bachelor''s program before enrolling in a Master''s or PhD program.';
    END IF;
END$$

DELIMITER ;


INSERT INTO Student (student_id, first_name, last_name, email, date_of_birth)
VALUES (10500, 'test', 'test', 'test@example.com', '1995-03-15');
-- Ξέρουμε πως το program_term_id = 1 ισούται με ένα πρόγραμμα σπουδών που είναι μάστερ
INSERT INTO Enrollment (enrollment_id, student_id, program_term_id, registration_date)
VALUES (50000, 10500, 1, '2050-01-01');

INSERT INTO Student (student_id, first_name, last_name, email, date_of_birth)
VALUES (10500, 'test', 'test', 'test@example.com', '1995-03-15');
-- Ξέρουμε πως το program_term_id = 4 ισούται με ένα πρόγραμμα σπουδών που είναι bachelor
INSERT INTO Enrollment (enrollment_id, student_id, program_term_id, registration_date)
VALUES (50000, 10500, 4, '2050-01-01');
-- Ξέρουμε πως το program_term_id = 1 ισούται με ένα πρόγραμμα σπουδών που είναι μάστερ
INSERT INTO Enrollment (enrollment_id, student_id, program_term_id, registration_date)
VALUES (50001, 10500, 1, '2050-01-01');
-- Ξέρουμε πως το program_term_id = 3 ισούται με ένα πρόγραμμα σπουδών που είναι PhD
INSERT INTO Enrollment (enrollment_id, student_id, program_term_id, registration_date)
VALUES (50002, 10500, 3, '2050-01-01');




-- increment company emlpoyee count by 1


DELIMITER $$

CREATE TRIGGER IncrementEmployeeCountAfterWorkExperienceAdded
AFTER INSERT ON WorkExperience
FOR EACH ROW
BEGIN
    -- Increment the employee count for the company associated with the new work experience record
    UPDATE Company
    SET employees = employees + 1
    WHERE company_id = NEW.company_id;
END$$

DELIMITER ;

-- to test 

INSERT INTO WorkExperience (experience_id, student_id, company_id, job_title_id, job_category, start_date, end_date, description, responsibilities)
VALUES (10500, 1, 1, 1, 'SoftwareEngineering', '2022-01-01', '2022-12-31', 'Developed and maintained web applications.', 'Responsible for back-end development');











---------------------------------------------------------------------------










Για να γινει εισαγωγη ενος φοιτητη σε ενα μεταπτυχιακο προγραμμα θα πρεπει να υπαρχει μια εισαγωγη για προπτυχιακο τιτλο σπουδων απο οποιοδηποτε πανεπιστημιο.

DELIMITER //

CREATE TRIGGER prevent_masters_without_bachelors_before_insert
BEFORE INSERT ON Enrollment
FOR EACH ROW
BEGIN
    DECLARE bachelors_exists BOOLEAN;

    -- Check if the student has a bachelor's enrollment
    SELECT EXISTS (
        SELECT 1
        FROM Enrollment e
        JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
        JOIN Program p ON pt.program_id = p.program_id
        JOIN Degree d ON p.awarded_degree = d.degree_id
        JOIN EducationLevel el ON d.education_level_id = el.level_id
        WHERE el.level_name = 'Bachelors' AND e.student_id = NEW.student_id
    ) INTO bachelors_exists;

    -- If the new enrollment is for a master's program and no bachelor's enrollment exists, prevent insertion
    IF (SELECT el.level_name
        FROM Program p
        JOIN Degree d ON p.awarded_degree = d.degree_id
        JOIN EducationLevel el ON d.education_level_id = el.level_id
        WHERE p.program_id = (SELECT program_id FROM Program_Term WHERE program_term_id = NEW.program_term_id)
    ) = 'Masters' AND NOT bachelors_exists THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot enroll in a Master’s program without a Bachelor’s enrollment.';
    END IF;
END;
//
DELIMITER ;








Η εισαγωγή του μεταπτυχιακού τίτλου θα πρέπει να είναι ύστερα απο την χρονική στιγμή της αποφοίτησης του προπτυχιακόυ.

Εφοσων μας ενδιαφερουν μονο αποφοιτοι του πανεπιστημιου πειραιως, τοτε μια εγγραφη σε προγραμμα σπουδων, ειτε προπτυχιακη, μεταπτυχιακη η διδακτορικη για καθε φοιτητη πρεπει να σχετιζεται με το πανεπιστημιο του πειραιως τουλαχιστον μια φορα. Αν δεν υπάρχει, τότε διαγράφεται ο φοιτητής.

Εισαγωγη φοιτητη μονο εφοσων υπαρχει ημερομηνια που αποφοιτησε (πριν την σημερινη).

εφαρμόζεται περιορισμός για τη διατήρηση εργασιακών εμπειριών μόνο κατά το χρονικό διάστημα μετά την αποφοίτηση από ένα πρόγραμμα σπουδών του Πανεπιστημίου Πειραιώς. 
Υποθετουμε πως για εναν φοιτητη μπορεί να γινει η τελευταία του εγγραφή στο πανεπηστημιο πειραιως, οποτε θα φτιαξουμε ενα trigger που κοιτάει κάθε Χ χρονικό διάστημα αν αυτος ο φοιτητης έχει καποια εγγραφή με το πανεηπστημιο πειραιως, και αν δεν έχει καμια τότε να στέλενει ενα μήνυμα στον διαχείριστη για πιθανή διαγραφή.










