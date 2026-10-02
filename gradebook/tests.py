from decimal import Decimal

from django.test import TestCase

from .models import Course, Result, Student
from .queries import course_averages, students_below_pass_mark, top_scorers_per_course


class GradebookQueryTests(TestCase):
    def test_seed_data_counts(self):
        self.assertEqual(Student.objects.count(), 18)
        self.assertEqual(Course.objects.count(), 5)
        self.assertEqual(Result.objects.count(), 90)

    def test_top_three_per_course(self):
        rows = list(top_scorers_per_course())
        self.assertEqual(len(rows), 15)
        for course in Course.objects.all():
            best = list(
                Result.objects.filter(course=course)
                .order_by("-marks")
                .values_list("marks", flat=True)[:3]
            )
            got = [r.marks for r in rows if r.course_id == course.id]
            self.assertEqual(got, best)

    def test_below_pass_mark(self):
        qs = students_below_pass_mark()
        self.assertTrue(qs.exists())
        self.assertTrue(all(r.marks < 50 for r in qs))
        self.assertEqual(qs.count(), Result.objects.filter(marks__lt=50).count())

    def test_course_averages_sorted(self):
        avgs = [c.average_marks for c in course_averages()]
        self.assertEqual(avgs, sorted(avgs, reverse=True))
        first = course_averages().first()
        manual = sum(r.marks for r in first.results.all()) / Decimal(18)
        self.assertAlmostEqual(float(first.average_marks), float(manual), places=2)
