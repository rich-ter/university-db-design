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
