from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EventForm, CategoryForm
from .models import Event, Category


# Events
def event_list(request):
    queryset = Event.objects.select_related('category').prefetch_related('users').annotate(
        user_count=Count('users')
    )

    category_id = request.GET.get('category')
    if category_id:
        queryset = queryset.filter(category__id=category_id)

    start_date, end_date = request.GET.get('start_date'), request.GET.get('end_date')
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])

    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    categories = Category.objects.all()
    context = {'events': queryset, 'categories': categories}
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('users'),
        pk=pk
    )
    return render(request, 'events/event_detail.html', {'event': event})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'event': event})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    return render(request, 'events/event_delete.html', {'event': event})


# Categories
def category_list(request):
    categories = Category.objects.annotate(event_count=Count('events'))
    return render(request, 'category/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(Category.objects.prefetch_related('events'), pk=pk)
    return render(request, 'category/category_detail.html', {'category': category})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('category-detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form, 'category': category})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'category/category_delete.html', {'category': category})


# RSVP
@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        if event.users.filter(id=request.user.id).exists():
            messages.warning(request, "You have already RSVP'd to this event.")
        else:
            event.users.add(request.user)
            messages.success(request, f"You have successfully RSVP'd for {event.name}!")

    return redirect('event-detail', pk=pk)