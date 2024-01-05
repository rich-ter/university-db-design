
-- this is working fine - FINAL 
CREATE TABLE Student (
    StudentID int NOT NULL,
  	FirstName varchar(255) NOT NULL, 
    LastName varchar(255) NOT NULL,
    FatherName varchar(255) NOT NULL,
    Email varchar(255) NOT NULL,
    DateOfBirth DATE NOT NULL,
    RegistrationYear YEAR NOT NULL
    --IsCurrentStudent Boolean NOT NULL,
);

CREATE TABLE WorkPlacement (
    PlacementID int NOT NULL,
  	CompanyName varchar(255) NOT NULL, 
    CompanyIndustry varchar(255) NOT NULL,
    JobTitle varchar(255) NOT NULL,
    --THE REASON THAT WE INCLUDE PARTICULAR SELECTIONS HERE IS SO WE CAN THEN GROUP BY THOSE CLOSEST ONES AND BRING THE STATISTICS BACK]--
    JobType ENUM  NOT NULL(
        'Software Engineer',
        'Business Analyst',
        'Sales',
        'Operations',
        'Other'
    ), 
    StartingDate DATE NOT NULL,
    FinishDate DATE NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES Student
);

CREATE TABLE Program (
    ProgramID int NOT NULL,
  	ProgramName varchar(255) NOT NULL, 
    UniversityName varchar(255) NOT NULL,
    FacultyName varchar(255) NOT NULL,
    ProgramType ENUM NOT NULL (
        'Bachelors Program',
        'Masters Program',
        'PhD Program'
    ), 
    StartingDate DATE NOT NULL,
    FinishDate DATE NOT NULL
);

CREATE TABLE Enrolment (
    EnrolmentID int NOT NULL,
    PRIMARY KEY (EnrolmentID),
    FOREIGN KEY (StudentID) REFERENCES Student,
    FOREIGN KEY (ProgramID) REFERENCES Program
);


