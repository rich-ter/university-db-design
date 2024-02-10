
-- student table

CREATE INDEX idx_student_last_name ON Student(last_name);
CREATE INDEX idx_student_first_name ON Student(first_name);
CREATE UNIQUE INDEX idx_student_email_unique ON Student(email);


-- Η δημιουργία ενός δείκτη στο location_id βοηθάει στη βελτίωση της απόδοσης των ερωτημάτων 
-- που εκτελούν JOIN μεταξύ των πινάκων University και Location, καθώς και σε ερωτήματα που 
-- φιλτράρουν ή ταξινομούν με βάση την τοποθεσία του πανεπιστημίου.
CREATE INDEX idx_university_location ON University(location_id);

--Οι δείκτες στα university_id και location_id βελτιστοποιούν τις επιδόσεις των JOIN ερωτημάτων 
--με τους πίνακες University και Location αντίστοιχα, καθώς και των ερωτημάτων που αναζητούν συγκεκριμένες 
--σχολές με βάση το πανεπιστήμιο ή την τοποθεσία.
CREATE INDEX idx_faculty_university ON Faculty(university_id);
CREATE INDEX idx_faculty_location ON Faculty(location_id);

--Επιταχύνουν τα ερωτήματα που συνδέουν προγράμματα με συγκεκριμένες σχολές ή βαθμίδες εκπαίδευσης, 
--βοηθώντας στη γρήγορη ανάκτηση προγραμμάτων βάσει της σχολής ή του επιπέδου εκπαίδευσης.
CREATE INDEX idx_program_faculty ON Program(faculty_id);
CREATE INDEX idx_program_awarded_degree ON Program(awarded_degree);

-- Βελτιώνει την απόδοση των ερωτημάτων που αναζητούν όρους προγραμμάτων με βάση συγκεκριμένα προγράμματα, 
--καθιστώντας την αντιστοίχιση μεταξύ των προγραμμάτων και των όρων πιο αποδοτική.
CREATE INDEX idx_program_term_program ON Program_Term(program_id);

--Αυτοί οι δείκτες επιταχύνουν τις αναζητήσεις και τις λειτουργίες JOIN για τις εγγραφές φοιτητών σε 
--συγκεκριμένους όρους προγραμμάτων, κάνοντας τις επερωτήσεις πιο αποδοτικές.
CREATE INDEX idx_enrollment_student ON Enrollment(student_id);
CREATE INDEX idx_enrollment_program_term ON Enrollment(program_term_id);
CREATE INDEX idx_enrollment_registration_date ON Enrollment(registration_date);

--Βελτιστοποιούν την απόδοση των ερωτημάτων που σχετίζονται με την εμπειρία εργασίας φοιτητών, εταιρειών, 
--και τίτλων εργασίας, κάνοντας τις αναζητήσεις και τις αναλύσεις πιο γρήγορες και αποδοτικές.
CREATE INDEX idx_work_experience_student ON WorkExperience(student_id);
CREATE INDEX idx_work_experience_company ON WorkExperience(company_id);
CREATE INDEX idx_work_experience_job_title ON WorkExperience(job_title_id);

