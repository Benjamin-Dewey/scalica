from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.forms import ModelForm, TextInput

class Post(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  text = models.CharField(max_length=256, default="")
  pub_date = models.DateTimeField('date_posted')
  def __str__(self):
    if len(self.text) < 16:
      desc = self.text
    else:
      desc = self.text[0:16]
    return self.user.username + ':' + desc

class Following(models.Model):
  id = models.IntegerField(primary_key=True)

  follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_follows")
  followee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_followed")
  follow_date = models.DateTimeField('follow data')
  def __str__(self):
    return self.follower.username + "->" + self.followee.username

class ReverseFollowing(models.Model):
  id = models.IntegerField(primary_key=True)

  follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="reverse_user_follows")
  followee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="reverse_user_followed")
  follow_date = models.DateTimeField('reverse follow data')
  def __str__(self):
    return self.followee.username + "->" + self.follower.username

# Model Forms
class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ('text',)
    widgets = {
      'text': TextInput(attrs={'id' : 'input_post'}),
    }

class FollowingForm(ModelForm):
  class Meta:
    model = Following
    fields = ('followee',)

  def __init__(self, *args, **kwargs):
    pk_list = kwargs.pop('pk_list', None)
    super(FollowingForm, self).__init__(*args, **kwargs)
    if pk_list:
      self.fields['followee'].queryset = User.objects.filter(pk__in=pk_list)

class MyUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    help_texts = {
      'username' : '',
    }
