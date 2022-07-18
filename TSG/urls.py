from django.urls import path
from TSG import views

urlpatterns = [
    path('tsg/', views.tsg, name='tsg_list'),
    path('tsg/<int:pk>', views.tsg_detail, name='tsg'),
    path('tsg/<int:tsg_pk>/manage', views.manage, name='tsg_manage'),
    path('tsg/<int:tsg_pk>/create_notification', views.create_notification, name='create_notification'),
    path('tsg/<int:tsg_pk>/create_announcement', views.create_announcement, name='create_announcement'),
    path('tsg/<int:tsg_pk>/announcement', views.announcement_list, name='announcement_list'),
    path('tsg/<int:tsg_pk>/announcement/<int:announcement_pk>', views.announcement_detail, name='announcement_detail'),
    path('tsg/<int:tsg_pk>/announcement/<int:announcement_pk>/delete', views.announcement_delete,
         name='announcement_delete'),
    path('tsg/<int:tsg_pk>/notification', views.notification_tsg_list, name='notification_tsg_list'),
    path('flat/<int:flat_pk>/notification', views.notification_flat_list, name='notification_flat_list'),
    path('tsg/<int:tsg_pk>/notification/<int:notification_pk>', views.notification_detail,
         name='notification_tsg_detail'),
    path('flat/<int:flat_pk>/notification/<int:notification_pk>', views.notification_detail,
         name='notification_flat_detail'),
    path('tsg/<int:tsg_pk>/notification/<int:notification_pk>/delete', views.notification_delete,
         name='notification_delete'),
    path('tsg/<int:tsg_pk>/flat', views.flat_list, name='flat_list'),
    # path('<int:tsg_pk>/<int:flat_pk>/manage', views.manage, name='flat_manage'),
]
