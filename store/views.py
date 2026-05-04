from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, UserInteraction
from .recommender import get_recommendations

CATEGORIES = ['Mobiles', 'Laptops', 'Accessories', 'Electronics', 'Fashion', 'Home & Appliances']

def landing(request):
    top_products = Product.objects.order_by('?')[:8]
    recommended = []
    
    if request.user.is_authenticated:
        ids = get_recommendations(request.user.id)
        recommended = Product.objects.filter(id__in=ids)
    
    # Specific top sellers for the landing page (iPhone 13, Sony XM4)
    top_sellers = Product.objects.filter(id__in=[2, 16])
        
    return render(request, 'landing.html', {
        'top_products': top_products,
        'recommended': recommended,
        'top_sellers': top_sellers
    })

def home(request):
    products = Product.objects.all()
    recommended = []

    if request.user.is_authenticated:
        ids = get_recommendations(request.user.id)
        recommended = Product.objects.filter(id__in=ids)

    return render(request, 'home.html', {
        'products': products,
        'recommended': recommended,
        'categories': CATEGORIES
    })
def category_view(request, category_name):
    # Fetch products for the specific category (case-insensitive)
    products = Product.objects.filter(category__iexact=category_name)
    recommended = []

    if request.user.is_authenticated:
        ids = get_recommendations(request.user.id)
        recommended = Product.objects.filter(id__in=ids)

    return render(request, 'home.html', {
        'products': products,
        'recommended': recommended,
        'category_name': category_name,
        'categories': CATEGORIES
    })

def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(category__icontains=query)
    
    recommended = []
    if request.user.is_authenticated:
        ids = get_recommendations(request.user.id)
        recommended = Product.objects.filter(id__in=ids)

    return render(request, 'home.html', {
        'products': products,
        'recommended': recommended,
        'search_query': query,
        'categories': CATEGORIES
    })

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def interact_product(request, product_id):
    product = Product.objects.get(id=product_id)
    interaction, created = UserInteraction.objects.get_or_create(
        user=request.user, 
        product=product,
        defaults={'rating': 1}
    )
    if not created and interaction.rating < 5:
        interaction.rating += 1
        interaction.save()
    
    return redirect('home')

@login_required
def view_cart(request):
    from .models import Cart, CartItem
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    return render(request, 'cart.html', {'cart': cart, 'total': total})

@login_required
def add_to_cart(request, product_id):
    from .models import Product, Cart, CartItem
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('view_cart')
def info_view(request, page_slug):
    pages = {
        'about': {
            'title': 'About Sj_Store',
            'content': '<p>Welcome to Sj_Store, where premium technology meets elegant design. Founded in 2024, our mission is to curate the finest electronics and heritage apparel for the modern connoisseur.</p><p>We believe that every product should tell a story of quality and innovation. From our global logistics network to our AI-driven recommendation engine, every detail is crafted to provide you with a seamless shopping experience.</p>'
        },
        'careers': {
            'title': 'Join the Team',
            'content': '<p>We are always looking for visionary engineers, creative designers, and passionate curators to help us redefine e-commerce.</p><p>At Sj_Store, you\'ll work at the intersection of high-fashion and cutting-edge technology. Check back often for new openings in Bengaluru and beyond.</p>'
        },
        'news': {
            'title': 'Sj_Store Newsroom',
            'content': '<p>Stay updated with the latest from Sj_Store. We recently celebrated reaching 10,000 active premium members and launched our new Spring heritage collection.</p><p>Read about our commitment to carbon-neutral shipping and our recent awards in digital design excellence.</p>'
        },
        'contact': {
            'title': 'Contact Center',
            'content': '<p>Our dedicated support specialists are available 24/7 to assist with your inquiries. Whether you need help with a premium order or have a question about our curated catalog, we are here for you.</p><p><strong>Email:</strong> support@sj-store.com<br><strong>Location:</strong> Premium Park, HSR Layout, Bengaluru</p>'
        },
        'returns': {
            'title': 'Returns & Exchanges',
            'content': '<p>We offer a hassle-free 30-day return policy for all unused and pristine items in their original packaging.</p><p>Simply log into your account, select your order, and initiate a return request. Our courier partners will handle the rest with white-glove service.</p>'
        },
        'warranty': {
            'title': 'Warranty Information',
            'content': '<p>Every product sold on Sj_Store comes with our unique "Sj-Gold" warranty, covering all manufacturing defects for up to 2 years.</p><p>For select electronics, we also offer extended protection plans to ensure your premium gear stays in perfect condition.</p>'
        },
        'privacy': {
            'title': 'Privacy Policy',
            'content': '<p>Your data is handled with the highest level of security. We use end-to-end encryption for all transactions and never sell your personal information to third parties.</p><p>We collect only the essential data needed to provide our premium services and personalized recommendations.</p>'
        },
        'terms': {
            'title': 'Terms of Service',
            'content': '<p>By using Sj_Store, you agree to our terms of conduct and service. We maintain a high standard of platform integrity and expect our community to do the same.</p><p>All digital assets and designs on this platform are protected under intellectual property law.</p>'
        }
    }
    
    page = pages.get(page_slug, {'title': 'Page Not Found', 'content': '<p>The page you are looking for does not exist.</p>'})
    return render(request, 'info.html', page)

@login_required
def remove_from_cart(request, item_id):
    from .models import CartItem
    from django.shortcuts import get_object_or_404
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        
    return redirect('view_cart')