from django import template
from website.models import CustomUser

register = template.Library()

#show the title dynamic for admin,student & partner portal
def dynamic_title(request):
    user_role = None
    if request.user.is_authenticated:
        user_role = request.user.role  
    
    title = "Dashboard"  
    if user_role == "partner":
        title = "Partner Portal"
    elif user_role == "admin":
        title = "Admin Portal"
    elif user_role == "student":
        title = "Student Portal"
    
    return {
        'user_role': user_role,
        'dynamic_title': title,
    }

#filter the user by role for admin vi
# @register.filter
# def get_role_display(value):
#     return dict(CustomUser.ROLE_CHOICES).get(value, value)