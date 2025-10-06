from django . urls import path
from . import views

urlpatterns = [path("about",views.about, name="about"),
               path("welcome",views.welcome, name="welcome"),
               path ( "book/<int:book_id>", views.book , name="book"),
               path ( "bookBoard", views.bookBoard , name="bookBoard"),
               path ( "newBook", views.newBook , name="newBook")
               ]
