from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

users = User.objects.all()
for user in users:
    token, created = Token.objects.get_or_create(user=user)
    print(user.username, token.key)
