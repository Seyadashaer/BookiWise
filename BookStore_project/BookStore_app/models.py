from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA_Z0-9._-]+\.[a-zA-z]+$')

# UserManager class is used to handle the validation for user registration and login
class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First Name should contain letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last name should contain letters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format"
        elif len(User.objects.filter(email = postData['email'])) > 0:
            errors['email'] = "Email already registered"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords do not match"

        return errors

    def validate_login(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])):
            user = User.objects.get(email = postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password):
                return errors
            else:
                errors['login'] = "Email OR Password incorrect"
                return errors
        else:
            errors['login'] = "Email OR Password incorrect"
            return errors

# User class is used to define the user model, with fields for first name, last name, email, password, is_admin
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.BinaryField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# Model for category with name, created_at and updated_at fields
class Category(models.Model):
	name = models.CharField(max_length = 100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# Model for author with name, created_at and updated_at fields
class Author(models.Model):
	name = models.CharField(max_length = 100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# Book model represents a book and its details
class Book(models.Model):
	author = models.ForeignKey(Author, on_delete = models.CASCADE) # one to many relationship
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books') # one to many relationship
	title = models.CharField(max_length = 100)
	price = models.IntegerField()
	bookpage = models.FileField(upload_to = "files/bookpage/")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	total_rating = models.IntegerField(default=0)
	description = models.TextField()

# Review model represents a review for a book by customer
class Review(models.Model):
	customer = models.ForeignKey(User, on_delete = models.CASCADE) # one to many relationship
	book = models.ForeignKey(Book, on_delete = models.CASCADE) # many to one relationship
	rating = models.IntegerField()
	review = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# Order model representing orders made by customers
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=150)
    country = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# OrderItem model representing the items of an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

# Cart model represents the cart of a user which contains the books and their quantity
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # method to calculate the total cost of the books in the cart
    def book_total(self):
        return self.quantity * self.book.price

# Wishlist model represents the wishlist of a user which contains the books and their quantity
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Message model represents a message from user and its contents
class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
