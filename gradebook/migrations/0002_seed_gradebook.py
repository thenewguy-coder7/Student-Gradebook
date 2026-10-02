from django.db import migrations

STUDENTS = [
    ("KN0001", "Kwame", "Mensah"), ("KN0002", "Ama", "Owusu"),
    ("KN0003", "Kojo", "Asante"), ("KN0004", "Abena", "Boateng"),
    ("KN0005", "Kofi", "Adjei"), ("KN0006", "Akosua", "Bonsu"),
    ("KN0007", "Yaw", "Osei"), ("KN0008", "Adwoa", "Appiah"),
    ("KN0009", "Kwesi", "Agyeman"), ("KN0010", "Esi", "Frimpong"),
    ("KN0011", "Nana", "Yeboah"), ("KN0012", "Akua", "Asamoah"),
    ("KN0013", "Kwaku", "Darko"), ("KN0014", "Mawuli", "Kudjo"),
    ("KN0015", "Efua", "Amoah"), ("KN0016", "Fiifi", "Addo"),
    ("KN0017", "Maame", "Sarpong"), ("KN0018", "Selorm", "Ahiable"),
]

COURSES = [
    ("COE301", "Database Systems"),
    ("COE302", "Software Engineering"),
    ("COE303", "Computer Networks"),
    ("COE304", "Operating Systems"),
    ("COE305", "Web Development"),
]

# One row per course, one column per student (5 x 18 = 90 results).
MARKS = [
    [48, 57, 86, 87, 82, 79, 97, 41, 79, 47, 64, 73, 73, 83, 72, 49, 95, 41],
    [43, 78, 49, 58, 82, 84, 94, 81, 52, 59, 84, 57, 78, 81, 58, 80, 85, 94],
    [70, 83, 76, 69, 51, 46, 82, 63, 95, 82, 86, 53, 71, 57, 83, 90, 81, 68],
    [74, 45, 32, 46, 56, 63, 97, 49, 73, 42, 87, 82, 59, 81, 83, 94, 59, 70],
    [75, 84, 75, 35, 55, 43, 52, 47, 92, 58, 80, 61, 48, 97, 97, 99, 44, 37],
]


def load_data(apps, schema_editor):
    Student = apps.get_model("gradebook", "Student")
    Course = apps.get_model("gradebook", "Course")
    Result = apps.get_model("gradebook", "Result")

    students = [
        Student.objects.create(
            index_number=idx,
            first_name=first,
            last_name=last,
            email=f"{first.lower()}.{last.lower()}@knust.example",
        )
        for idx, first, last in STUDENTS
    ]
    courses = [Course.objects.create(code=c, title=t) for c, t in COURSES]

    Result.objects.bulk_create(
        Result(student=students[s], course=courses[c], marks=MARKS[c][s])
        for c in range(len(courses))
        for s in range(len(students))
    )


def clear_data(apps, schema_editor):
    for name in ("Result", "Student", "Course"):
        apps.get_model("gradebook", name).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("gradebook", "0001_initial")]
    operations = [migrations.RunPython(load_data, clear_data)]
