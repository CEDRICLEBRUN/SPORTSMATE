from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    SPORTS_CHOICES = [
        ('Football', 'Football'),
        ('Basketball', 'Basketball'),
        ('Tennis', 'Tennis'),
        ('Rugby', 'Rugby'),
    ]

    sport = models.CharField(max_length=100, choices=SPORTS_CHOICES)
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    city = models.CharField(max_length=100)
    participants_number = models.IntegerField()
    available_places = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='events_joined')
    price = models.IntegerField()

    def __str__(self):
        return(f'{self.name} - {self.date} {self.time} ({self.sport})')


    def still_available(self):
        """Function checking if there is still available place for an event."""
        if self.available_places > 0:
            return True
        
        return False

    def new_participant(self, user):
        """Function taking a place for one user."""
        self.participants.add(user)
        self.available_places -= 1

class Conversation(models.Model):
    participant1 = models.ForeignKey(User, related_name='conversations_as_participant1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(User, related_name='conversations_as_participant2', on_delete=models.CASCADE)

    def __str__(self):
        return f"Conversation between {self.participant1.username} and {self.participant2.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation}"