-- Mock data for the Student table with 50 examples
INSERT INTO Student (StudentID, FirstName, LastName, FatherName, Email, DateOfBirth, RegistrationYear)
VALUES
    (1, 'John', 'Doe', 'Michael Doe', 'john.doe@example.com', '1995-05-10', 2020),
    (2, 'Jane', 'Smith', 'David Smith', 'jane.smith@example.com', '1998-07-15', 2019),
    (3, 'Robert', 'Johnson', 'James Johnson', 'robert.johnson@example.com', '1997-03-22', 2021),
    (4, 'Emily', 'Brown', 'Richard Brown', 'emily.brown@example.com', '1996-11-30', 2020),
    (5, 'Michael', 'Williams', 'Thomas Williams', 'michael.williams@example.com', '1999-02-18', 2018),
    (6, 'Linda', 'Davis', 'Mark Davis', 'linda.davis@example.com', '1997-08-05', 2017),
    (7, 'William', 'Jones', 'Joseph Jones', 'william.jones@example.com', '1998-04-12', 2019),
    (8, 'Sarah', 'Miller', 'Steven Miller', 'sarah.miller@example.com', '1996-06-28', 2020),
    (9, 'David', 'Garcia', 'Edward Garcia', 'david.garcia@example.com', '1994-12-17', 2018),
    (10, 'Olivia', 'Martinez', 'Daniel Martinez', 'olivia.martinez@example.com', '1997-10-22', 2019),
    (11, 'James', 'Hernandez', 'Paul Hernandez', 'james.hernandez@example.com', '1996-03-14', 2021),
    (12, 'Sophia', 'Lopez', 'George Lopez', 'sophia.lopez@example.com', '1995-09-07', 2017),
    (13, 'Benjamin', 'Wilson', 'William Wilson', 'benjamin.wilson@example.com', '1998-01-25', 2018),
    (14, 'Mia', 'Gonzalez', 'Charles Gonzalez', 'mia.gonzalez@example.com', '1996-04-29', 2020),
    (15, 'Daniel', 'Smith', 'Richard Smith', 'daniel.smith@example.com', '1999-07-03', 2019),
    (16, 'Ava', 'Davis', 'Matthew Davis', 'ava.davis@example.com', '1997-12-11', 2020),
    (17, 'Alexander', 'Lee', 'Robert Lee', 'alexander.lee@example.com', '1998-08-15', 2017),
    (18, 'Isabella', 'Jackson', 'Brian Jackson', 'isabella.jackson@example.com', '1995-02-28', 2020),
    (19, 'Matthew', 'Harris', 'Kenneth Harris', 'matthew.harris@example.com', '1996-10-01', 2018),
    (20, 'Ella', 'Taylor', 'Timothy Taylor', 'ella.taylor@example.com', '1997-06-14', 2019),
    (21, 'Christopher', 'Clark', 'Jerry Clark', 'christopher.clark@example.com', '1994-03-19', 2018),
    (22, 'Charlotte', 'Young', 'Ronald Young', 'charlotte.young@example.com', '1999-09-26', 2017),
    (23, 'Nicholas', 'Walker', 'Larry Walker', 'nicholas.walker@example.com', '1998-05-07', 2019),
    (24, 'Grace', 'Brown', 'Donald Brown', 'grace.brown@example.com', '1996-07-08', 2020),
    (25, 'Andrew', 'Johnson', 'Samuel Johnson', 'andrew.johnson@example.com', '1997-11-13', 2018),
    (26, 'Madison', 'Anderson', 'Eugene Anderson', 'madison.anderson@example.com', '1995-04-20', 2021),
    (27, 'Daniel', 'Garcia', 'Victor Garcia', 'daniel.garcia@example.com', '1996-12-03', 2020),
    (28, 'Chloe', 'Williams', 'Gregory Williams', 'chloe.williams@example.com', '1998-03-17', 2019),
    (29, 'William', 'Rodriguez', 'Bruce Rodriguez', 'william.rodriguez@example.com', '1997-01-09', 2020),
    (30, 'Avery', 'Smith', 'Ralph Smith', 'avery.smith@example.com', '1995-10-26', 2018),
    (31, 'Sofia', 'Perez', 'Bobby Perez', 'sofia.perez@example.com', '1999-06-06', 2017),
    (32, 'Ethan', 'Gonzalez', 'Roy Gonzalez', 'ethan.gonzalez@example.com', '1996-09-21', 2019),
    (33, 'Amelia', 'Thomas', 'Albert Thomas', 'amelia.thomas@example.com', '1994-02-12', 2018),
    (34, 'Oliver', 'Lopez', 'Ivan Lopez', 'oliver.lopez@example.com', '1997-04-16', 2020),
    (35, 'Lily', 'Hall', 'Louis Hall', 'lily.hall@example.com', '1998-08-27', 2021),
    (36, 'Michael', 'Young', 'Philip Young', 'michael.young@example.com', '1995-03-25', 2019),
    (37, 'Lucas', 'Wilson', 'Wayne Wilson', 'lucas.wilson@example.com', '1999-10-30', 2017),
    (38, 'Evelyn', 'Martin', 'Marvin Martin', 'evelyn.martin@example.com', '1996-07-07', 2020),
    (39, 'Henry', 'Gonzalez', 'Dennis Gonzalez', 'henry.gonzalez@example.com', '1997-05-01', 2018),
    (40, 'Aria', 'Thompson', 'Clarence Thompson', 'aria.thompson@example.com', '1998-12-24', 2020),
    (41, 'Jackson', 'Lewis', 'Russell Lewis', 'jackson.lewis@example.com', '1995-09-10', 2017),
    (42, 'Scarlett', 'Parker','Walter Parker', 'scarlett.parker@example.com', '1994-01-14', 2019),
    (43, 'Liam', 'Smith', 'Frederick Smith', 'liam.smith@example.com', '1996-02-09', 2021),
    (44, 'Victoria', 'White', 'Raymond White', 'victoria.white@example.com', '1999-06-02', 2018),
    (45, 'Mason', 'Hernandez', 'Frank Hernandez', 'mason.hernandez@example.com', '1997-03-18', 2019),
    (46, 'Harper', 'Lee', 'Alan Lee', 'harper.lee@example.com', '1998-04-26', 2020),
    (47, 'Liam', 'Johnson', 'Samuel Johnson', 'liam.johnson@example.com', '1995-11-23', 2018),
    (48, 'Grace', 'Taylor', 'Timothy Taylor', 'grace.taylor@example.com', '1996-08-07', 2017),
    (49, 'Alexander', 'Wright', 'Eugene Wright', 'alexander.wright@example.com', '1994-07-21', 2019),
    (50, 'Aria', 'Brown', 'Lawrence Brown', 'aria.brown@example.com', '1999-05-05', 2021);



