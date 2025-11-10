from django . urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.welcome, name="welcome"),
    path ( "book/<int:book_id>", views.book , name="book"),
    path ( "bookBoard", views.bookBoard , name="bookBoard"),
    path ( "newBook", views.newBook , name="newBook"),
    path ( "delete_book/<int:book_id>", views.delete_book ,name = "delete_book"),
    path ( "edit_book/<int:book_id>", views.edit_book , name="edit_book"),
    path ( "ReviewForm/<int:book_id>", views.newReview , name="newReview"),
    path ( "delete_review/<int:book_id>/<int:review_id>", views.delete_review , name="delete_review"),
    path ( "edit_review/<int:book_id>/<int:review_id>", views.edit_review, name="edit_review"),
    path ( "Author_board", views.authorBoard , name="authorBoard"),
    path ( "AuthorForm", views.newAuthor , name="newAuthor"),
    path ( "delete_author/<int:author_id>", views.delete_author ,name = "delete_author"),
    path ( "edit_author/<int:author_id>", views.edit_author , name="edit_author"),
    path ( "author/<int:author_id>", views.author , name="author"),

    #auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    ]
