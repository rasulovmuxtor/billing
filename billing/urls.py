from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('student/', views.student_detail, name='student'),
    path('student/pay/<int:student_id>/', views.student_checkout_session, name='student_checkout_session'),
    path('webhook/', views.stripe_webhook),
]
