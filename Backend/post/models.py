from django.db import models

class UserProfile(models.Model):
    nickname = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profile_images/')

    def __str__(self):
        return self.nickname

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    expect_number = models.PositiveIntegerField(default=0)  # 기본값 0
    real_number = models.PositiveIntegerField(default=0)  # 기본값 0
    star = models.BooleanField(default=False)
    star_number = models.PositiveIntegerField(default=0)

    # ForeignKey 연결
  #  nickname = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
  #  profile_image = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.pk}] {self.title}'
    
    def get_absolute_url(self):
        return f'/post/{self.pk}'
