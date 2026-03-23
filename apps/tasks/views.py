from django.views.generic import (TemplateView, CreateView, ListView,
                                  UpdateView, DeleteView)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from datetime import date
from django.db.models import Q
from .models import Task
from .forms import TaskForm
import calendar


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        tasks = Task.objects.filter(user=self.request.user)

        context.update({
            'today': today,
            'total_tasks': tasks.count(),
            'completed_tasks': tasks.filter(status='done').count(),
            'inprogress_tasks': tasks.filter(status='progress').count(),
            'scheduled_tasks': tasks.filter(due_date__gt=today).count(),
            'today_tasks': tasks.filter(due_date=today).order_by('due_time'),
            'upcoming_tasks': tasks.filter(
                due_date__gt=today,
                status__in=['todo', 'progress']
            ).order_by('due_date', 'due_time')[:5],
        })

        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(user=self.request.user)
        
        active_filter = self.request.GET.get('filter', 'all')
        query = self.request.GET.get('q', '')

        if query:
            tasks = tasks.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        
        if active_filter == 'todo':
            tasks = tasks.filter(status='todo')
        elif active_filter == 'progress':
            tasks = tasks.filter(status='progress')
        elif active_filter == 'done':
            tasks = tasks.filter(status='done')
        elif active_filter == 'high':
            tasks = tasks.filter(priority='high')
        elif active_filter == 'scheduled':
            tasks = tasks.filter(due_date__isnull=False)
        
        return tasks.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_filter'] = self.request.GET.get('filter', 'all')

        context['filters'] = [
            ('All', 'all'),
            ('To Do', 'todo'),
            ('In Progress', 'progress'),
            ('Completed', 'done'),
            ('High Priority', 'high'),
            ('Scheduled', 'scheduled'),
        ]
        return context
    

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_create')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created Successfully")
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_create')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Task Updated Successfully")
        return super().form_valid(form)
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task Delete Successfully")
        return super().delete(request, *args, **kwargs)


class TaskToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)

        task.status = 'todo' if task.status == 'done' else 'done'
        task.save()
        next_url =( 

            request.POST.get('next') 
            or request.META.get('HTTP_REFERER') 
            or 'dashboard'
        )
        return redirect(next_url)


class TaskCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/task_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')

        try:
            year = int(year) if year else today.year
            month = int(month) if month else today.month
        except ValueError:
            year = today.year
            month = today.month

    
        month_name = calendar.month_name[month]
        day_names = list(calendar.day_abbr)

        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
            
        selected_date_str = self.request.GET.get('date')

        selected_date = None
        selected_day_tasks = []

        if selected_date_str:
            try:
                selected_date = date.fromisoformat(selected_date_str)
                selected_day_tasks = Task.objects.filter(
                    user=self.request.user,
                    due_date=selected_date
                ).order_by('due_time')
            except ValueError:
                pass

        month_tasks = Task.objects.filter(
            user=self.request.user,
            due_date__year=year,
            due_date__month=month,
        ).values_list('due_date', flat=True)

        task_dates = set(month_tasks)

        cal = calendar.monthcalendar(year, month)
        calendar_days = []

        for week in cal:
            for day_num in week:
                if day_num == 0:
                    calendar_days.append({'date': None})
                else:
                    d = date(year, month, day_num)
                    calendar_days.append({
                        'date': d,
                        'day': day_num,
                        'is_today': d == today,
                        'is_selected': d == selected_date,
                        'has_tasks': d in task_dates,
                        'other_month': False 
                    })

        context.update({
            'year': year,
            'month': month,
            'month_name': month_name,       
            'prev_month': prev_month,       
            'prev_year': prev_year,         
            'next_month': next_month,       
            'next_year': next_year,         
            'day_names': day_names,         
            'calendar_days': calendar_days,
            'selected_day_tasks': selected_day_tasks,
            'selected_date': selected_date, 
        })

        return context