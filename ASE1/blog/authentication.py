from django.contrib.auth.models import User
class EmailAuthbackend(object):
    def authenticate(self, username=None, password=None):
        print('Here 1')
        try:
            user = User.objects.get(email=username)
            print(user)
            if user.check_password(password):
                print('Here 2')
                return user
            return None
        except User.DoesNotExist:
            print('Here 3')
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None