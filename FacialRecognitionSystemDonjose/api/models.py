import datetime
import time
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Person(models.Model):
    image = models.BinaryField(null=True, blank=True)  
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    wage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True) 

    pin = models.CharField(max_length=6, validators=[MinLengthValidator(6), MaxLengthValidator(6)], null=True, blank=True)
    security_question = models.CharField(max_length=255, null=True, blank=True)
    security_answer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Person"
    
class Attendance(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(null=True, blank=True)

    time_in_am = models.DateTimeField(null=True, blank=True)
    time_out_am = models.DateTimeField(null=True, blank=True)

    time_in_pm = models.DateTimeField(null=True, blank=True)
    time_out_pm = models.DateTimeField(null=True, blank=True)

    #enw field 
    remarks = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.person.name} - {self.person.role} - {self.person.position} on {self.get_date()}"

    def get_date(self):
        """Return the date of the attendance record."""
        if self.timestamp:
            return self.timestamp.date()
        return "No date"
    

class ExcuseLetter(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    reason = models.TextField()
    
    # Use DateField instead of DateTimeField
    submitted_at = models.DateField(auto_now_add=True, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.person.name} - {self.status}"



# class Excuse(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#         ('Rejected', 'Rejected'),
#     ]

#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     reason = models.TextField()  # The excuse text
#     submitted_at = models.DateTimeField(default=timezone.now)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
#     approved_by = models.ForeignKey(
#         Person, related_name='approved_excuses', on_delete=models.SET_NULL, null=True, blank=True
#     )

#     def __str__(self):
#         return f"{self.person.name} - {self.status} - submitted at {self.submitted_at}"
    
# class Attendance(models.Model):
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
#     # AM shift
#     time_in_am = models.DateTimeField(null=True, blank=True)
#     time_out_am = models.DateTimeField(null=True, blank=True)
#     status_am = models.CharField(
#         max_length=10,
#         choices=[('Present', 'Present'), ('Absent', 'Absent')],
#         default='Absent'
#     )
    
#     # PM shift
#     time_in_pm = models.DateTimeField(null=True, blank=True)
#     time_out_pm = models.DateTimeField(null=True, blank=True)
#     status_pm = models.CharField(
#         max_length=10,
#         choices=[('Present', 'Present'), ('Absent', 'Absent')],
#         default='Absent'
#     )

#     def __str__(self):
#         return f"{self.person.name} - {self.person.role} - {self.person.position} on {self.get_date()}"

#     def get_date(self):
#         if self.time_in_am:
#             return self.time_in_am.date()
#         elif self.time_in_pm:
#             return self.time_in_pm.date()
#         return "No date"