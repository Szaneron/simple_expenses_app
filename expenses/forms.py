from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    fromDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    toDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    CHOICES = (
        ('asc', 'Date (oldest first)'),
        ('desc', 'Date (newest first)'),
    )
    sortByDate = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Expense
        fields = ('name', 'fromDate', 'toDate', 'categories', 'sortByDate')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['fromDate'].required = False
        self.fields['toDate'].required = False
        self.fields['categories'].required = False
        self.fields['sortByDate'].required = False
