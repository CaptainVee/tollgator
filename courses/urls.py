from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostDetailView, PaymentView
from .views import  add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView, LessonCreateView, LessonDetailView


urlpatterns = [
path('', PostListView.as_view(), name='courses-home'),
path('user/<int:pk>/', UserPostDetailView.as_view(), name='user-post'),
path('post/new/', PostCreateView.as_view(), name='post-create'),
path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), #product view
path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
path('about/', views.about, name='courses-about'), 


# path('course/<int:pk>/', CourseDetailView.as_view(), name='detail'),
path('lesson/<int:course_pk>/new/', LessonCreateView.as_view(), name='lesson-create'),
path('lesson/<int:course_pk>/<int:lesson_pk>',LessonDetailView.as_view(), name='lesson-detail'),
path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
path('remove-item-from-cart/<int:pk>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
path('payment/', PaymentView, name='payment'),
]
