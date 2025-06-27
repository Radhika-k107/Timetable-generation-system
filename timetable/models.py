from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# 1️⃣ Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

# 1️⃣ Teacher Model
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers',null=True, blank=True)

    def __str__(self):
        return self.name

# 2️⃣ Classroom Model
class Classroom(models.Model):
    name = models.CharField(max_length=50)
    is_lab = models.BooleanField(default=False)  # ✅ If true, it's a lab
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classrooms',null=True, blank=True)

    def __str__(self):
        return f"{self.name} {'(Lab)' if self.is_lab else ''}"

# 3️⃣ Division Model (Each division has multiple batches)
class Division(models.Model):
    name = models.CharField(max_length=10, unique=True)
    batches = models.ManyToManyField('Batch', blank=True, related_name='divisions')  # Added related_name for easier access
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='divisions',null=True, blank=True)

    def __str__(self):
        batch_names = ", ".join([batch.name for batch in self.batches.all()])
        return f"{self.name} ({batch_names})"

# 4️⃣ Batch Model (Linked to Division)
class Batch(models.Model):
    name = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='batches',null=True, blank=True)

    def __str__(self):
        return self.name

# 5️⃣ Year Model (Each Year has a Fixed Classroom & Multiple Divisions)
class Year(models.Model):
    YEAR_CHOICES = [
        ('1st', 'First Year'),
        ('2nd', 'Second Year'),
        ('3rd', 'Third Year'),
    ]
    
    year = models.CharField(max_length=3, choices=YEAR_CHOICES)  # Removed unique=True
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='years',null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    divisions = models.ManyToManyField(Division)

    def __str__(self):
        return f"{self.get_year_display()} - {self.classroom.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)  # Removed unique=True
    code = models.CharField(max_length=10)  # Removed unique=True
    division = models.ForeignKey('Division', on_delete=models.CASCADE)
    year = models.ForeignKey('Year', on_delete=models.CASCADE)

    # ✅ Checkboxes for Theory & Practical
    is_theory = models.BooleanField(default=False)
    is_practical = models.BooleanField(default=False)

    # ✅ Theory Fields
    lecture_hours = models.IntegerField(default=0, blank=True, null=True)  # ✅ No. of lecture hours (if theory)
    theory_teacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='theory_subjects'
    )  # ✅ Theory ke liye teacher
    classroom = models.ForeignKey(
        'Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='theory_classroom'
    )  # ✅ Fixed Classroom for Theory Lectures

    # ✅ Practical Fields
    practical_hours = models.IntegerField(default=0, blank=True, null=True)  # ✅ No. of practical hours (if practical)
    lab = models.ForeignKey(
        'Classroom', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_lab': True}, related_name='practical_lab'
    )  # ✅ Fixed Lab for Practicals
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects',null=True, blank=True)
    batches = models.ManyToManyField('Batch', blank=True)  # ✅ Practical ke liye multiple batches assign ho sakte hain
    practical_batch_teachers = models.JSONField(default=dict, blank=True)  # {batch_id: teacher_id, ...}

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.division.name} - {self.year.year}"
  
class BatchTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='batch_teachers')
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('batch', 'subject')
    
    def __str__(self):
        return f"{self.subject.name} - {self.batch.name} - {self.teacher.name}"

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        # Convert to 12-hour format with proper AM/PM
        def format_time(time):
            # Handle special case for 12 PM (noon)
            if time.hour == 12:
                return time.strftime('%I:%M PM')
            # Handle special case for 12 AM (midnight)
            elif time.hour == 0:
                return time.strftime('%I:%M AM')
            # Normal cases
            elif time.hour < 12:
                return time.strftime('%I:%M AM')
            else:
                # Convert 24-hour to 12-hour for PM
                return time.strftime('%I:%M PM')

        return f"{format_time(self.start_time)} - {format_time(self.end_time)}"
    

    def get_duration(self):
        """Get precise duration in hours (including minutes)"""
        today = datetime.today().date()
        start_dt = datetime.combine(today, self.start_time)
        end_dt = datetime.combine(today, self.end_time)

    # Handle overnight time slot (e.g., 11 PM to 1 AM)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)

        duration = end_dt - start_dt
        return duration.total_seconds() / 3600  # returns float hours
        

        
class Timetable(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)  # ✅ For theory
    lab = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True, related_name='lab_sessions')  # ✅ For practical
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)  # ✅ For practicals
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), 
                                                    ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), 
                                                    ('Friday', 'Friday'), ('Saturday', 'Saturday')])

    def __str__(self):
        return f"{self.subject.name} - {self.division.name} - {self.time_slot}"



