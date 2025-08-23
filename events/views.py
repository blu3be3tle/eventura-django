from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import is_organizer
from .models import Event, Category
from .forms import EventForm, CategoryForm


# Event
class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category').prefetch_related('users').annotate(
            user_count=Count('users')
        )

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related('users')


@method_decorator(is_organizer, name='dispatch')
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event-list')


@method_decorator(is_organizer, name='dispatch')
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def get_success_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.get_object().pk})


@method_decorator(is_organizer, name='dispatch')
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_delete.html'
    success_url = reverse_lazy('event-list')


# Categories
def category_list(request):
    categories = Category.objects.annotate(event_count=Count('events'))
    return render(request, 'category/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(
        Category.objects.prefetch_related('events'), pk=pk)
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
            messages.success(
                request, f"You have successfully RSVP'd for {event.name}!")

    return redirect('event-detail', pk=pk)
