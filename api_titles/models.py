from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def __str__(self):
        return str(self.name)


class Title(models.Model):
    name = models.CharField(blank=False, null=False, max_length=200)
    year = models.IntegerField()
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='genre', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category', blank=True, null=True)

    def __str__(self):
        return str(self.name)
