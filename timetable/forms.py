from django import forms
from django.contrib.auth.models import User
from .models import Teacher, Subject, Classroom, Batch, Division, Year, Department, BatchTeacher


# ✅ Department Form
class DepartmentForm(forms.ModelForm):
    admin_username = forms.CharField(max_length=150)
    admin_password = forms.CharField(widget=forms.PasswordInput)
    admin_email = forms.EmailField()

    class Meta:
        model = Department
        fields = ['name', 'code']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('admin_username')
        email = cleaned_data.get('admin_email')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        return cleaned_data

    def save(self, commit=True):
        department = super().save(commit=False)
        if commit:
            # Create department admin user
            admin_user = User.objects.create_user(
                username=self.cleaned_data['admin_username'],
                email=self.cleaned_data['admin_email'],
                password=self.cleaned_data['admin_password']
            )
            department.admin = admin_user
            department.save()
        return department

# ✅ Teacher Form
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)

# ✅ Classroom Form
class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'is_lab']

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)

# ✅ Batch Form
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)

# ✅ Division Form (Allows multiple batch selection)
class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name', 'batches']
        widgets = {
            'batches': forms.CheckboxSelectMultiple(attrs={'class': 'batch-checkboxes'})
        }

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if self.department:
            self.fields['batches'].queryset = Batch.objects.filter(department=self.department)
        # Add a label for the batches field
        self.fields['batches'].label = "Select Batches for this Division"
        # Add help text
        self.fields['batches'].help_text = "Choose which batches belong to this division"

# ✅ Year Form (Select fixed classroom and divisions)
class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['year', 'classroom', 'divisions']
        widgets = {
            'divisions': forms.CheckboxSelectMultiple()  # ✅ Multi-select for divisions
        }

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if self.department:
            # Only show non-lab classrooms
            self.fields['classroom'].queryset = Classroom.objects.filter(department=self.department, is_lab=False)
            self.fields['divisions'].queryset = Division.objects.filter(department=self.department)

# ✅ Subject Form (Handles Theory & Practical Selection)
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'division', 'year', 'is_theory', 'is_practical', 
                 'lecture_hours', 'theory_teacher', 'classroom', 
                 'practical_hours', 'lab', 'batches']

    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if self.department:
            self.fields['division'].queryset = Division.objects.filter(department=self.department)
            self.fields['year'].queryset = Year.objects.filter(department=self.department)
            self.fields['theory_teacher'].queryset = Teacher.objects.filter(department=self.department)
            self.fields['classroom'].queryset = Classroom.objects.filter(department=self.department)
            self.fields['lab'].queryset = Classroom.objects.filter(department=self.department, is_lab=True)
            self.fields['batches'].queryset = Batch.objects.filter(department=self.department)
            
            # Customize year field choices to show division, year, and classroom
            year_choices = []
            for year in self.fields['year'].queryset:
                division_names = ", ".join([div.name for div in year.divisions.all()])
                classroom_name = year.classroom.name if year.classroom else "No Classroom"
                year_choices.append((
                    year.id,
                    f"{division_names} - {year.year} Year - {classroom_name}"
                ))
            self.fields['year'].choices = [("", "Select Year")] + year_choices
            
        # Make batches not required (handled by JS for practical)
        self.fields['batches'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_theory = cleaned_data.get("is_theory")
        lecture_hours = cleaned_data.get("lecture_hours")
        theory_teacher = cleaned_data.get("theory_teacher")
        is_practical = cleaned_data.get("is_practical")
        practical_hours = cleaned_data.get("practical_hours")
        lab = cleaned_data.get("lab")
        batches = cleaned_data.get("batches")

        # ✅ Validate Theory Selection
        if is_theory and (lecture_hours <= 0 or not theory_teacher):
            raise forms.ValidationError("If theory is selected, lecture hours must be > 0 and a theory teacher must be assigned.")

        # ✅ Validate Practical Selection
        if is_practical and (practical_hours <= 0 or not lab or not batches):
            raise forms.ValidationError("If practical is selected, practical hours must be > 0, a lab must be assigned, and at least one batch must be selected.")

        return cleaned_data

class BatchTeacherForm(forms.ModelForm):
    class Meta:
        model = BatchTeacher
        fields = ['batch', 'teacher']
        
    def __init__(self, *args, **kwargs):
        self.department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if self.department:
            self.fields['batch'].queryset = Batch.objects.filter(department=self.department)
            self.fields['teacher'].queryset = Teacher.objects.filter(department=self.department)

BatchTeacherFormSet = forms.inlineformset_factory(
    Subject, BatchTeacher,
    form=BatchTeacherForm,
    extra=1,
    can_delete=True
)
