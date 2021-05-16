from django.db import models
from django.contrib.auth import get_user_model

from offers.models import Offer

User = get_user_model()


class Request(models.Model):
    """
    User who wants to borrow a book from offer must submit request to book owner.
    In about section he can provide additional information e.g. time of rent or
    any other information owner will choose his request over others.

    Owner may reject some requested due to some factor e.g. bad user rating.
    Upon acceptiong one offer all other shall be rejected.
    """

    class Status(models.TextChoices):
        PENDING = 'PD', 'Pending'
        REJECTED = 'RJ', 'Rejected'
        APPROVED = 'AP', 'Approved'
        FINISHED = 'FN', 'Finished'

    id = models.AutoField(primary_key=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    about = models.TextField(help_text='Addtional information requester may provide')
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    requester_phone = models.CharField(max_length=13)

    def __str__(self):
        return f'{self.offer}, requester {self.requester}'

    class Meta:
        # prevents user from spamming lender with requests
        unique_together = ('offer', 'requester')
