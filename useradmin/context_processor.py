from core.models import Category, Vendor, Product

def default(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors,
    }

    return context
    