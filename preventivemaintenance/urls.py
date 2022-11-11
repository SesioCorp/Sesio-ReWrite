from django.urls import path
from .views import PreventiveMaintenanceListView, PreventiveMaintenanceDetailView, PreventiveMaintenanceQuestionAnswerView
from .forms import PreventiveMaintenanceForm

Forms = [
    ("PreventiveMaintenanceFrom", PreventiveMaintenanceForm)
    ]

urlpatterns = [
    path('list/', PreventiveMaintenanceListView.as_view(), name='preventive_maintenance_list'),
    path('details/<int:pk>/', PreventiveMaintenanceDetailView.as_view(), name='preventive_maintenance_detail'),
    path("question_answer/create/<str:slug>/<int:pk>/<int:step>/", PreventiveMaintenanceQuestionAnswerView.as_view(),
    name="preventive-maintenance-question-answer-form-step"),
    path("question_answer/create/<str:slug>/<int:pk>/", PreventiveMaintenanceQuestionAnswerView.as_view(),
    name="preventive-maintenance-question-answer-form")
]