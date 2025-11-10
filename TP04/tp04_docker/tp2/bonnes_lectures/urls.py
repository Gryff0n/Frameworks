from django . urls import path
from . import views

urlpatterns = [path("about",views.about, name="about"),
               path("welcome",views.welcome, name="welcome"),
               path ( "book/<int:book_id>", views.book , name="book"),
               path ( "bookBoard", views.bookBoard , name="bookBoard"),
               path ( "newBook", views.newBook , name="newBook"),
               path ( "delete_book/<int:book_id>", views.delete_book ,name = "delete_book"),
               path ( "edit_book/<int:book_id>", views.edit_book , name="edit_book"),
               path ( "ReviewForm/<int:book_id>", views.newReview , name="newReview"),
               path ( "delete_review/<int:book_id>/<int:review_id>", views.delete_review , name="delete_review"),
               path("edit_review/<int:book_id>/<int:review_id>", views.edit_review, name="edit_review"),

               ]
