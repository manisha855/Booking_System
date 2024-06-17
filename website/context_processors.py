# yourapp/context_processors.py

def dynamic_title(request):
    user_role = None
    if request.user.is_authenticated:
        user_role = request.user.role  # Assuming role is stored in the user model
    
    title = "Dashboard"  # Default title if user_role is not set or recognized
    if user_role == "Partner":
        title = "Partner Portal"
    elif user_role == "admin":
        title = "Admin Portal"
    elif user_role == "individual":
        title = "Student Portal"
    
    return {
        'user_role': user_role,
        'dynamic_title': title,
    }
