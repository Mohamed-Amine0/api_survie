from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Scenario, Choix, JoueurState
from .serializers import ScenarioSerializer, ChoixSerializer, JoueurStateSerializer, ReponseChoixSerializer

import uuid

class ScenarioDetailView(APIView):
    """
    Affiche les détails d'un scénario avec ses choix possibles
    """
    def get(self, request, scenario_id):
        scenario = get_object_or_404(Scenario, pk=scenario_id)
        serializer = ScenarioSerializer(scenario)
        return Response(serializer.data)
        
class FaireChoixView(APIView):
    """
    Permet de faire un choix dans un scénario et de voir les conséquences
    """
    def post(self, request, scenario_id, choix_id):
        scenario = get_object_or_404(Scenario, pk=scenario_id)
        choix = get_object_or_404(Choix, pk=choix_id, scenario=scenario)
        
        # Récupère ou crée l'état du joueur
        joueur_state = self._get_or_create_joueur_state(request)
        
        # Vérifier que le joueur est bien au bon scénario
        if joueur_state.scenario_actuel and joueur_state.scenario_actuel.id != scenario_id:
            return Response({"error": "Vous n'êtes pas à ce scénario actuellement."},
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Appliquer les effets du choix
        nouvel_etat = joueur_state.appliquer_choix(choix)
        scenario_suivant = choix.scenario_suivant or scenario
        
        # Préparer la réponse
        response_data = {
            "message": choix.texte,
            "etat": nouvel_etat,
            "suivant": {
                "id": scenario_suivant.id,
                "texte": scenario_suivant.texte
            }
        }
        
        return Response(response_data)
    
    def _get_or_create_joueur_state(self, request):
        # Si l'utilisateur est authentifié
        if request.user.is_authenticated:
            joueur_state, created = JoueurState.objects.get_or_create(
                user=request.user,
                defaults={
                    'scenario_actuel': Scenario.objects.first()
                }
            )
        # Sinon, utiliser la session
        else:
            session_id = request.session.get('joueur_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['joueur_session_id'] = session_id
            
            joueur_state, created = JoueurState.objects.get_or_create(
                session_id=session_id,
                defaults={
                    'scenario_actuel': Scenario.objects.first()
                }
            )
        
        return joueur_state
        
class IndexView(TemplateView):
    """
    Vue principale pour afficher l'interface de jeu
    """
    template_name = "survie_api/index.html"
    
class NouvellePartieView(APIView):
    """
    Commence une nouvelle partie de survie sur l'île
    """
    def post(self, request):
        # Créer ou réinitialiser l'état du joueur
        joueur_state = self._reinit_joueur_state(request)
        
        # Obtenir le premier scénario
        premier_scenario = Scenario.objects.first()
        if not premier_scenario:
            return Response({"error": "Aucun scénario disponible."},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Renvoyer le premier scénario
        serializer = ScenarioSerializer(premier_scenario)
        return Response(serializer.data)
    
    def _reinit_joueur_state(self, request):
        # Si l'utilisateur est authentifié
        if request.user.is_authenticated:
            JoueurState.objects.filter(user=request.user).delete()
            joueur_state = JoueurState.objects.create(
                user=request.user,
                scenario_actuel=Scenario.objects.first()
            )
        # Sinon, utiliser la session
        else:
            session_id = request.session.get('joueur_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['joueur_session_id'] = session_id
            
            JoueurState.objects.filter(session_id=session_id).delete()
            joueur_state = JoueurState.objects.create(
                session_id=session_id,
                scenario_actuel=Scenario.objects.first()
            )
        
        return joueur_state
