from django.contrib import admin
from .models import Scenario, Choix, JoueurState

class ChoixInline(admin.TabularInline):
    model = Choix
    extra = 1
    fk_name = 'scenario'

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre')
    search_fields = ('titre', 'texte')
    inlines = [ChoixInline]

@admin.register(Choix)
class ChoixAdmin(admin.ModelAdmin):
    list_display = ('texte', 'scenario', 'delta_faim', 'delta_energie', 'delta_moral', 'scenario_suivant')
    list_filter = ('scenario',)
    search_fields = ('texte',)

@admin.register(JoueurState)
class JoueurStateAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'faim', 'energie', 'moral', 'scenario_actuel', 'date_mise_a_jour')
    list_filter = ('scenario_actuel',)
    search_fields = ('user__username', 'session_id')
