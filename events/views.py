from .forms import EventForm, CategoryForm
from .models import Event, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from users.models import User


# Event
def event_list(request):

    queryset = Event.objects.all()

    queryset = queryset.select_related('category').prefetch_related('users').annotate(
        user_count=Count('users')
    )

    category_id = request.GET.get('category')
    if category_id:
        queryset = queryset.filter(category__id=category_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])

    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(
                location__icontains=search_query)
        )

    categories = Category.objects.all()

    context = {
        'events': queryset,
        'categories': categories,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):

    event = get_object_or_404(
        Event.objects.select_related(
            'category').prefetch_related('users'),
        pk=pk
    )
    context = {'event': event}
    return render(request, 'events/event_detail.html', context)


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'events/event_form.html', context)


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', pk=pk)
    else:
        form = EventForm(instance=event)
    context = {'form': form, 'event': event}
    return render(request, 'events/event_form.html', context)


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    context = {'event': event}
    return render(request, 'events/event_delete.html', context)


# Category
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('category-detail', pk=category.pk)
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'category/category_form.html', context)


def category_list(request):
    categories = Category.objects.all().annotate(event_count=Count('events'))
    context = {'categories': categories}
    return render(request, 'category/category_list.html', context)


def category_detail(request, pk):
    category = get_object_or_404(
        Category.objects.prefetch_related('events'),
        pk=pk
    )
    context = {'category': category}
    return render(request, 'category/category_detail.html', context)


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    context = {'form': form, 'category': category}
    return render(request, 'category/category_form.html', context)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    context = {'category': category}
    return render(request, 'category/category_delete.html', context)
