from django.db import models
from django.contrib.auth.models import User

# Modèle pour représenter un scénario du jeu
class Scenario(models.Model):
    titre = models.CharField(max_length=100)
    texte = models.TextField(help_text="Description narrative de l'étape du jeu")
    
    def __str__(self):
        return self.titre

# Modèle pour représenter un choix possible dans un scénario
class Choix(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='choix')
    texte = models.CharField(max_length=255)
    delta_faim = models.IntegerField(default=0)
    delta_energie = models.IntegerField(default=0)
    delta_moral = models.IntegerField(default=0)
    scenario_suivant = models.ForeignKey(Scenario, on_delete=models.SET_NULL, null=True, blank=True, related_name='choix_precedent')
    
    def __str__(self):
        return f"{self.texte} - {self.scenario.titre}"

# Modèle pour représenter l'état du joueur
class JoueurState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)  # Pour les utilisateurs non authentifiés
    faim = models.IntegerField(default=100)  # 0 = Affamé, 100 = Rassasié
    energie = models.IntegerField(default=100)  # 0 = Épuisé, 100 = Plein d'énergie
    moral = models.IntegerField(default=100)  # 0 = Déprimé, 100 = Enthousiaste
    scenario_actuel = models.ForeignKey(Scenario, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(session_id__isnull=False),
                name='joueur_identification'
            )
        ]
    
    def __str__(self):
        if self.user:
            return f"État de {self.user.username}"
        return f"État de session {self.session_id}"
    
    def appliquer_choix(self, choix):
        # Mettre à jour les stats du joueur
        self.faim = max(0, min(100, self.faim + choix.delta_faim))
        self.energie = max(0, min(100, self.energie + choix.delta_energie))
        self.moral = max(0, min(100, self.moral + choix.delta_moral))
        
        # Mettre à jour le scénario actuel si un scénario suivant est défini
        if choix.scenario_suivant:
            self.scenario_actuel = choix.scenario_suivant
        
        self.save()
        
        return {
            'faim': self.faim,
            'energie': self.energie,
            'moral': self.moral,
        }
