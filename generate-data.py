from faker import Faker
import random

fake = Faker('el_GR')  # Set the locale to Greek (Greece)

# Generate fake location entries


def generate_greek_locations(num):
    locations = []
    for _ in range(num):
        location = (
            fake.unique.random_int(min=1, max=1000),  # location_id
            fake.address(),                           # location_address
            fake.city(),                              # city
            fake.random_int(min=10000, max=99999)     # postcode
        )
        locations.append(location)
    return locations

# Generate fake student entries


def generate_student_data(num_students):
    students = []
    for _ in range(num_students):
        student_id = fake.unique.random_int(min=1000, max=9999)
        first_name = fake.first_name()
        last_name = fake.last_name()
        father_name = fake.first_name_male()
        email = fake.email()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=25)

        student = (student_id, first_name, last_name,
                   father_name, email, date_of_birth)
        students.append(student)
    return students

# Generate fake student entries


def generate_company_data(num_companies):
    industries = ['Telecommunications', 'Hospitality', 'Shipping',
                  'Engineering', 'Software', 'Auditing', 'Banking']
    companies = []
    for _ in range(num_companies):
        company_id = fake.unique.random_int(min=1000, max=9999)
        company_name = fake.company()
        # Assuming Location IDs exist in the range [1, 100]
        # here need to add random between entries of location.
        location_id = fake.unique.random_int(min=1, max=100)
        employees = fake.random_int(min=10, max=1000)
        industry = random.choice(industries)

        company = (company_id, company_name, location_id, employees, industry)
        companies.append(company)
    return companies

# Generate fake university entries


def generate_university_data(num_universities):
    athens_universities = [
        "National and Kapodistrian University of Athens",
        "National Technical University of Athens",
        "Athens University of Economics and Business",
        "University of Piraeus",
        "Panteion University of Social and Political Sciences",
        "Harokopio University",
        "Agricultural University of Athens",
        "University of West Attica",
        "University of Peloponnese",
        "Hellenic Open University",
    ]
    universities = []
    for _ in range(num_universities):
        university_id = fake.unique.random_int(min=1000, max=9999)
        university_name = random.choice(athens_universities)
        # Assuming universities founded between 1800 and 2022
        founded_year = fake.random_int(min=1800, max=2022)
        website = fake.url()
        # Assuming Location IDs exist in the range [1, 100]
        location_id = fake.unique.random_int(min=1, max=100)
        faculty_count = fake.random_int(min=10, max=500)

        university = (university_id, university_name, founded_year,
                      website, location_id, faculty_count)
        universities.append(university)
    return universities

# Generate fake faculty data


def generate_random_faculty_data(num_faculties):

    random_faculties = [
        "Faculty of Arts",
        "Faculty of Sciences",
        "Faculty of Engineering",
        "Faculty of Business Administration",
        "Faculty of Social Sciences",
        "Faculty of Medicine",
        "Faculty of Law",
        "Faculty of Economics",
        "Faculty of Information Technology",
        "Faculty of Environmental Sciences",
        "Faculty of Education",
        "Faculty of Agriculture",
        "Faculty of Fine Arts",
        "Faculty of Psychology",
        "Faculty of Communication",
    ]

    faculties = []
    for _ in range(num_faculties):
        faculty_id = fake.unique.random_int(min=1000, max=9999)
        university_id = fake.unique.random_int(min=1000, max=9999)
        # Generate a random word as faculty name
        faculty_name = random.choice(random_faculties)
        contact_phone = fake.random_int(min=1000000000, max=9999999999)
        contact_email = fake.email()
        location_id = fake.unique.random_int(min=1000, max=9999)
        head_of_faculty = fake.name()

        faculty = (faculty_id, university_id, faculty_name,
                   contact_phone, contact_email, location_id, head_of_faculty)
        faculties.append(faculty)
    return faculties


# Example usage:
faculties = generate_random_faculty_data(5)
for faculty in faculties:
    print(faculty)
