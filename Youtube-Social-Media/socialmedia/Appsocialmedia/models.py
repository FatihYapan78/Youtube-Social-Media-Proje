from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Profil-İmage")
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class Post(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="Post-İmage")
    description = models.TextField()
    likes = models.ManyToManyField(Profil, related_name="Beğenenler", blank=True)
    post_save = models.ManyToManyField(Profil, related_name="Kaydedenler", blank=True)
    comment_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profil.user.username

class Comment(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profil.user.username

class Takip(models.Model):
    profil = models.ForeignKey(Profil,related_name="takipci_profil", on_delete=models.CASCADE) # benim profilim
    takip_edilen = models.ForeignKey(Profil,related_name="takip_edilen", on_delete=models.CASCADE) # faruk

    def __str__(self):
        return self.profil.user.username

class Takipci(models.Model):
    profil = models.ForeignKey(Profil,related_name="takip_profil", on_delete=models.CASCADE) # benim profilim
    takip_eden = models.ForeignKey(Profil, related_name="takip_eden", on_delete=models.CASCADE) # faruk

    def __str__(self):
        return self.profil.user.username