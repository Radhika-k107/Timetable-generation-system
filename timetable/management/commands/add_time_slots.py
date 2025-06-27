from django.core.management.base import BaseCommand
from timetable.models import TimeSlot

class Command(BaseCommand):
    help = 'Adds predefined time slots to the database'

    def handle(self, *args, **kwargs):
        # Clear existing time slots
        TimeSlot.objects.all().delete()
        
        # Predefined time slots
        time_slots = [
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
        
        # Create time slots
        for start_time, end_time, id in time_slots:
            TimeSlot.objects.create(
                id=id,
                start_time=start_time,
                end_time=end_time
            )
            self.stdout.write(self.style.SUCCESS(f'Created time slot: {start_time} - {end_time}'))
        
 