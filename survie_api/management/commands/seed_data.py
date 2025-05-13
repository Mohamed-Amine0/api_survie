from django.core.management.base import BaseCommand
from survie_api.models import Scenario, Choix

class Command(BaseCommand):
    help = 'Crée des données de test pour le jeu de survie'

    def handle(self, *args, **options):
        # Suppression des données existantes
        self.stdout.write(self.style.WARNING('Suppression des scénarios et choix existants...'))
        Choix.objects.all().delete()
        Scenario.objects.all().delete()

        # Création des scénarios
        self.stdout.write(self.style.NOTICE('Création des scénarios...'))
        
        # Scénario initial
        debut = Scenario.objects.create(
            titre="Le réveil sur l'île",
            texte="Tu te réveilles sur une plage déserte. La tête te tourne et tu es désorienté. Ton avion s'est écrasé et tu es le seul survivant visible. Que fais-tu en premier ?"
        )
        
        # Autres scénarios
        explorer_jungle = Scenario.objects.create(
            titre="La jungle mystérieuse",
            texte="Tu pénètres dans la jungle dense. Les bruits d'animaux résonnent autour de toi. Tu aperçois un sentier qui semble mener quelque part et des fruits sur certains arbres."
        )
        
        chercher_eau = Scenario.objects.create(
            titre="À la recherche d'eau",
            texte="Tu marches le long de la plage à la recherche d'eau douce. Après une heure de marche, tu entends le son d'une cascade au loin."
        )
        
        construire_abri = Scenario.objects.create(
            titre="Construction d'un abri",
            texte="Tu décides qu'il te faut un abri. Tu rassembles des branches, des feuilles de palmier et tout ce qui pourrait être utile."
        )
        
        cascade = Scenario.objects.create(
            titre="La cascade",
            texte="Tu arrives devant une magnifique cascade d'eau douce qui se déverse dans un bassin naturel. L'eau a l'air limpide."
        )
        
        nuit_plage = Scenario.objects.create(
            titre="La nuit sur la plage",
            texte="Le soleil se couche et tu n'as pas d'abri. La température baisse et tu entends des bruits inquiétants venant de la jungle."
        )
        
        nuit_abri = Scenario.objects.create(
            titre="Première nuit dans l'abri",
            texte="Ton abri rudimentaire te protège du vent et d'une légère pluie qui commence à tomber. Tu te sens relativement en sécurité."
        )
        
        fruits_inconnus = Scenario.objects.create(
            titre="Les fruits mystérieux",
            texte="Tu trouves des fruits colorés que tu n'as jamais vus auparavant. Ils ont l'air juteux mais tu ne sais pas s'ils sont comestibles."
        )

        # Création des choix
        self.stdout.write(self.style.NOTICE('Création des choix...'))
        
        # Choix pour le scénario de début
        Choix.objects.create(
            scenario=debut,
            texte="Explorer la jungle à la recherche de nourriture",
            delta_faim=0,
            delta_energie=-10,
            delta_moral=-5,
            scenario_suivant=explorer_jungle
        )
        
        Choix.objects.create(
            scenario=debut,
            texte="Marcher le long de la plage pour trouver de l'eau douce",
            delta_faim=0,
            delta_energie=-15,
            delta_moral=0,
            scenario_suivant=chercher_eau
        )
        
        Choix.objects.create(
            scenario=debut,
            texte="Construire un abri rudimentaire avec ce que tu trouves",
            delta_faim=0,
            delta_energie=-20,
            delta_moral=+10,
            scenario_suivant=construire_abri
        )
        
        # Choix pour la jungle
        Choix.objects.create(
            scenario=explorer_jungle,
            texte="Suivre le sentier plus profondément dans la jungle",
            delta_faim=0,
            delta_energie=-15,
            delta_moral=+5,
            scenario_suivant=cascade
        )
        
        Choix.objects.create(
            scenario=explorer_jungle,
            texte="Cueillir et goûter les fruits inconnus",
            delta_faim=+20,
            delta_energie=+10,
            delta_moral=-5,
            scenario_suivant=fruits_inconnus
        )
        
        Choix.objects.create(
            scenario=explorer_jungle,
            texte="Retourner à la plage avant la tombée de la nuit",
            delta_faim=-5,
            delta_energie=-5,
            delta_moral=-5,
            scenario_suivant=nuit_plage
        )
        
        # Choix pour la recherche d'eau
        Choix.objects.create(
            scenario=chercher_eau,
            texte="Suivre le son de la cascade",
            delta_faim=-5,
            delta_energie=-10,
            delta_moral=+15,
            scenario_suivant=cascade
        )
        
        Choix.objects.create(
            scenario=chercher_eau,
            texte="Retourner à la plage et chercher ailleurs",
            delta_faim=-10,
            delta_energie=-15,
            delta_moral=-10,
            scenario_suivant=nuit_plage
        )
        
        # Choix pour la construction d'abri
        Choix.objects.create(
            scenario=construire_abri,
            texte="Améliorer l'abri pour le rendre plus solide",
            delta_faim=-5,
            delta_energie=-20,
            delta_moral=+15,
            scenario_suivant=nuit_abri
        )
        
        Choix.objects.create(
            scenario=construire_abri,
            texte="Partir chercher de la nourriture maintenant que tu as un abri",
            delta_faim=+15,
            delta_energie=-15,
            delta_moral=+5,
            scenario_suivant=explorer_jungle
        )
        
        # Choix pour la cascade
        Choix.objects.create(
            scenario=cascade,
            texte="Boire l'eau et te rafraîchir",
            delta_faim=0,
            delta_energie=+20,
            delta_moral=+15,
            scenario_suivant=explorer_jungle
        )
        
        Choix.objects.create(
            scenario=cascade,
            texte="Construire un abri près de la cascade",
            delta_faim=-5,
            delta_energie=-25,
            delta_moral=+10,
            scenario_suivant=nuit_abri
        )
        
        # Choix pour la nuit sur la plage
        Choix.objects.create(
            scenario=nuit_plage,
            texte="Essayer de dormir malgré le froid",
            delta_faim=-10,
            delta_energie=+10,
            delta_moral=-15,
            scenario_suivant=debut
        )
        
        Choix.objects.create(
            scenario=nuit_plage,
            texte="Construire un feu pour te réchauffer",
            delta_faim=-5,
            delta_energie=-15,
            delta_moral=+5,
            scenario_suivant=debut
        )
        
        # Choix pour la nuit dans l'abri
        Choix.objects.create(
            scenario=nuit_abri,
            texte="Dormir profondément grâce à la sécurité de l'abri",
            delta_faim=-10,
            delta_energie=+30,
            delta_moral=+10,
            scenario_suivant=debut
        )
        
        Choix.objects.create(
            scenario=nuit_abri,
            texte="Rester vigilant et observer les environs",
            delta_faim=-5,
            delta_energie=+5,
            delta_moral=-5,
            scenario_suivant=debut
        )
        
        # Choix pour les fruits inconnus
        Choix.objects.create(
            scenario=fruits_inconnus,
            texte="Manger plus de fruits pour calmer ta faim",
            delta_faim=+25,
            delta_energie=-15,
            delta_moral=-10,
            scenario_suivant=nuit_plage
        )
        
        Choix.objects.create(
            scenario=fruits_inconnus,
            texte="Arrêter de manger par prudence et chercher autre chose",
            delta_faim=+10,
            delta_energie=-10,
            delta_moral=+5,
            scenario_suivant=chercher_eau
        )
        
        self.stdout.write(self.style.SUCCESS('Données de test créées avec succès !'))
