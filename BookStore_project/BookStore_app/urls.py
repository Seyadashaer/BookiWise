from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('cart', views.cart),
    path('checkout/', views.checkout),
    path('login_page', views.login_page),
    path('my_account', views.my_account), 
    path('book_detail/<int:book_id>', views.book_detail),
    path('categories', views.categories), 
    path('wishlist', views.wishlist), 
    path('contact', views.contact),
    path('register_page', views.register_page),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('home', views.home),
    path('admin_page',views.admin_page ),
    path('add_category', views.add_category),
    path('add_author', views.add_author),
    path('add_book', views.add_book),
    path('add_to_cart/<int:book_id>', views.add_to_cart),
    path('add_to_wishlist/<int:book_id>', views.add_to_wishlist),
    path('create_order', views.create_order),
    path('order_success', views.order_success),
    path('category_view/<str:category_name>', views.category_view),
    path('write_review/<int:book_id>', views.write_review),
    path('search', views.search),
    path('remove_from_cart/<int:book_id>', views.remove_from_cart),
    path('remove_from_wishlist/<int:book_id>', views.remove_from_wishlist),
    path('delete_order/<int:order_id>', views.delete_order),
    path('delete_book/<int:book_id>', views.delete_book),
    path('add_admin/', views.add_admin),
    path('add_as_admin/<int:user_id>', views.add_as_admin),
    path('remove_as_admin/<int:user_id>', views.remove_as_admin),
    path('send_message', views.send_message),
    path('view_messages', views.view_messages),
    path('edit_book/<int:book_id>', views.edit_book),
    path('delete_message/<int:message_id>', views.delete_message)












]
