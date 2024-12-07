from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="tags")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.quote}"

    def show_tags(self):
        tag = self.tags.all()
        return tag

    def show_quote_author(self):
        return self.author
