# Student Gradebook System

A Django project that stores students, courses and their marks, and answers
three questions about the data using the Django ORM.

## Models
- `Student` - index number, name, email
- `Course` - code and title
- `Result` - a student's marks in a course (one result per student per course, marks 0-100)

## Seed data
Running `migrate` also loads 18 students, 5 courses and 90 results
(a mix of high, average and below-pass marks).

## The three queries (`gradebook/queries.py`)
1. `top_scorers_per_course()` - top 3 students in each course (window function)
2. `students_below_pass_mark()` - every result under 50, with a remark
3. `course_averages()` - average mark per course, highest first

## Run it
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py gradebook_queries
python manage.py test
```

Optional admin site: `python manage.py createsuperuser`, then `python manage.py runserver`
and open http://127.0.0.1:8000/admin/
