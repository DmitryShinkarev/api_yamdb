from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api_titles.models import Title
from api_users.models import User


class Review(models.Model):
    score = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name=_('Vote'))
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='title_vote', verbose_name=_('User'))
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='votes', verbose_name=_('Title'))
    pub_date = models.DateTimeField(auto_now=True, verbose_name=_('date vote'))
    text = models.TextField(verbose_name=_('Text'))

    def __str__(self):
        return self.title.name