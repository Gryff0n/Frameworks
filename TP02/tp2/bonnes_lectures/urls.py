from django . urls import path
from . import views

urlpatterns = [path("about",views.about, name="about"),
               path("welcome",views.welcome, name="welcome"),
               path ( "books/<int:book_id>", views.books , name="books"),
               path ( "bookBoard", views.bookBoard , name="book")
               ]
