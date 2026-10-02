"""The three ORM queries required by the assignment."""
from django.db.models import Avg, Case, CharField, Count, F, Value, When, Window
from django.db.models.functions import RowNumber

from .models import Course, Result

PASS_MARK = 50


def top_scorers_per_course(limit=3):
    """Query 1: the best `limit` students in every course.

    A window function numbers the results inside each course (best mark first),
    then we keep only the rows numbered 1..limit. One database query in total.
    """
    return (
        Result.objects.select_related("student", "course")
        .annotate(
            position=Window(
                expression=RowNumber(),
                partition_by=[F("course_id")],
                order_by=[F("marks").desc(), F("student__last_name").asc()],
            )
        )
        .filter(position__lte=limit)
        .order_by("course__code", "position")
    )


def students_below_pass_mark(pass_mark=PASS_MARK):
    """Query 2: every result under the pass mark, with a short remark."""
    return (
        Result.objects.filter(marks__lt=pass_mark)
        .select_related("student", "course")
        .annotate(
            remark=Case(
                When(marks__lt=pass_mark - 10, then=Value("Needs urgent help")),
                default=Value("Close to passing"),
                output_field=CharField(),
            )
        )
        .order_by("marks", "student__last_name")
    )


def course_averages():
    """Query 3: average mark per course (plus class size), highest first."""
    return Course.objects.annotate(
        average_marks=Avg("results__marks"),
        class_size=Count("results"),
    ).order_by("-average_marks", "code")
