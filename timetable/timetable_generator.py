import random
from django.db import transaction
from .models import Timetable, Subject, Teacher, Classroom, Batch, Division, TimeSlot

def generate_timetable():
    """
    Generate a timetable for all subjects
    """
    # Clear existing timetable entries
    Timetable.objects.all().delete()

    # Get all subjects
    subjects = Subject.objects.all()

    # Get all time slots and days
    time_slots = list(TimeSlot.objects.all())
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Track teacher and lab schedules to avoid conflicts
    teacher_schedule = {}
    lab_schedule = {}

    timetable_entries = []

    for subject in subjects:
        # Theory scheduling
        if subject.is_theory and subject.lecture_hours > 0:
            available_slots = random.sample(time_slots, subject.lecture_hours)

            for slot in available_slots:
                assigned_day = random.choice(days)

                # Conflict check - Teacher & Classroom
                if (
                    (subject.theory_teacher.id, assigned_day, slot.id) not in teacher_schedule and
                    (subject.classroom.id, assigned_day, slot.id) not in lab_schedule
                ):
                    # Create timetable entry
                    timetable_entries.append(
                        Timetable(
                            subject=subject,
                            teacher=subject.theory_teacher,
                            classroom=subject.classroom,
                            time_slot=slot,
                            day=assigned_day,
                            division=subject.division
                        )
                    )

                    # Track conflicts
                    teacher_schedule[(subject.theory_teacher.id, assigned_day, slot.id)] = True
                    lab_schedule[(subject.classroom.id, assigned_day, slot.id)] = True

        # Practical scheduling
        if subject.is_practical and subject.practical_hours > 0:
            batches = subject.batches.all()
            batch_hours = subject.practical_hours // len(batches)  # Equally distribute hours

            for batch in batches:
                batch_teacher = subject.batch_teachers.filter(batch=batch).first()
                if not batch_teacher:
                    continue  # Skip if no teacher assigned for this batch
                    
                available_slots = random.sample(time_slots, batch_hours)

                for slot in available_slots:
                    assigned_day = random.choice(days)

                    # Conflict check - Teacher & Lab
                    if (
                        (batch_teacher.teacher.id, assigned_day, slot.id) not in teacher_schedule and
                        (subject.lab.id, assigned_day, slot.id) not in lab_schedule
                    ):
                        # Create timetable entry
                        timetable_entries.append(
                            Timetable(
                                subject=subject,
                                teacher=batch_teacher.teacher,
                                lab=subject.lab,
                                time_slot=slot,
                                day=assigned_day,
                                division=subject.division,
                                batch=batch
                            )
                        )

                        # Track conflicts
                        teacher_schedule[(batch_teacher.teacher.id, assigned_day, slot.id)] = True
                        lab_schedule[(subject.lab.id, assigned_day, slot.id)] = True

    # Bulk insert for performance optimization
    Timetable.objects.bulk_create(timetable_entries)
    print("✅ Timetable generated successfully!")