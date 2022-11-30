from django.urls import path
from question import views

urlpatterns = [
    path('question/data/', views.GetQuestionData.as_view(), name='question-data'),
    path('question/ajax', views.QuestionCreateByAjax.as_view(), name='question-create-ajax')
]