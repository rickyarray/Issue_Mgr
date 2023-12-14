from django.urls import path
from .views import BoardView, StatusUpdateView
from issues import views

urlpatterns = [
    path("", BoardView.as_view(), name="board"),
    # path("edit/status/<int:pk>/", StatusUpdateView.as_view(), name="update_status"),
    path("<int:pk>/", views.IssueDeleteView.as_view(), name="detail"),
]