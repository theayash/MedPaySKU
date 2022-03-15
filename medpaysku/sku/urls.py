from django.urls import path
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path('transaction/<int:transaction_id>', views.TransactionDetails.as_view()),
    path('transaction-summary-bySKU/<int:number_of_days>', views.TransactionSummaryBySKU.as_view()),
    path('transaction-summary-bycategory/<int:number_of_days>', views.TransactionSummaryBySKUCategory.as_view()),

    # For checking the schema
    path('openapi/', get_schema_view(
                                title="MedPay SKU Manager",
                                description="Get Transaction Details"
                                ), name='openapi-schema'),
    # Swagger UI Path
    path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url': 'openapi-schema'}
         ), name='swagger-ui'),
]
