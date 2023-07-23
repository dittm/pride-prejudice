from django.shortcuts import  render
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Book, Category

from django.shortcuts import get_object_or_404

def home(request):
    books = Book.objects.order_by('name')[:3]
    return render(request, 'library/home.html', {'books': books})

def about(request):
    return render(request, 'library/about.html')

# def book_list(request):
#     books = Book.objects.all()
#     return render(request, 'library/book_list.html', {'books': books})

# def book_list(request):
#     books = Book.objects.order_by('name')
#     paginator = Paginator(books, 4)

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'library/book_list.html', {'page_obj': page_obj})


def book_list(request):
    category = request.GET.get('category')

    categories = Category.objects.all()

    if category:
        books = Book.objects.filter(category__name__iexact=category).order_by('name')
    else:
        books = Book.objects.all().order_by('name')

    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'library/book_list.html', {'page_obj': page_obj, 'selected_category': category, 'categories': categories})

@login_required
@csrf_exempt
def borrow_book(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)

    # Check if the book is available for borrowing
    if book.borrowed_by is None:
        book.borrowed_by = request.user
        book.borrow_date = timezone.now()
        book.save()
        return HttpResponse("Book borrowed successfully")
    else:
        return HttpResponse("Book is already borrowed")

@login_required
@csrf_exempt
def return_book(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    if book.borrowed_by == request.user:
        book.borrowed_by = None
        book.borrow_date = None
        book.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Book not borrowed by the current user."}, status=400)

@login_required
def dashboard(request):
    # Retrieve the list of books borrowed by the current user
    borrowed_books = Book.objects.filter(borrowed_by=request.user)

    return render(request, 'library/dashboard.html', {'borrowed_books': borrowed_books})
