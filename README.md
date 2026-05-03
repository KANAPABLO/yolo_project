# Système Multi-Agents IA – Détection d'anomalies vidéo 🎯

Projet académique réalisé dans le cadre du BUT Science des Données à l'IUT de Metz.

## Description

Système de **détection de chutes en temps réel** basé sur une architecture **multi-agents IA**.
Chaque agent est responsable d'une tâche précise et communique avec les suivants.

```
Agent Capture (OpenCV)
    ↓  flux vidéo frame par frame
Agent Détection (YOLOv8)
    ↓  anomalies détectées
Agent Alerte (Streamlit)
    ↓  affichage en direct + historique
```

## Architecture multi-agents

| Agent | Rôle | Technologie |
|-------|------|-------------|
| **AgentCapture** | Ouvre la source vidéo et fournit les frames | OpenCV |
| **AgentDetection** | Analyse chaque frame, détecte les personnes et les chutes | YOLOv8 |
| **AgentAlerte** | Reçoit les anomalies, les horodate, maintient l'historique | Python |

### Logique de détection de chute

Une chute est détectée quand la **bounding box d'une personne est plus large que haute** :

```
ratio = largeur / hauteur > 1.4 → chute probable
```

Une personne debout a une bounding box verticale (hauteur > largeur).
Une personne au sol a une bounding box horizontale (largeur > hauteur).

## Fonctionnalités

- ✅ Analyse en **temps réel** (webcam ou fichier vidéo)
- ✅ **Bounding boxes** colorées : vert = personne normale, rouge = chute
- ✅ **Historique des alertes** avec horodatage
- ✅ **Compteur** de personnes détectées et d'anomalies
- ✅ **Anti-spam** : délai minimum entre deux alertes
- ✅ **Interface Streamlit** déployable en ligne

## Installation

```bash
# 1. Cloner le repo
git clone https://github.com/KANAPABLO/yolo-detection-anomalies
cd yolo-detection-anomalies

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

Le modèle YOLOv8 (`yolov8n.pt`) se télécharge automatiquement au premier lancement.

## Utilisation

1. Choisir la source : **fichier vidéo** ou **webcam**
2. Choisir le modèle : `yolov8n` (rapide) ou `yolov8s` (précis)
3. Cliquer sur **▶️ Démarrer**
4. Les alertes apparaissent en temps réel dans le panneau de droite

## Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

- **Python** – langage principal
- **YOLOv8** (Ultralytics) – détection d'objets temps réel
- **OpenCV** – capture et traitement vidéo
- **Streamlit** – interface web interactive

## Structure du projet

```
yolo-detection-anomalies/
├── app.py                    # Application principale Streamlit
├── requirements.txt          # Dépendances
├── agents/
│   ├── __init__.py
│   ├── agent_capture.py      # Agent 1 : capture vidéo
│   ├── agent_detection.py    # Agent 2 : détection YOLO
│   └── agent_alerte.py       # Agent 3 : gestion des alertes
└── README.md
```

## Auteur

**Souleymane NDIAYE** – BUT Science des Données, IUT de Metz  
[LinkedIn](https://www.linkedin.com/in/souleymane-ndiaye-887578322)
