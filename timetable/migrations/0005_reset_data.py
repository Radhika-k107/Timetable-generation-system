from django.db import migrations

def reset_data(apps, schema_editor):
    # Get the models
    Batch = apps.get_model('timetable', 'Batch')
    Classroom = apps.get_model('timetable', 'Classroom')
    Teacher = apps.get_model('timetable', 'Teacher')
    TimeSlot = apps.get_model('timetable', 'TimeSlot')
    Division = apps.get_model('timetable', 'Division')
    Subject = apps.get_model('timetable', 'Subject')
    Timetable = apps.get_model('timetable', 'Timetable')
    Year = apps.get_model('timetable', 'Year')
    
    # Clear existing data
    Timetable.objects.all().delete()
    Subject.objects.all().delete()
    Division.objects.all().delete()
    TimeSlot.objects.all().delete()
    Teacher.objects.all().delete()
    Classroom.objects.all().delete()
    Batch.objects.all().delete()
    Year.objects.all().delete()
    
    # Add batches
    batches = [
        ('IF1', 1),
        ('IF2', 2),
        ('IF3', 3),
        ('CM1', 4),
        ('CM2', 5),
        ('CM3', 6)
    ]
    for name, id in batches:
        Batch.objects.create(id=id, name=name)
    
    # Add classrooms
    classrooms = [
        ('M-120', False, 1),
        ('M-122', False, 3),
        ('M-123', False, 13),
        ('M-124', False, 14),
        ('Microprocessor-1', True, 21),
        ('Microprocessor-2', True, 22),
        ('Pro-119-A', True, 23),
        ('Pro-119-B', True, 24),
        ('Pro-119-C', True, 25),
        ('Pro-119-D', True, 26),
        ('Pro-118-A', True, 27),
        ('Pro-118-B', True, 28),
        ('Hardware Lab', True, 29),
        ('Physics Lab', True, 30),
        ('Yoga Hall', False, 32),
        ('Drawing Hall', False, 33)
    ]
    for name, is_lab, id in classrooms:
        Classroom.objects.create(id=id, name=name, is_lab=is_lab)
    
    # Add teachers
    teachers = [
        ('YSP', 11),
        ('CMP', 12),
        ('PRM', 14),
        ('DSP', 15),
        ('SNB', 17),
        ('YPB', 18),
        ('PSS', 19),
        ('NSN', 21),
        ('SCW', 22),
        ('PVS', 23),
        ('TDP', 24),
        ('TMS', 25),
        ('ANM', 26),
        ('SAP', 27),
        ('AHJ', 28),
        ('HHB', 29),
        ('SBN', 30),
        ('MND', 31),
        ('GVG', 32),
        ('VSK', 33),
        ('MPW', 34),
        ('DNB', 35),
        ('MSD', 37),
        ('SML', 38),
        ('PMR', 39)
    ]
    for name, id in teachers:
        Teacher.objects.create(id=id, name=name)
    
    # Add timeslots
    timeslots = [
        ('10:00:00', '11:00:00', 70),
        ('10:00:00', '12:00:00', 71),
        ('11:00:00', '12:00:00', 72),
        ('11:00:00', '13:00:00', 73),
        ('12:00:00', '13:00:00', 74),
        ('13:30:00', '14:30:00', 75),
        ('13:30:00', '15:30:00', 76),
        ('14:30:00', '15:30:00', 77),
        ('15:45:00', '16:45:00', 78),
        ('15:45:00', '17:45:00', 79),
        ('16:45:00', '17:45:00', 80)
    ]
    for start_time, end_time, id in timeslots:
        TimeSlot.objects.create(id=id, start_time=start_time, end_time=end_time)
    
    # Add divisions
    divisions = [
        ('IFA', 1),
        ('CMA', 2)
    ]
    for name, id in divisions:
        Division.objects.create(id=id, name=name)
    
    # Add years
    years = [
        (1, 1, '1st'),
        (3, 3, '3rd'),
        (4, 13, '2nd'),
        (5, 14, '1st'),
        (6, 1, '2nd'),
        (7, 3, '3rd')
    ]
    for id, classroom_id, year in years:
        Year.objects.create(id=id, classroom_id=classroom_id, year=year)

def reverse_data(apps, schema_editor):
    # Get the models
    Batch = apps.get_model('timetable', 'Batch')
    Classroom = apps.get_model('timetable', 'Classroom')
    Teacher = apps.get_model('timetable', 'Teacher')
    TimeSlot = apps.get_model('timetable', 'TimeSlot')
    Division = apps.get_model('timetable', 'Division')
    Subject = apps.get_model('timetable', 'Subject')
    Timetable = apps.get_model('timetable', 'Timetable')
    Year = apps.get_model('timetable', 'Year')
    
    # Clear all data
    Timetable.objects.all().delete()
    Subject.objects.all().delete()
    Division.objects.all().delete()
    TimeSlot.objects.all().delete()
    Teacher.objects.all().delete()
    Classroom.objects.all().delete()
    Batch.objects.all().delete()
    Year.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('timetable', '0004_alter_division_batches'),
    ]

    operations = [
        migrations.RunPython(reset_data, reverse_data),
    ] 