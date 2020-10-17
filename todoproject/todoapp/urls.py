from django.urls import include, path
from .views import BucketView, TodoItemView

urlpatterns = [
    path('buckets/', BucketView.as_view()),
    path('bucket/<uuid>/', BucketView.as_view()),
    path('todoitem/', TodoItemView.as_view()),
    path('todoitem/<uuid>/', TodoItemView.as_view())
]
