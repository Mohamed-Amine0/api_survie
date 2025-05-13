from django.urls import path
from .views import ScenarioDetailView, FaireChoixView, NouvellePartieView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('scenario/<int:scenario_id>/', ScenarioDetailView.as_view(), name='scenario_detail'),
    path('scenario/<int:scenario_id>/choisir/<int:choix_id>/', FaireChoixView.as_view(), name='faire_choix'),
    path('nouvelle-partie/', NouvellePartieView.as_view(), name='nouvelle_partie'),
]
