from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            fromDate = form.cleaned_data.get('fromDate')
            toDate = form.cleaned_data.get('toDate')
            categories = form.cleaned_data.get('categories')
            sortByDate = form.cleaned_data.get('sortByDate')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if fromDate:
                queryset = queryset.filter(date__gte=fromDate)
            if toDate:
                queryset = queryset.filter(date__lte=toDate)
            if categories:
                queryset = queryset.filter(category__in=categories)
            if sortByDate == 'asc':
                queryset = queryset.order_by('date')
            if sortByDate == 'desc':
                queryset = queryset.order_by('-date')

        totalAmountSpent = round(queryset.aggregate(total=Sum('amount'))['total'] or 0, 2)

        expense_summary = queryset.annotate(month=TruncMonth('date')).values('month').annotate(
            total_spent=Sum('amount'))

        for expense in expense_summary:
            expense['total_spent'] = round(expense['total_spent'], 2)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            totalAmountSpent=totalAmountSpent,
            expense_summary=expense_summary,
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_expenses=Count('expense'))
        return queryset
