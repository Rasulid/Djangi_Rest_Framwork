from django.db import models
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])





class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default="python")
    style = models.CharField(max_length=100, choices=STYLE_CHOICES, default="friendly")
    owner = models.ForeignKey("auth.User", related_name="snippets", on_delete=models.CASCADE)
    hightlateg = models.TextField()

    class Meta:
        ordering = ["created"]
        
    def save(self, hightlate=None, *args, **kwargs):
        lexar = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos  else False
        options = {'table': self.title} if self.title else {}
        formater = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options)
        self.hightlateg = hightlate(self.code, lexar, formater)
        super(Snippet, self).save(*args, **kwargs)        

    def __str__(self):
        return self.title
