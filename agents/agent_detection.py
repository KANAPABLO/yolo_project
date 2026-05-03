"""
Agent Détection – responsable de l'analyse des frames avec YOLO.
Détecte les personnes et identifie les chutes potentielles.
"""

import cv2
import numpy as np
from ultralytics import YOLO


class AgentDetection:
    """
    Agent 2 : Détection
    Rôle : analyser chaque frame avec YOLOv8 et détecter les anomalies.
    Anomalie ciblée : chute d'une personne (bounding box horizontale).
    """

    SEUIL_CONFIANCE = 0.5      # Confiance minimale pour valider une détection
    RATIO_CHUTE     = 1.4      # Largeur / Hauteur > ce ratio → chute probable

    def __init__(self, modele="yolov8n.pt"):
        """
        modele : yolov8n.pt (nano, léger) ou yolov8s.pt (small, plus précis)
        """
        self.modele = YOLO(modele)
        self.id_personne = 0    # COCO class 0 = person

    def analyser(self, frame):
        """
        Analyse une frame et retourne :
        - frame_annotee : frame avec les boîtes dessinées
        - anomalies     : liste des anomalies détectées
        - personnes     : nombre de personnes détectées
        """
        resultats = self.modele(frame, verbose=False)[0]
        anomalies = []
        nb_personnes = 0
        frame_annotee = frame.copy()

        for box in resultats.boxes:
            cls        = int(box.cls[0])
            confiance  = float(box.conf[0])

            # On ne traite que les personnes avec confiance suffisante
            if cls != self.id_personne or confiance < self.SEUIL_CONFIANCE:
                continue

            nb_personnes += 1
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            largeur  = x2 - x1
            hauteur  = y2 - y1

            # Détection de chute : ratio largeur/hauteur élevé
            chute = (hauteur > 0) and (largeur / hauteur > self.RATIO_CHUTE)

            if chute:
                anomalies.append({
                    "type"      : "CHUTE DÉTECTÉE",
                    "confiance" : round(confiance, 2),
                    "position"  : (x1, y1, x2, y2),
                })
                # Boîte rouge pour chute
                cv2.rectangle(frame_annotee, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(frame_annotee, f"CHUTE! {confiance:.0%}",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)
            else:
                # Boîte verte pour personne normale
                cv2.rectangle(frame_annotee, (x1, y1), (x2, y2), (0, 200, 0), 2)
                cv2.putText(frame_annotee, f"Personne {confiance:.0%}",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 200, 0), 2)

        return frame_annotee, anomalies, nb_personnes
