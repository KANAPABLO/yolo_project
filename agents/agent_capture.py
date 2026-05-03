"""
Agent Capture – responsable de la capture du flux vidéo.
Source : webcam en temps réel OU fichier vidéo uploadé.
"""

import cv2


class AgentCapture:
    """
    Agent 1 : Capture
    Rôle : ouvrir la source vidéo et fournir les frames une par une.
    """

    def __init__(self, source=0):
        """
        source : 0 = webcam, ou chemin vers un fichier vidéo (str)
        """
        self.source = source
        self.cap = None

    def demarrer(self):
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Impossible d'ouvrir la source vidéo : {self.source}")

    def lire_frame(self):
        """
        Retourne (True, frame) si la lecture est possible, (False, None) sinon.
        """
        if self.cap is None:
            return False, None
        ret, frame = self.cap.read()
        return ret, frame

    def arreter(self):
        if self.cap:
            self.cap.release()
            self.cap = None

    def est_actif(self):
        return self.cap is not None and self.cap.isOpened()
