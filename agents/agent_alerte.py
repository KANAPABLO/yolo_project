"""
Agent Alerte – responsable de la gestion et de l'historique des alertes.
Reçoit les anomalies de l'Agent Détection et les stocke.
"""

from datetime import datetime


class AgentAlerte:
    """
    Agent 3 : Alerte
    Rôle : recevoir les anomalies, les horodater et maintenir l'historique.
    """

    DELAI_ALERTE = 2    # secondes minimum entre deux alertes du même type

    def __init__(self):
        self.historique   = []          # toutes les alertes
        self.derniere_alerte = None     # timestamp de la dernière alerte

    def traiter(self, anomalies):
        """
        Reçoit la liste d'anomalies de l'Agent Détection.
        Filtre les doublons rapides et enregistre les nouvelles alertes.
        Retourne True si une nouvelle alerte a été déclenchée.
        """
        if not anomalies:
            return False

        maintenant = datetime.now()

        # Anti-spam : ne pas répéter une alerte trop rapidement
        if self.derniere_alerte:
            delta = (maintenant - self.derniere_alerte).total_seconds()
            if delta < self.DELAI_ALERTE:
                return False

        for anomalie in anomalies:
            alerte = {
                "horodatage" : maintenant.strftime("%H:%M:%S"),
                "type"       : anomalie["type"],
                "confiance"  : anomalie["confiance"],
                "position"   : anomalie["position"],
            }
            self.historique.append(alerte)

        self.derniere_alerte = maintenant
        return True

    def get_historique(self):
        """Retourne l'historique des alertes (plus récent en premier)."""
        return list(reversed(self.historique))

    def nb_alertes(self):
        return len(self.historique)

    def reinitialiser(self):
        self.historique = []
        self.derniere_alerte = None
