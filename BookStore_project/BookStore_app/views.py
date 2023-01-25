from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User , Book, Review, Author, Category, Order, OrderItem, Cart, Wishlist, Message
from . import models


# This function to display the main page of the website
def index(request):

    context = { 
        'books' : Book.objects.all(),
        'recent_books' : Book.objects.order_by('-created_at')[:10],
        'featured_books' : Book.objects.order_by('-total_rating')[:10],
        'categories' : Category.objects.all(),

    }
    
    return render(request, 'index.html', context)

# This function check if any user logged in 
def check_user_logged_in(request):
    if not request.session.get('id'):
        return redirect('/')
    try:
        user = User.objects.get(id=request.session['id'])
    except (User.DoesNotExist, KeyError) :
        return redirect('/')

# This function to display the home page of the website after the user has logged in
def home(request): 
    check_user_logged_in(request)
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/')

    context = {
        'books' : Book.objects.all(),
        'recent_books' : Book.objects.order_by('-created_at')[:10],
        'featured_books' : Book.objects.order_by('-total_rating')[:10],
        'user': user,
        'categories' : Category.objects.all()
    }
    return render(request, 'home.html', context)

# This function renders the register page
def register_page(request):
        return render(request, 'register.html')

# This function renders the login page
def login_page(request): 
    return render(request, 'login.html')

# This function validates the login and logs the user in
def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/home')

# This function validates the registration information and creates a new user
def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_page')
    else:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/home')

# This function clears the session data and redirects the user to the main page
def logout(request):
    request.session.clear()
    return redirect('/')

# This function is used to add a new book in admin page
def add_book(request):
    if request.method == 'POST':
        author = Author.objects.get(id=request.POST['author'])
        category = Category.objects.get(id=request.POST['category'])
        title = request.POST['title']
        price = request.POST['price']
        bookpage = request.FILES['bookpage']
        description = request.POST['description']
        Book.objects.create(
            author=author,
            category=category,
            title=title,
            price=price,
            bookpage=bookpage,
            description=description
        )
        return redirect('/admin_page')
    return redirect('/admin_page')

# This function is used to add a new category in admin page
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect('/admin_page')
    return redirect('/admin_page')

# This function is used to add a new author in admin page
def add_author(request):
    if request.method == 'POST':
        name = request.POST['name']
        Author.objects.create(name=name)
        return redirect('/admin_page')
    return redirect('/admin_page')

