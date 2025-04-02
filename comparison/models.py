from django.db import models

class Economic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class AbstractAnswer(models.Model):

    ANSWER_CHOICES = [
        ('agree', 'Stimme zu'),
        ('neutral', 'Neutral'),
        ('disagree', 'Stimme nicht zu'),
    ]

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Answer(AbstractAnswer):
    economic = models.ForeignKey(Economic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'economic')

    def __str__(self):
        return f"{self.economic.name} - {self.get_answer_display()}"


class UserAnswer(AbstractAnswer):

    session_uuid = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_answer_display()}"
