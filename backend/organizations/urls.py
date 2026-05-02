from django.urls import path
from .views import OrganizationListCreateView, OrganizationDetailView, MembershipListView

urlpatterns = [
    path('', OrganizationListCreateView.as_view(), name='org-list'),
    path('<int:pk>/', OrganizationDetailView.as_view(), name='org-detail'),
    path('<int:org_id>/members/', MembershipListView.as_view(), name='org-members'),
]