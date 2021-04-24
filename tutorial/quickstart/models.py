from django.db import models


class Tweet(models.Model):
    text = models.TextField(max_length=560)
    photo = models.URLField(max_length=4096, blank=True, help_text='image URL')
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.author.username}: {self.text}'


class Follow(models.Model):
    follower = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='follows')  # кто подписался на follows
    follows = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='followers')  # на кого подписался
    followed = models.DateTimeField(auto_now_add=True)  # когда подписался

    def __str__(self):
        return f'{self.follower.username} -> {self.follows.username}'
