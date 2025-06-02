from django.urls import path
from newsletters.apps import NewslettersConfig
from newsletters.views import RecipientCreateView, RecipientDeleteView, RecipientDetailView, RecipientUpdateView, \
    MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView, DistributionDeleteView, \
    DistributionListView, DistributionCreateView, DistributionDetailView, DistributionUpdateView, HomeListView, \
    distribution_reports, StartDistributionView

app_name = NewslettersConfig.name

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("distribution_list/", DistributionListView.as_view(), name="distribution_list"),
    path("distribution_detail/<int:pk>/", DistributionDetailView.as_view(), name="distribution_detail"),
    path("distribution_create/", DistributionCreateView.as_view(), name="distribution_create"),
    path("distribution_update/<int:pk>/", DistributionUpdateView.as_view(), name="distribution_update"),
    path("distribution_delete/<int:pk>/", DistributionDeleteView.as_view(), name="distribution_delete"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("recipient_update/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("distribution_reports/", distribution_reports, name="distribution_reports"),
    path("distribution_start/<int:pk>/", StartDistributionView.as_view(), name="distribution_start"),
]
