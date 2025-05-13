from rest_framework import serializers
from .models import Scenario, Choix, JoueurState

class ChoixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choix
        fields = ['id', 'texte']

class ScenarioSerializer(serializers.ModelSerializer):
    choix = ChoixSerializer(many=True, read_only=True)
    
    class Meta:
        model = Scenario
        fields = ['id', 'titre', 'texte', 'choix']

class JoueurStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoueurState
        fields = ['id', 'faim', 'energie', 'moral', 'scenario_actuel']

class ChoixDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choix
        fields = ['id', 'texte', 'delta_faim', 'delta_energie', 'delta_moral', 'scenario_suivant']

class ScenarioSuivantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id', 'texte']

class EtatJoueurSerializer(serializers.Serializer):
    faim = serializers.IntegerField()
    energie = serializers.IntegerField()
    moral = serializers.IntegerField()

class ReponseChoixSerializer(serializers.Serializer):
    message = serializers.CharField()
    etat = EtatJoueurSerializer()
    suivant = ScenarioSuivantSerializer()
