#!/usr/bin/env python3
"""
Script pour générer des fichiers audio de test pour l'application Synthétiseur de rêves.
Crée des échantillons audio avec différentes émotions pour tester les services.
"""

import os
from gtts import gTTS
from pathlib import Path
import json

# Config routes
AUDIO_DIR = Path("data/audio/samples")
METADATA_FILE = AUDIO_DIR / "metadata.json"

REVES_SAMPLES = {
    "heureux": [
        {
            "text": "J'ai rêvé que je volais au-dessus d'un magnifique lac cristallin. Les rayons du soleil dansaient sur l'eau et je me sentais complètement libre. Des oiseaux colorés volaient à mes côtés en chantant une mélodie joyeuse.",
            "emotion": "heureux",
            "intensite": 0.8
        },
        {
            "text": "Dans mon rêve, je retrouvais tous mes amis d'enfance dans un jardin extraordinaire rempli de fleurs qui brillaient comme des diamants. Nous riions aux éclats et dansions sous une pluie d'étoiles filantes.",
            "emotion": "heureux",
            "intensite": 0.9
        }
    ],
    "stressant": [
        {
            "text": "J'étais poursuivi dans un labyrinthe sombre et sans fin. Mes jambes devenaient de plus en plus lourdes et je n'arrivais pas à courir assez vite. J'entendais des bruits étranges derrière moi qui se rapprochaient.",
            "emotion": "stressant",
            "intensite": 0.7
        },
        {
            "text": "Je me trouvais dans un ascenseur qui montait à une vitesse vertigineuse. Les boutons ne répondaient plus et l'ascenseur ne s'arrêtait jamais. J'avais l'impression que j'allais être projeté dans l'espace.",
            "emotion": "stressant",
            "intensite": 0.8
        }
    ],
    "neutre": [
        {
            "text": "Je me promenais dans une ville que je ne connaissais pas. Les rues étaient calmes et les bâtiments avaient une architecture simple. J'observais les gens passer sans vraiment interagir avec eux.",
            "emotion": "neutre",
            "intensite": 0.3
        },
        {
            "text": "J'étais dans une bibliothèque silencieuse en train de lire un livre dont je ne me souviens plus du titre. L'atmosphère était paisible et je feuilletais les pages tranquillement.",
            "emotion": "neutre",
            "intensite": 0.2
        }
    ],
    "bizarre": [
        {
            "text": "Les objets de ma maison parlaient entre eux quand je n'étais pas là. Mon frigo négociait avec le micro-ondes pour savoir qui allait réchauffer mon dîner. C'était absurde mais parfaitement logique dans le rêve.",
            "emotion": "bizarre",
            "intensite": 0.6
        }
    ]
}

def create_directories():
    """Crée les répertoires nécessaires s'ils n'existent pas."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Répertoire créé : {AUDIO_DIR}")

def generate_audio_file(text, filename, emotion):
    """Génère un fichier audio à partir du texte."""
    try:
        tts = gTTS(text=text, lang='fr', slow=False)
        filepath = AUDIO_DIR / f"{filename}.mp3"
        tts.save(str(filepath))
        print(f"Généré : {filename}.mp3 ({emotion})")
        return True
    except Exception as e:
        print(f"Erreur lors de la génération de {filename}: {e}")
        return False

def create_metadata(samples_info):
    metadata = {
        "description": "Échantillons audio pour tests du Synthétiseur de rêves",
        "total_files": len(samples_info),
        "emotions": list(set(info["emotion"] for info in samples_info)),
        "samples": samples_info
    }
    
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Métadonnées sauvegardées : {METADATA_FILE}")

def main():
    """Fonction principale pour générer tous les échantillons."""
    print("Génération des échantillons audio...")
    print("=" * 50)
    
    # Créer les répertoires
    create_directories()
    
    # Générer les fichiers audio
    samples_info = []
    total_generated = 0
    
    for emotion, reves in REVES_SAMPLES.items():
        print(f"\nGénération des rêves {emotion}...")
        
        for i, reve in enumerate(reves, 1):
            filename = f"reve_{emotion}_{i:02d}"
            
            if generate_audio_file(reve["text"], filename, emotion):
                samples_info.append({
                    "filename": f"{filename}.mp3",
                    "emotion": emotion,
                    "text": reve["text"],
                    "intensite": reve["intensite"],
                    "duree_estimee": len(reve["text"]) / 10  # Estimation grossière
                })
                total_generated += 1
    
    # Créer le fichier de métadonnées
    create_metadata(samples_info)
    
    print("\n" + "=" * 50)
    print(f"Génération terminée : {total_generated} fichiers créés")
    print(f"Fichiers sauvegardés dans : {AUDIO_DIR}")
    
    # Afficher un résumé
    print("\nRésumé des émotions :")
    for emotion in set(info["emotion"] for info in samples_info):
        count = sum(1 for info in samples_info if info["emotion"] == emotion)
        print(f"   {emotion}: {count} fichier(s)")

if __name__ == "__main__":
    main()