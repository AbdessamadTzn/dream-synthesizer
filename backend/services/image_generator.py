# backend/services/image_generator.py
import requests
from pathlib import Path
from typing import Dict

def generate_from_main_output(text: str, emotions: Dict[str, float], output_dir: Path) -> str:
    """Génère une image à partir du texte et des émotions du main.py"""
    # 1. Trouver l'émotion dominante
    dominant_emotion = max(emotions, key=emotions.get)
    
    # 2. Adapter le style visuel
    styles = {
        "heureux": "style fantastique, couleurs pastel, lumière douce",
        "anxieux": "style sombre, contrastes élevés",
        # Ajoute d'autres styles au besoin
    }
    
    # 3. Construire le prompt optimisé
    prompt = (
        f"Illustration de rêve {dominant_emotion} (intensité: {emotions[dominant_emotion]:.0%}), "
        f"{styles.get(dominant_emotion, 'style onirique')}, "
        f"Scène: {text}"
    )
    
    # 4. Appel API (Pollinations)
    try:
        response = requests.get(f"https://image.pollinations.ai/prompt/{prompt}", timeout=10)
        response.raise_for_status()
        
        # 5. Sauvegarde
        output_dir.mkdir(exist_ok=True)
        image_path = output_dir / "dream_visualization.png"
        with open(image_path, "wb") as f:
            f.write(response.content)
            
        return f"Image générée avec succès : {image_path}"
    
    except Exception as e:
        return f"Erreur lors de la génération : {str(e)}"