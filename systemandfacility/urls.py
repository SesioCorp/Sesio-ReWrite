from django.urls import path
from systemandfacility import views


urlpatterns = [
    path("building/list/", views.BuildingListView.as_view(), name="building-list"),
    path("floor/list/", views.FloorListView.as_view(), name="floor-list"),
    path("department/list/", views.DepartmentListView.as_view(), name="department-list")
]