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










