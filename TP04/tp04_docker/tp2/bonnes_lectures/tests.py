from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from bonnes_lectures.models import Author, Book, Review
from datetime import datetime


class AuthorModelTests(TestCase):
    """Tests pour le modèle Author"""
    
    def test_author_creation(self):
        """Test de création d'un auteur"""
        author = Author.objects.create(prenom="Victor", nom="Hugo")
        self.assertEqual(author.prenom, "Victor")
        self.assertEqual(author.nom, "Hugo")
    
    def test_author_str(self):
        """Test de la représentation string d'un auteur"""
        author = Author.objects.create(prenom="Victor", nom="Hugo")
        self.assertEqual(str(author), "Victor Hugo")
    
    def test_author_has_books_relation(self):
        """Test de la relation auteur-livres"""
        author = Author.objects.create(prenom="Victor", nom="Hugo")
        book = Book.objects.create(
            title="Les Misérables",
            author=author,
            publisher="Pocket",
            year=1862,
            ISBN=9782266123456,
            backCover="Un chef-d'œuvre",
            cover=True
        )
        self.assertEqual(author.livres.count(), 1)
        self.assertEqual(author.livres.first(), book)


class BookModelTests(TestCase):
    """Tests pour le modèle Book"""
    
    def setUp(self):
        """Création d'un auteur pour les tests"""
        self.author = Author.objects.create(prenom="Albert", nom="Camus")
    
    def test_book_creation(self):
        """Test de création d'un livre"""
        book = Book.objects.create(
            title="L'Étranger",
            author=self.author,
            publisher="Gallimard",
            year=1942,
            ISBN=9782070360024,
            backCover="Un classique de la littérature",
            cover=True
        )
        self.assertEqual(book.title, "L'Étranger")
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.year, 1942)
    
    def test_book_str(self):
        """Test de la représentation string d'un livre"""
        book = Book.objects.create(
            title="La Peste",
            author=self.author,
            publisher="Gallimard",
            year=1947,
            ISBN=9782070360031,
            backCover="Roman sur une épidémie",
            cover=False
        )
        self.assertEqual(str(book), "La Peste")
    
    def test_book_without_author(self):
        """Test de création d'un livre sans auteur (null=True)"""
        book = Book.objects.create(
            title="Livre anonyme",
            author=None,
            publisher="Inconnu",
            year=2000,
            ISBN=1234567890123,
            backCover="Texte de couverture",
            cover=False
        )
        self.assertIsNone(book.author)
    
    def test_book_has_reviews_relation(self):
        """Test de la relation livre-critiques"""
        book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publisher="Test Publisher",
            year=2024,
            ISBN=9781234567890,
            backCover="Test",
            cover=True
        )
        review = Review.objects.create(
            book=book,
            text="Excellent livre!",
            review=5
        )
        self.assertEqual(book.reviews.count(), 1)
        self.assertEqual(book.reviews.first(), review)


class ReviewModelTests(TestCase):
    """Tests pour le modèle Review"""
    
    def setUp(self):
        """Création des données de test"""
        self.author = Author.objects.create(prenom="Test", nom="Author")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publisher="Test",
            year=2024,
            ISBN=1234567890,
            backCover="Test",
            cover=True
        )
    
    def test_review_creation(self):
        """Test de création d'une critique"""
        review = Review.objects.create(
            book=self.book,
            text="Très bon livre",
            review=4
        )
        self.assertEqual(review.text, "Très bon livre")
        self.assertEqual(review.review, 4)
        self.assertEqual(review.book, self.book)
    
    def test_review_date_auto_now(self):
        """Test que la date est automatiquement ajoutée"""
        review = Review.objects.create(
            book=self.book,
            text="Test",
            review=3
        )
        self.assertIsNotNone(review.date)
        self.assertEqual(review.date, datetime.now().date())
    
    def test_review_min_validator(self):
        """Test du validateur minimum (1)"""
        from django.core.exceptions import ValidationError
        review = Review(
            book=self.book,
            text="Mauvais",
            review=0
        )
        with self.assertRaises(ValidationError):
            review.full_clean()
    
    def test_review_max_validator(self):
        """Test du validateur maximum (5)"""
        from django.core.exceptions import ValidationError
        review = Review(
            book=self.book,
            text="Trop bon",
            review=6
        )
        with self.assertRaises(ValidationError):
            review.full_clean()
    
    def test_review_valid_range(self):
        """Test que les valeurs de 1 à 5 sont valides"""
        for i in range(1, 6):
            review = Review.objects.create(
                book=self.book,
                text=f"Test {i}",
                review=i
            )
            review.full_clean()  # Ne devrait pas lever d'exception
            self.assertEqual(review.review, i)


