from django.urls import path
from . import views  # ✅ Ensure correct import

urlpatterns = [
    path('',views.login_view,name="login"),
    path('logout/',views.logout_view,name='logout_view'),
    path('main-admin-dashboard/',views.main_admin_dashboard,name='main_admin_dashboard'),
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/<int:pk>/delete/', views.delete_department, name='delete_department'),
    path('department/dashboard/', views.department_dashboard, name='department_dashboard'),

    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),  # ✅ Added delete path
    path('add-subject/', views.add_subject, name='add_subject'),
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),  # ✅ Added edit path for subjects
    path('view-subject/<int:subject_id>/', views.view_subject, name='view_subject'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),  # ✅ Added delete path for subjects
    path('add-classroom/', views.add_classroom, name='add_classroom'),
    path('delete-classroom/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),  # ✅ Added delete path for classrooms
    path('add-batch/', views.add_batch, name='add_batch'),
    path('delete-batch/<int:batch_id>/', views.delete_batch, name='delete_batch'),  # ✅ Added delete path for batches
    path('add-division/', views.add_division, name='add_division'),
    path('delete-division/<int:division_id>/', views.delete_division, name='delete_division'),  # ✅ Added delete path for divisions
    path('add-year/', views.add_year, name='add_year'),
    path('delete-year/<int:year_id>/', views.delete_year, name='delete_year'),  # ✅ Delete functionality
    # path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('view-timetable/', views.view_timetable, name='view_timetable'),
    path('get-divisions/', views.get_divisions, name='get_divisions'),
    path('get-years/', views.get_years, name='get_years'),
    path('get-teachers/', views.get_teachers, name='get_teachers'),
    path('get-classrooms/', views.get_classrooms, name='get_classrooms'),
    path('get-batches/', views.get_batches, name='get_batches'),
    path('generate-timetable/', views.manual_timetable, name='manual_timetable'),
    path('timetable/manual/', views.manual_timetable, name='manual_timetable'),
    path('manual-timetable/', views.manual_timetable, name='manual_timetable'),
    path('delete-all-timetable-entries/', views.delete_all_timetable_entries, name='delete_all_timetable_entries'),
    path('delete-timetable-entry/<int:entry_id>/', views.delete_timetable_entry, name='delete_timetable_entry'),
    path('save-timetable-entry/', views.save_timetable_entry, name='save_timetable_entry'),
    path('select-department-timetable/', views.select_department_timetable, name='select_department_timetable'),
    path('view-department-timetable/', views.view_department_timetable, name='view_department_timetable'),
    path('view-meta-timetable/', views.view_meta_timetable, name='view_meta_timetable'),
    path('download-timetable/<str:format>/', views.download_timetable, name='download_timetable'),
]