# This function is used to display the user's cart which contains all the books added by the user
def cart(request):
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/login_page')

    user = User.objects.get(id=request.session['id'])
    cart_items = Cart.objects.filter(user=user)
    total_price = 0
    for item in cart_items:
        total_price += item.book_total()
    
    context = {
        'books_in_cart': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

# This function is used to add a book to the user's cart
def add_to_cart(request, book_id):
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/login_page')
    # Get the user and book
    user = User.objects.get(id=request.session['id'])
    book = Book.objects.get(id=book_id)
    # Check if the book is already in the user's cart
    cart_item = Cart.objects.filter(user=user, book=book).first()
    if cart_item:
        # Update the quantity of the existing cart item
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Create a new cart item
        cart_item = Cart.objects.create(user=user, book=book, quantity=1)
    return redirect('/cart')

# This function is used to remove a book from the user's cart. It gets the user and book by their ID, and then finds the corresponding cart item and deletes it.
def remove_from_cart(request, book_id):
    user = User.objects.get(id=request.session['id'])
    book = Book.objects.get(id=book_id)
    cart = Cart.objects.filter(user=user, book=book).first()
    if cart:
        cart.delete()
    return redirect('/cart')

# This function is used to display the items in the user's wishlist.
def wishlist(request):
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/login_page')
    user = User.objects.get(id=request.session['id'])
    wishlist_items = Wishlist.objects.filter(user=user)

    
    context = {
        'books_in_wishlist': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

# This function is used to add a book to the user's wishlist. 
def add_to_wishlist(request, book_id):
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/login_page')
    # Get the user and book
    user = User.objects.get(id=request.session['id'])
    book = Book.objects.get(id=book_id)
    # Check if the book is already in the user's wishlist
    wishlist_item = Wishlist.objects.filter(user=user, book=book).first()
    if wishlist_item:
        # Update the quantity of the existing wishlist item
        wishlist_item.quantity += 1
        wishlist_item.save()
    else:
        # Create a new wishlist item
        wishlist_item = Wishlist.objects.create(user=user, book=book, quantity=1)
    return redirect('/wishlist')

# This function is used to remove a book from the user's wishlist. It gets the user and book by their ID, and then finds the corresponding wishlist item and deletes it
def remove_from_wishlist(request, book_id):
    user = User.objects.get(id=request.session['id'])
    book = Book.objects.get(id=book_id)
    wishlist = Wishlist.objects.filter(user=user, book=book).first()
    if wishlist:
        wishlist.delete()
    return redirect('/wishlist')

# This function is used to display the checkout page for the user
def checkout(request): 
    user = User.objects.get(id=request.session['id'])
    cart_items = Cart.objects.filter(user=user)
    total_price = 0
    for item in cart_items:
        total_price += item.book.price * item.quantity
    context = {
        'books_in_cart': cart_items,
        'total_price': total_price
    }
    return render(request, 'checkout.html', context)

# This function is used to show the contact page where the user can contact the bookstore
def contact(request): 
    return render(request, 'contact.html')

# This function is used to handle the order creation process by adding the customer information and the cart items to the order table
def create_order(request):
    user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        customer = user
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(customer=customer, name=name, email=email, phone=phone, address=address, country=country, zip_code=zip_code, payment_method=payment_method)

        cart_items = Cart.objects.filter(user=user)

        # Create the order items
        for item in cart_items:
            OrderItem.objects.create(order=order, book=item.book, price=item.book.price, quantity=item.quantity)

        return redirect('/order_success')

# This function is used to handle the order success page after a customer places an order. It retrieves the most recent order for the logged in use
def order_success(request):
    user = User.objects.get(id=request.session['id'])
    recent_order = Order.objects.filter(customer=user).latest('created_at')
    order_items = OrderItem.objects.filter(order=recent_order)
    total_price = 0
    for item in order_items:
        total_price += item.book.price * item.quantity
    context = {
    'order_items': order_items,
    'total_price': total_price
    }
    return render(request, 'order_success.html', context)

# This function is used to handle the my account page for the logged in user.
def my_account(request): 
    return render(request, 'my_account.html')

# This function is used to handle the book detail page for a specific book. It retrieves the book using the book_id passed in the URL
def book_detail(request, book_id): 

    book =  Book.objects.get(id=book_id)
    context = {
        'book': Book.objects.get(id=book_id),
        'categories' : Category.objects.all(),
        'book_reviews' : Review.objects.filter(book = book),
        'book_reviews_number' : Review.objects.filter(book = book).count

    }
    return render(request, 'book_detail.html', context)

# This function is used to handle the post request of adding a review for a book and updating the book's total rating.
def write_review(request, book_id):
    # Get the book and user
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/login_page')
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        # Get the rating and review from the request
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        book.total_rating += int(rating)
        book.save()

        # Create the review
        Review.objects.create(customer=user, book=book, rating=rating, review=review)

        return redirect('/book_detail/' + str(book_id))

# This function is used to handle the search request by filtering books by the search query and render the result
def search(request):
    # Get the search query from the request
    query = request.GET.get('q')
    # Filter books by the search query
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = []
    context = {
        'books': books,
        'categories': Category.objects.all(),
    }
    # Render the search results template with the search results and categories
    return render(request, 'search_results.html', context)

# This function is used to view all books by categories. 
def categories(request): 
    context = {
        'books' : Book.objects.all(),
        'authors' : Author.objects.all(),
        'categories' : Category.objects.all()
    }

    return render(request, 'categories.html', context)

# This function is used to view a specific category by getting the it by its name, and getting all books in that category. 
def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    category_books = Book.objects.filter(category=category)

    context = {
        'category_books': category_books,
        'category_name': category_name,
        'categories' : Category.objects.all()

        }
    
    return render(request, 'category.html', context)

# This function is used to render the admin page, which displays all data.
def admin_page(request):
    # To view All Orders to admin 
    # Retrieve all orders from the database
    user = User.objects.get(id=request.session['id'])
    if user.is_admin:
            

            orders = Order.objects.all()
            users = User.objects.all()
            messages = Message.objects.all()



            # Retrieve all order items for each order
            for order in orders:
                order.items = OrderItem.objects.filter(order=order)
                order.total_price = sum(item.price * item.quantity for item in order.items)

            # Pass the orders and their items to the template

            context = {
            'books' : Book.objects.all(),
            'authors' : Author.objects.all(),
            'categories' : Category.objects.all(),
            'orders' :orders,
            'users' : users,
            'messages' : messages,
            'messages_number': messages.count

            }
            
            return render(request, 'admin_page.html', context)
    else:
        return redirect('/home')

# This function is used to handle the request to delete an order by getting the order by its id, and deleting it.
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('/admin_page')

# This function is used to handle the request to delete a book by getting the book by its id, and deleting it.
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/admin_page')

# This function to add an admin user based on their email
def add_admin(request):
    if request.method == "POST":
        email = request.POST.get("admin_email")
        user = User.objects.get(email=email)
        user.is_admin = True
        user.save()
        return redirect("/admin_page")

# This function to add an admin user based on their id
def add_as_admin(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_admin = True
    user.save()
    return redirect("/admin_page")

# This function to remove an admin user based on their id
def remove_as_admin(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_admin = False
    user.save()
    return redirect("/admin_page")

# This function allow users to send message with their issues to admin 
def send_message(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        Message.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('/home')

# This function allow admin to see the messages from users
def view_messages(request): 
    messages = Message.objects.all()
    context = {
        'messages' : messages,
        'messages_number': messages.count
    }

    return render(request, "messages.html", context)

# This function is used to handle the request to delete an message by getting the order by its id, and deleting it.
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect('/view_messages')

# This function edit book information by admin 
def edit_book(request, book_id):
    if request.method == 'POST':
        # Get the form data
        author = Author.objects.get(id=request.POST.get('author'))
        category = Category.objects.get(id=request.POST.get('category'))
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        
        # Update the book in the database
        book = Book.objects.get(id=book_id)
        book.author = author
        book.category = category
        book.title = title
        book.price = price
        book.description = description
        book.save()
        
        return redirect(f'/book_detail/{book_id}')
    else:
        # Get the book and related data to display in the form
        book = Book.objects.get(id=book_id)
        authors = Author.objects.all()
        categories = Category.objects.all()
        
        context = {
            'book': book,
            'authors': authors,
            'categories': categories
        }
        return render(request, 'edit_book.html', context)
