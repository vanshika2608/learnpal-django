from django import forms
from .models import LearningGoal, Resource

class LearningGoalForm(forms.ModelForm):
    PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={
        "class": "modern-select",
        "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out;"
    }))

    class Meta:
        model = LearningGoal
        fields = ["title", "description", "status", "progress", "due_date", "priority", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "modern-input",
                "placeholder": "Enter goal title",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "description": forms.Textarea(attrs={
                "class": "modern-textarea",
                "placeholder": "Describe your goal",
                "rows": 3,
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem; resize: vertical;"
            }),
            "status": forms.Select(attrs={
                "class": "modern-select",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "progress": forms.NumberInput(attrs={
                "class": "modern-input",
                "min": 0,
                "max": 100,
                "placeholder": "0-100",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "due_date": forms.DateInput(attrs={
                "class": "modern-input",
                "type": "date",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "tags": forms.TextInput(attrs={
                "class": "modern-input",
                "placeholder": "e.g. Python, Django",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title.strip():
            raise forms.ValidationError("Title cannot be empty.")
        return title

    def clean_progress(self):
        progress = self.cleaned_data.get('progress')
        if progress < 0 or progress > 100:
            raise forms.ValidationError("Progress must be between 0 and 100.")
        return progress

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')
        try:
            priority_int = int(priority)
        except (TypeError, ValueError):
            raise forms.ValidationError("Priority must be an integer between 1 and 5.")
        if priority_int < 1 or priority_int > 5:
            raise forms.ValidationError("Priority must be between 1 and 5.")
        return priority_int

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "url", "topic", "goal", "is_bookmarked"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "modern-input",
                "placeholder": "Resource title",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "url": forms.URLInput(attrs={
                "class": "modern-input",
                "placeholder": "https://example.com",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "topic": forms.TextInput(attrs={
                "class": "modern-input",
                "placeholder": "Topic name",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "goal": forms.Select(attrs={
                "class": "modern-select",
                "style": "width: 100%; padding: 0.75rem; border: 1px solid #374151; border-radius: 0.5rem; background-color: #1f2937; color: #f9fafb; font-size: 0.875rem; transition: all 0.2s ease-in-out; margin-bottom: 0.5rem;"
            }),
            "is_bookmarked": forms.CheckboxInput(attrs={
                "class": "modern-checkbox",
                "style": "width: 1.25rem; height: 1.25rem; accent-color: #3b82f6; margin-right: 0.5rem;"
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title.strip():
            raise forms.ValidationError("Title cannot be empty.")
        return title

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url.startswith(('http://', 'https://')):
            raise forms.ValidationError("URL must start with http:// or https://")
        return url
