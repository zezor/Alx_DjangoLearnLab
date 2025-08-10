# api/serializers.py
from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model fields: id, title, publication_year, author.
    Also includes custom validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        # include author as a PK by default; we include all fields here.
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Field-level validation for publication_year.
        Ensures year is not greater than the current calendar year.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year ({value}) cannot be in the future (current year: {current_year})."
            )
        return value


class NestedBookSerializer(serializers.ModelSerializer):
    """
    A small helper serializer used for nested display inside Author.
    This is the same as BookSerializer but made read-only for nested contexts
    to avoid accidental creation through Author endpoints.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author model.
    - name: author name.
    - books: nested list of related Book objects using NestedBookSerializer.
    """
    books = NestedBookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        # We include books as a read-only nested field to show related books
        # when retrieving an Author instance.