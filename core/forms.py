from django import forms
from django.utils import timezone
from core.models import Book, Genre, BookLibrary
from core.models import Reservation


class AddBookForm(forms.ModelForm):
    title = forms.CharField(max_length=30, label='Titre du livre')
    cover = forms.ImageField(label='Couverture du livre')
    #collection = forms.IntegerField(label='Nombre d\'exemplaires')
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), label='Genre du livre')

    class Meta:
        model = Book
        exclude = ['author', 'created_at']


class AddBookLibraryForm(forms.ModelForm):
    # book not in BookLibrary
    # my_bookLibrary = BookLibrary.objects.filter(library__user=self.request.user)


    book = forms.ModelChoiceField(queryset=Book.objects.all(), label='Titre du livre')
    collection = forms.IntegerField(label='Nombre d\'exemplaires')
    book_available = forms.BooleanField(label='Disponible', required=False)

    class Meta:
        model = BookLibrary
        exclude = ['library', 'created_at']

class UpdateBookLibraryForm(forms.ModelForm):
    collection = forms.IntegerField(label='Nombre d\'exemplaires')
    book_available = forms.BooleanField(label='Disponible', required=False)

    class Meta:
        model = BookLibrary
        exclude = ['library', 'book', 'created_at']

class BookReservationForm(forms.ModelForm):
    limit_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        help_text='La date de retour du livre est la date maximal pour rendre le livre. Si vous ne le faites pas, vous serez sanctionné.<br>La date ne peut pas être inférieur à 5 jours après la date du jour et ne peut pas être supérieur à 20 jours après la date du jour.',
        label='Date de retour du livre'
    )

    class Meta:
        model = Reservation
        fields = ['limit_date']

    def clean_limit_date(self):
        limit_date = self.cleaned_data.get('limit_date')
        if limit_date and limit_date < timezone.localdate() + timezone.timedelta(days=5):
            raise forms.ValidationError("La date ne peut pas être inférieur à 5 jours après la date du jour.")
        if limit_date and limit_date > timezone.localdate() + timezone.timedelta(days=20):
            raise forms.ValidationError("La date ne peut pas être supérieur à 20 jours après la date du jour")

        return limit_date
