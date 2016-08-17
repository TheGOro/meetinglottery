from __future__ import unicode_literals

from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=30,
                            unique=True)

    def __str__(self):
        return self.name


class Participation(models.Model):
    ALONE    = 'A'
    TOGETHER = 'T'
    VACATION = 'V'
    CLASSIFICATION_CHOICES = (
        (ALONE, 'Alone'),
        (TOGETHER, 'Together'),
        (VACATION, 'Vacation')
    )
    candidate = models.ForeignKey(Candidate)
    classification = models.CharField(max_length=2,
                                     choices=CLASSIFICATION_CHOICES,
                                     default=ALONE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.date.strftime('%Y. %m. %d. %H:%M') + ' - ' + self.candidate.name +
                ' (' + self.classification + ')')