-- Mock data for the WorkPlacement table referencing the students
INSERT INTO WorkPlacement (PlacementID, CompanyName, CompanyIndustry, JobTitle, JobType, StartingDate, FinishDate, StudentID)
VALUES
    (1, 'TechCo', 'Technology', 'Software Developer', 'Software Engineer', '2021-06-01', '2022-01-15', 1),
    (2, 'BizCorp', 'Business', 'Business Analyst', 'Business Analyst', '2020-08-10', '2021-03-30', 2),
    (3, 'SalesPro', 'Sales', 'Sales Representative', 'Sales', '2019-04-05', '2020-11-20', 3),
    (4, 'OpsInc', 'Operations', 'Operations Manager', 'Operations', '2022-02-20', '2022-10-30', 4),
    (5, 'Tech Solutions', 'Technology', 'Software Developer', 'Software Engineer', '2020-09-15', '2021-05-28', 5),
    (6, 'Financial Group', 'Finance', 'Financial Analyst', 'Other', '2021-03-10', '2021-11-30', 6),
    (7, 'RetailMart', 'Retail', 'Store Manager', 'Other', '2019-07-10', '2020-12-15', 7),
    (8, 'HealthCare Inc.', 'Healthcare', 'Nurse', 'Other', '2022-01-05', '2022-09-10', 8),
    (9, 'Tech Innovators', 'Technology', 'Data Scientist', 'Software Engineer', '2020-12-15', '2021-08-31', 9),
    (10, 'MarketPro', 'Marketing', 'Marketing Specialist', 'Other', '2019-10-01', '2020-05-15', 10),
    (11, 'Green Energy Corp', 'Energy', 'Environmental Analyst', 'Other', '2021-04-02', '2021-11-15', 11),
    (12, 'TechGenius', 'Technology', 'Software Engineer', 'Software Engineer', '2022-03-10', '2022-10-20', 12),
    (13, 'Financial Wizards', 'Finance', 'Financial Consultant', 'Other', '2020-06-25', '2021-01-10', 13),
    (14, 'SalesPros', 'Sales', 'Sales Manager', 'Sales', '2019-11-20', '2020-08-05', 14),
    (15, 'OpsTech', 'Operations', 'Operations Specialist', 'Operations', '2022-01-15', '2022-09-30', 15),
    (16, 'TechNerds', 'Technology', 'IT Specialist', 'Other', '2021-07-12', '2022-02-28', 16),
    (17, 'BizTech Solutions', 'Business', 'Business Consultant', 'Business Analyst', '2020-10-05', '2021-05-20', 17),
    (18, 'RetailGiant', 'Retail', 'Retail Associate', 'Other', '2019-08-15', '2020-03-31', 18),
    (19, 'HealthCare Innovations', 'Healthcare', 'Medical Researcher', 'Other', '2022-02-10', '2022-10-15', 19),
    (20, 'Tech Wizards', 'Technology', 'Software Tester', 'Software Engineer', '2020-11-15', '2021-06-30', 20),
    (21, 'MarketingGenius', 'Marketing', 'Marketing Manager', 'Other', '2019-12-01', '2020-07-15', 21),
    (22, 'SolarTech', 'Energy', 'Solar Engineer', 'Other', '2021-05-10', '2021-12-25', 22),
    (23, 'DataTech', 'Technology', 'Data Analyst', 'Software Engineer', '2022-03-05', '2022-10-15', 23),
    (24, 'Financial Experts', 'Finance', 'Financial Planner', 'Other', '2020-07-20', '2021-03-05', 24),
    (25, 'SalesForce', 'Sales', 'Sales Coordinator', 'Sales', '2019-10-15', '2020-05-30', 25),
    (26, 'OpsWorld', 'Operations', 'Logistics Manager', 'Operations', '2022-02-20', '2022-09-15', 26),
    (27, 'TechPro', 'Technology', 'Software Developer', 'Software Engineer', '2020-09-25', '2021-05-10', 27),
    (28, 'Financial Insights', 'Finance', 'Financial Analyst', 'Other', '2021-04-15', '2021-11-30', 28),
    (29, 'RetailPro', 'Retail', 'Store Manager', 'Other', '2019-07-25', '2020-12-10', 29),
    (30, 'HealthTech', 'Healthcare', 'Healthcare Administrator', 'Other', '2022-01-10', '2022-09-25', 30),
    (31, 'TechInnovate', 'Technology', 'Data Scientist', 'Software Engineer', '2020-12-25', '2021-08-10', 31),
    (32, 'MarketBuzz', 'Marketing', 'Marketing Specialist', 'Other', '2019-10-15', '2020-05-31', 32),
    (33, 'EcoTech', 'Energy', 'Environmental Analyst', 'Other', '2021-04-20', '2021-11-05', 33),
    (34, 'DataWizards', 'Technology', 'Software Engineer', 'Software Engineer', '2022-03-15', '2022-10-30', 34),
    (35, 'FinanceTech', 'Finance', 'Financial Consultant', 'Other', '2020-06-30', '2021-01-15', 35);

questions:
Can a student be registered but not enroled? 