class ViewTests(TestCase):
    """Tests pour les vues"""
    
    def setUp(self):
        """Configuration initiale pour les tests de vues"""
        self.client = Client()
        self.author = Author.objects.create(prenom="Jane", nom="Austen")
        self.book = Book.objects.create(
            title="Pride and Prejudice",
            author=self.author,
            publisher="Penguin",
            year=1813,
            ISBN=9780141439518,
            backCover="A classic romance",
            cover=True
        )
    
    def test_welcome_view(self):
        """Test de la vue d'accueil"""
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonnes_lectures/welcome.html')
    
    def test_book_board_view(self):
        """Test de la vue tableau des livres"""
        response = self.client.get(reverse('bookBoard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonnes_lectures/Book_board.html')
        self.assertContains(response, "Pride and Prejudice")
    
    def test_book_detail_view(self):
        """Test de la vue détail d'un livre"""
        response = self.client.get(reverse('book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonnes_lectures/book.html')
        self.assertContains(response, "Pride and Prejudice")
    
    def test_book_detail_view_invalid_id(self):
        """Test avec un ID de livre invalide"""
        # La vue book utilise get() au lieu de get_object_or_404
        # Elle lève une exception DoesNotExist au lieu de retourner 404
        from bonnes_lectures.models import Book
        with self.assertRaises(Book.DoesNotExist):
            response = self.client.get(reverse('book', args=[9999]))
    
    def test_author_board_view(self):
        """Test de la vue tableau des auteurs"""
        response = self.client.get(reverse('authorBoard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonnes_lectures/Author_board.html')
        # Le template affiche prénom et nom séparément dans des colonnes
        self.assertContains(response, "Jane")
        self.assertContains(response, "Austen")
    
    def test_author_detail_view(self):
        """Test de la vue détail d'un auteur"""
        response = self.client.get(reverse('author', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonnes_lectures/author.html')
        # Le template affiche le prénom et nom séparément
        self.assertContains(response, "Jane")
        self.assertContains(response, "Austen")
    
    def test_new_book_get(self):
        """Test GET de la vue nouveau livre"""
        response = self.client.get(reverse('newBook'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonnes_lectures/BookForm.html')
        self.assertContains(response, "Ajouter")
    
    def test_new_book_post_valid(self):
        """Test POST valide pour créer un livre"""
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'publisher': 'New Publisher',
            'year': 2024,
            'ISBN': 9781234567890,
            'backCover': 'A new book',
            'cover': True
        }
        response = self.client.post(reverse('newBook'), data)
        self.assertEqual(Book.objects.count(), 2)
        new_book = Book.objects.get(title='New Book')
        self.assertRedirects(response, f'/book/{new_book.id}')
    
    def test_new_author_get(self):
        """Test GET de la vue nouvel auteur"""
        response = self.client.get(reverse('newAuthor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonnes_lectures/AuthorForm.html')
    
    def test_new_author_post_valid(self):
        """Test POST valide pour créer un auteur"""
        data = {
            'prenom': 'Charles',
            'nom': 'Dickens'
        }
        response = self.client.post(reverse('newAuthor'), data)
        self.assertEqual(Author.objects.count(), 2)
        new_author = Author.objects.get(nom='Dickens')
        self.assertRedirects(response, f'/author/{new_author.id}')
    
    def test_delete_book_post(self):
        """Test de suppression d'un livre"""
        book_id = self.book.id
        response = self.client.post(reverse('delete_book', args=[book_id]))
        self.assertRedirects(response, reverse('bookBoard'))
        self.assertEqual(Book.objects.filter(id=book_id).count(), 0)
    
    def test_delete_author_post(self):
        """Test de suppression d'un auteur"""
        # Créer un auteur sans livres
        author = Author.objects.create(prenom="Test", nom="Delete")
        author_id = author.id
        response = self.client.post(reverse('delete_author', args=[author_id]))
        self.assertRedirects(response, reverse('authorBoard'))
        self.assertEqual(Author.objects.filter(id=author_id).count(), 0)
    
    def test_edit_book_get(self):
        """Test GET de modification d'un livre"""
        response = self.client.get(reverse('edit_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modifier")
        self.assertContains(response, "Pride and Prejudice")
    
    def test_edit_book_post(self):
        """Test POST de modification d'un livre"""
        data = {
            'title': 'Pride and Prejudice (Updated)',
            'author': self.author.id,
            'publisher': 'Penguin Classics',
            'year': 1813,
            'ISBN': 9780141439518,
            'backCover': 'Updated description',
            'cover': True
        }
        response = self.client.post(reverse('edit_book', args=[self.book.id]), data)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Pride and Prejudice (Updated)')
        self.assertRedirects(response, reverse('book', args=[self.book.id]))
    
    def test_new_review_post_valid(self):
        """Test de création d'une critique"""
        data = {
            'text': 'Excellent livre!',
            'review': 5
        }
        response = self.client.post(reverse('newReview', args=[self.book.id]), data)
        self.assertEqual(Review.objects.count(), 1)
        self.assertRedirects(response, f'/book/{self.book.id}')
    
    def test_delete_review_post(self):
        """Test de suppression d'une critique"""
        review = Review.objects.create(
            book=self.book,
            text="Test review",
            review=3
        )
        response = self.client.post(reverse('delete_review', args=[self.book.id, review.id]))
        self.assertEqual(Review.objects.count(), 0)
        self.assertRedirects(response, reverse('book', args=[self.book.id]))


class FormTests(TestCase):
    """Tests pour les formulaires"""
    
    def setUp(self):
        self.author = Author.objects.create(prenom="Test", nom="Author")
    
    def test_book_form_valid(self):
        """Test d'un formulaire de livre valide"""
        from bonnes_lectures.forms import BookForm
        data = {
            'title': 'Test Book',
            'author': self.author.id,
            'publisher': 'Test Publisher',
            'year': 2024,
            'ISBN': 9781234567890,
            'backCover': 'Test description',
            'cover': True
        }
        form = BookForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_book_form_missing_title(self):
        """Test d'un formulaire de livre sans titre"""
        from bonnes_lectures.forms import BookForm
        data = {
            'author': self.author.id,
            'publisher': 'Test',
            'year': 2024,
            'ISBN': 1234567890,
            'backCover': 'Test',
            'cover': True
        }
        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_review_form_valid(self):
        """Test d'un formulaire de critique valide"""
        from bonnes_lectures.forms import ReviewForm
        data = {
            'text': 'Excellent livre!',
            'review': 5
        }
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_review_form_invalid_rating(self):
        """Test d'un formulaire de critique avec note invalide"""
        from bonnes_lectures.forms import ReviewForm
        data = {
            'text': 'Test',
            'review': 6
        }
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_author_form_valid(self):
        """Test d'un formulaire d'auteur valide"""
        from bonnes_lectures.forms import AuthorForm
        data = {
            'prenom': 'Victor',
            'nom': 'Hugo'
        }
        form = AuthorForm(data=data)
        self.assertTrue(form.is_valid())