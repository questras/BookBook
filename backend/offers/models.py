from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Offer(models.Model):
    """
    Model of an offer created by a user who wants to borrow somebody a book.

    He may choose to provide an arbitrary text in the description field to provide
    possible lenders with additional information e.g. publisher or edition of the book.

    Lender's phone number should not be shared with just anyone who sees this offer.
    """

    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        LENT = 'LT', 'Lent'
        RETURNED = 'RT', 'Returned'

    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=100, help_text='Book title')
    author = models.CharField(max_length=200, help_text='Author name or comma separated list of authors\' names')
    description = models.TextField(help_text='Detailed description of the offer')

    city = models.CharField(max_length=50, help_text='General area of an exchange place')
    state = models.CharField(max_length=50, help_text='State of the city')

    status = models.CharField(max_length=4, choices=Status.choices, default=Status.ACTIVE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    lender = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Who offered to lend a book')
    lender_phone = models.CharField(max_length=13, help_text='Lender\'s contact information')

    def __str__(self) -> str:
        return f'{self.id}. ({self.title}, {self.author}) by {self.lender.get_full_name()}'


class OfferImage(models.Model):
    """
    Images of the book from an offer.
    Separate model to allow multiple images be assigned to a single offer.
    """
    id = models.AutoField(primary_key=True)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
