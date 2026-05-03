"""
Application principale – Interface Streamlit
Orchestre les 3 agents : Capture → Détection → Alerte
"""

import tempfile
import time
import os

import cv2
import streamlit as st

from agents import AgentCapture, AgentDetection, AgentAlerte

# ── Configuration de la page ──────────────────────────────────
st.set_page_config(
    page_title="Détection d'anomalies – Système Multi-Agents IA",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Système Multi-Agents IA – Détection d'anomalies vidéo")
st.markdown("**Agent Capture** → **Agent Détection (YOLO)** → **Agent Alerte**")
st.divider()

# ── Sidebar : configuration ───────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    source = st.radio(
        "Source vidéo",
        ["📁 Fichier vidéo", "📷 Webcam"],
    )

    modele = st.selectbox(
        "Modèle YOLO",
        ["yolov8n.pt", "yolov8s.pt"],
        help="nano = plus rapide, small = plus précis",
    )

    st.divider()
    st.markdown("### 🤖 Architecture")
    st.markdown("""
    ```
    Agent Capture
    (OpenCV)
        ↓
    Agent Détection
    (YOLOv8)
        ↓
    Agent Alerte
    (Streamlit)
    ```
    """)

# ── Layout principal ──────────────────────────────────────────
col_video, col_alertes = st.columns([2, 1])

with col_video:
    st.subheader("📹 Flux vidéo")
    frame_placeholder = st.empty()
    info_placeholder  = st.empty()

with col_alertes:
    st.subheader("🚨 Alertes en direct")
    stats_placeholder   = st.empty()
    alertes_placeholder = st.empty()

# ── Initialisation des agents ─────────────────────────────────
if "agent_alerte" not in st.session_state:
    st.session_state.agent_alerte = AgentAlerte()

agent_alerte = st.session_state.agent_alerte

# ── Gestion de la source vidéo ────────────────────────────────
fichier_temp = None

if source == "📁 Fichier vidéo":
    fichier = st.file_uploader(
        "Importer une vidéo", type=["mp4", "avi", "mov", "mkv"]
    )
    if fichier:
        # Sauvegarder temporairement
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp.write(fichier.read())
        tmp.close()
        fichier_temp = tmp.name
        source_video = fichier_temp
    else:
        st.info("👆 Importez une vidéo pour démarrer.")
        st.stop()
else:
    source_video = 0  # webcam

# ── Boutons de contrôle ───────────────────────────────────────
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    demarrer = st.button("▶️ Démarrer", use_container_width=True, type="primary")
with col_btn2:
    arreter  = st.button("⏹️ Arrêter",  use_container_width=True)
with col_btn3:
    reset    = st.button("🔄 Reset alertes", use_container_width=True)

if reset:
    agent_alerte.reinitialiser()
    st.rerun()

# ── Boucle principale ─────────────────────────────────────────
if demarrer:

    # Instancier les agents
    agent_capture   = AgentCapture(source=source_video)
    agent_detection = AgentDetection(modele=modele)

    try:
        agent_capture.demarrer()
        st.success("✅ Agents démarrés. Analyse en cours...")

        while agent_capture.est_actif():

            # ── Agent Capture : lire une frame ────────────────
            ret, frame = agent_capture.lire_frame()
            if not ret:
                st.info("Fin de la vidéo.")
                break

            # ── Agent Détection : analyser la frame ──────────
            frame_annotee, anomalies, nb_personnes = agent_detection.analyser(frame)

            # ── Agent Alerte : traiter les anomalies ──────────
            nouvelle_alerte = agent_alerte.traiter(anomalies)

            # ── Affichage vidéo ───────────────────────────────
            frame_rgb = cv2.cvtColor(frame_annotee, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

            # ── Infos sous la vidéo ───────────────────────────
            couleur = "🔴" if anomalies else "🟢"
            info_placeholder.markdown(
                f"{couleur} **Personnes détectées :** {nb_personnes} | "
                f"**Anomalies :** {len(anomalies)} | "
                f"**Total alertes :** {agent_alerte.nb_alertes()}"
            )

            # ── Panneau d'alertes ──────────────────────────────
            with stats_placeholder.container():
                total = agent_alerte.nb_alertes()
                if total == 0:
                    st.metric("🔔 Alertes totales", "0")
                else:
                    st.metric("🔔 Alertes totales", total,
                              delta="⚠️ Nouvelle!" if nouvelle_alerte else None)

            historique = agent_alerte.get_historique()
            if historique:
                alertes_md = ""
                for a in historique[:10]:  # dernières 10
                    alertes_md += (
                        f"🚨 **{a['horodatage']}** — {a['type']}\n"
                        f"   Confiance : {a['confiance']:.0%}\n\n"
                    )
                alertes_placeholder.markdown(alertes_md)
            else:
                alertes_placeholder.info("Aucune anomalie détectée pour l'instant.")

            # Pause courte pour ne pas surcharger
            time.sleep(0.03)

            # Vérifier si l'utilisateur a cliqué sur Arrêter
            if arreter:
                break

    except Exception as e:
        st.error(f"Erreur : {e}")

    finally:
        agent_capture.arreter()
        if fichier_temp and os.path.exists(fichier_temp):
            os.unlink(fichier_temp)
        st.info("⏹️ Analyse terminée.")
