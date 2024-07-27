from core.models import Category, Vendor, Product
from userauths.models import UserProfile

def default(request):

    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None
            
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors,
        'profile': user_profile
    }

    return context
    