-- 1 Έλεγχος έγκυρου πεδίου email για τους φοιτητές.

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

-- 2 Για να γίνει εισαγωγή φοιτητή σε μεταπτυχιακό πρόγραμμα θα πρέπει να υπάρχει εισαγωγή προπτυχιακού τίτλου σπουδών.

DELIMITER $$
CREATE TRIGGER BeforeEnrollInAdvancedProgram
BEFORE INSERT ON Enrollment
FOR EACH ROW
BEGIN
    DECLARE hasBachelors INT;

    SELECT COUNT(*) INTO hasBachelors
    FROM Enrollment e
    JOIN Program_Term pt ON e.program_term_id = pt.program_term_id
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Degree d ON p.awarded_degree = d.degree_id
    JOIN EducationLevel el ON d.education_level_id = el.level_id
    WHERE e.student_id = NEW.student_id
    AND el.level_name = 'Bachelors';

    SELECT IF(el.level_name IN ('Masters', 'Phd'), TRUE, FALSE) INTO @isAdvanced
    FROM Program_Term pt
    JOIN Program p ON pt.program_id = p.program_id
    JOIN Degree d ON p.awarded_degree = d.degree_id
    JOIN EducationLevel el ON d.education_level_id = el.level_id
    WHERE pt.program_term_id = NEW.program_term_id;

    IF @isAdvanced AND hasBachelors = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student must be enrolled in a Bachelor''s program before enrolling in a Master''s or PhD program.';
    END IF;
END$$
DELIMITER ;

-- 3 Αύξηση αριθμού εργαζομένων εταιρείας με βάση τις εργασιακές εμπειρίες των φοιτητών.

DELIMITER $$
CREATE TRIGGER IncrementEmployeeCountAfterWorkExperienceAdded
AFTER INSERT ON WorkExperience
FOR EACH ROW
BEGIN
    DECLARE jobType VARCHAR(255);
    SELECT jt.job_type INTO jobType
    FROM WorkExperience we
    JOIN JobTitle jt ON we.job_title_id = jt.title_id
    WHERE we.experience_id = NEW.experience_id;
    
    IF jobType = 'Permanent' THEN
        UPDATE Company
        SET employees = employees + 1
        WHERE company_id = NEW.company_id;
    END IF;
END$$
DELIMITER ;