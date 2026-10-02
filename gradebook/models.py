from django.db import models


class Student(models.Model):
    index_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.index_number} - {self.full_name}"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=120)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class Result(models.Model):
    """One student's mark in one course."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="results"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="results"
    )
    marks = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["course", "-marks"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="one_result_per_student_per_course",
            ),
            models.CheckConstraint(
                condition=models.Q(marks__gte=0) & models.Q(marks__lte=100),
                name="marks_between_0_and_100",
            ),
        ]

    def __str__(self):
        return f"{self.student.full_name} | {self.course.code} | {self.marks}"
