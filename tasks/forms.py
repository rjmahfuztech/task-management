from django import forms
from tasks.models import Task, TaskDetails

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    def __init__(self, *args, **kwargs):
        # print(args,kwargs)
        employees = kwargs.pop("employees",[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id,emp.name) for emp in employees]

class StyledFormMixin:
    """Mixin to apply style to form field"""
    default_classes = 'border-2 p-2 rounded-md w-full'

    def applyStyledWidget(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f'Enter {field.label.lower()}',
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': 'border-2 p-2 rounded-md mr-2'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'space-y-2'
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple    
        }

        # exclude = ['project', 'is_completed', 'created_at', 'updated_at']
        """Manual Widget"""
        # widgets = {
        #     'title': forms.TextInput(attrs={'class':'border-2 p-2 rounded-md w-full'}),
        #     'description': forms.Textarea(attrs={'class':'border-2 p-2 rounded-md w-full'}),
        #     'due_date': forms.SelectDateWidget(attrs={'class':'border-2 p-2 rounded-md mr-2'}),
        #     'assigned_to': forms.CheckboxSelectMultiple
        # }
    
    """Using Mixin Widget"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.applyStyledWidget();


class TaskDetailsModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = TaskDetails
        fields = ['priority', 'notes']

    """Using Mixin Widget"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.applyStyledWidget();