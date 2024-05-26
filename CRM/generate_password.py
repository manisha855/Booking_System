from django.contrib.auth.hashers import make_password

password = make_password('admin@123')
print(password)
