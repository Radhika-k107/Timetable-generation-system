from django.contrib import admin
from django import forms
from .models import Teacher, Batch, Subject, Classroom, Division, Year,Timetable,TimeSlot

# ✅ Custom Form for Subject Admin (Adding JavaScript)
class SubjectAdminForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

    class Media:
        js = ('admin/js/hide_lab_fields.js',)  # ✅ Custom JavaScript to Show/Hide Lab Fields

# ✅ Updated SubjectAdmin with Custom Form
class SubjectAdmin(admin.ModelAdmin):
    form = SubjectAdminForm
    list_display = ('name', 'code', 'year', 'division', 'is_theory', 'is_practical', 'lecture_hours', 'practical_hours')
    list_filter = ('year', 'division', 'is_theory', 'is_practical')
    search_fields = ('name', 'code')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_lab')
    list_filter = ('is_lab',)

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('batches',)  # ✅ Allow multiple batch selection

class YearAdmin(admin.ModelAdmin):
    list_display = ('year', 'classroom')
    filter_horizontal = ('divisions',)  # ✅ Allow multiple division selection

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)  # ✅ Custom Subject Admin Registered
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Batch)
admin.site.register(Timetable)
admin.site.register(TimeSlot)