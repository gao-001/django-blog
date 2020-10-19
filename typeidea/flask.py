import json
import requests
from requests.auth import HTTPBasicAuth
from blog.models import Post
from blog.models import Category
from django.contrib.auth.models import User

res = requests.get('http://www.gaocode.top:8060/api/v1/posts?page=2')
text = res.text
data = json.loads(text)
posts = data['posts']
cate = Category.objects.first()
user = User.objects.first()


for p in posts:
    Post.objects.create(title=p['topic'],content=p['body'],category=cate,owner=user)




