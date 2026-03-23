from django import forms
from django.utils import timezone
from datetime import datetime
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'category', 
                  'due_date', 'due_time']
        
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title','').strip()
        
        if not title:
            self.add_error('title', 'Title cannot be empty')
        
        if len(title) < 3:
            self.add_error('title', 'Title must be at least 3 characters long.')
        return title
    
    def clean(self):
        cleaned_data =  super().clean()
        due_date = cleaned_data.get('due_date')
        due_time = cleaned_data.get('due_time')

        if due_date:
            today = timezone.localdate()

            if due_date < today:
                self.add_error('due_date', "Due date cannot be in the past")
            
            if due_date == today and due_time:
                now_time = timezone.localtime().time()

                if due_time < now_time:
                    self.add_error('due_time', "Time must be in the Future.")

        return cleaned_data