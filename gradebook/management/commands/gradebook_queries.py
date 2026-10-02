from itertools import groupby

from django.core.management.base import BaseCommand

from gradebook.queries import (
    PASS_MARK,
    course_averages,
    students_below_pass_mark,
    top_scorers_per_course,
)


class Command(BaseCommand):
    help = "Print the results of the three gradebook ORM queries."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("\n1) Top 3 scorers per course"))
        rows = top_scorers_per_course()
        for course, group in groupby(rows, key=lambda r: r.course):
            self.stdout.write(f"\n  {course}")
            for r in group:
                self.stdout.write(f"    #{r.position}  {r.student.full_name:<20} {r.marks}")

        self.stdout.write(
            self.style.MIGRATE_HEADING(f"\n2) Results below the pass mark ({PASS_MARK})")
        )
        for r in students_below_pass_mark():
            self.stdout.write(
                f"  {r.student.full_name:<20} {r.course.code}  {r.marks:>6}  ({r.remark})"
            )

        self.stdout.write(self.style.MIGRATE_HEADING("\n3) Course averages, highest first"))
        for c in course_averages():
            self.stdout.write(
                f"  {c.code}  {c.title:<22} avg {c.average_marks:6.2f}  ({c.class_size} students)"
            )
        self.stdout.write("")
