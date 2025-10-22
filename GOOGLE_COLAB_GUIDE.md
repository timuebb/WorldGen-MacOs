# Google Colab Guide für WorldGen

Da WorldGen aufgrund der UniK3D/Triton-Abhängigkeit nicht nativ auf macOS funktioniert, ist **Google Colab** die einfachste Alternative für macOS-Nutzer.

## 🚀 Schnellstart

### 1. Google Colab öffnen

Gehe zu [https://colab.research.google.com](https://colab.research.google.com) und erstelle ein neues Notebook.

### 2. GPU aktivieren

**Wichtig**: Stelle sicher, dass eine GPU aktiviert ist:

1. Klicke auf `Runtime` → `Change runtime type`
2. Wähle `Hardware accelerator`: **GPU** (T4, A100, oder V100)
3. Klicke auf `Save`

### 3. Installation in Colab

Kopiere diese Zellen in dein Colab Notebook:

#### Zelle 1: Repository klonen und installieren

```python
# Repository klonen
!git clone https://github.com/ZiYang-xie/WorldGen.git
%cd WorldGen

# WorldGen installieren
!pip install -q .

print("✅ Installation abgeschlossen!")
```

#### Zelle 2: GPU überprüfen

```python
import torch

# GPU-Status prüfen
if torch.cuda.is_available():
    print(f"✅ GPU verfügbar: {torch.cuda.get_device_name(0)}")
    print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
else:
    print("❌ Keine GPU verfügbar - bitte Runtime-Typ ändern!")
```

## 📝 Verwendung

### Text-to-Scene Generation

```python
from worldgen import WorldGen
from PIL import Image

# WorldGen initialisieren (mit GPU)
worldgen = WorldGen(mode="t2s", device="cuda")

# Szene generieren
print("🌍 Generiere Szene...")
scene = worldgen.generate_world(
    prompt="A beautiful mountain landscape with a crystal clear lake"
)

# Als PLY-Datei speichern
scene.save("my_scene.ply")
print("✅ Szene gespeichert als 'my_scene.ply'")

# Datei herunterladen
from google.colab import files
files.download("my_scene.ply")
```

### Image-to-Scene Generation

```python
from worldgen import WorldGen
from PIL import Image

# Bild hochladen
from google.colab import files
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

# Bild laden
image = Image.open(image_path).convert("RGB")

# WorldGen im Image-to-Scene Modus
worldgen = WorldGen(mode="i2s", device="cuda")

# Szene aus Bild generieren
print("🌍 Generiere Szene aus Bild...")
scene = worldgen.generate_world(
    prompt="expand this scene into a full 360 environment",
    image=image
)

# Speichern und herunterladen
scene.save("scene_from_image.ply")
from google.colab import files
files.download("scene_from_image.ply")
```

### Demo mit Visualisierung

```python
# Demo-Server starten (erfordert Port-Forwarding)
!python demo.py -p "A cozy cabin in the snowy mountains"

# Hinweis: In Colab ist die Visualisierung begrenzt
# Die PLY-Datei kann in lokalen Tools wie MeshLab oder CloudCompare geöffnet werden
```

## 📦 Dateien verwalten

### Dateien hochladen

```python
from google.colab import files

# Einzelne Datei hochladen
uploaded = files.upload()

# Mehrere Bilder hochladen
print("Wähle deine Bilder aus:")
uploaded = files.upload()
```

### Dateien herunterladen

```python
from google.colab import files

# Einzelne Datei
files.download("my_scene.ply")

# Alle generierten Szenen
import os
for file in os.listdir("output"):
    if file.endswith(".ply"):
        files.download(f"output/{file}")
```

### Mit Google Drive arbeiten

```python
# Google Drive mounten
from google.colab import drive
drive.mount('/content/drive')

# Szene direkt in Drive speichern
scene.save("/content/drive/MyDrive/WorldGen/my_scene.ply")
```

## ⚙️ Erweiterte Optionen

### Mit verschiedenen Auflösungen

```python
# Höhere Auflösung (mehr VRAM benötigt)
worldgen = WorldGen(mode="t2s", device="cuda", resolution=2048)

# Niedrigere Auflösung (weniger VRAM)
worldgen = WorldGen(mode="t2s", device="cuda", resolution=1024)
```

### Low VRAM Modus

```python
# Automatische VRAM-Erkennung
worldgen = WorldGen(mode="t2s", device="cuda", low_vram=True)
```

### Batch-Generierung

```python
prompts = [
    "A futuristic city at sunset",
    "A tropical beach with palm trees",
    "A snowy mountain peak",
    "A medieval castle on a hill"
]

scenes = []
for i, prompt in enumerate(prompts):
    print(f"Generiere Szene {i+1}/{len(prompts)}: {prompt}")
    scene = worldgen.generate_world(prompt=prompt)
    filename = f"scene_{i+1}.ply"
    scene.save(filename)
    scenes.append(filename)
    print(f"✅ Gespeichert als {filename}")

# Alle herunterladen
from google.colab import files
for scene_file in scenes:
    files.download(scene_file)
```

## 🎯 Vollständiges Beispiel-Notebook

Hier ist ein komplettes, sofort nutzbares Notebook:

```python
# =============================================================================
# WorldGen auf Google Colab - Vollständiges Beispiel
# =============================================================================

# 1. Installation
print("📦 Installiere WorldGen...")
!git clone https://github.com/ZiYang-xie/WorldGen.git
%cd WorldGen
!pip install -q .

# 2. GPU Check
import torch
print(f"\n🔍 GPU-Status:")
if torch.cuda.is_available():
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
else:
    print("❌ Keine GPU! Bitte Runtime ändern.")
    
# 3. Szene generieren
from worldgen import WorldGen

print("\n🌍 Initialisiere WorldGen...")
worldgen = WorldGen(mode="t2s", device="cuda")

print("\n🎨 Generiere Szene...")
scene = worldgen.generate_world(
    prompt="A serene Japanese garden with cherry blossoms and a koi pond"
)

# 4. Speichern
scene.save("japanese_garden.ply")
print("\n✅ Szene generiert und gespeichert!")

# 5. Herunterladen
from google.colab import files
files.download("japanese_garden.ply")
print("\n📥 Download gestartet!")
```

## 💡 Tipps & Tricks

### 1. VRAM sparen

```python
# Nach jeder Generierung VRAM freigeben
import torch
torch.cuda.empty_cache()
```

### 2. Generierungszeit überwachen

```python
import time

start = time.time()
scene = worldgen.generate_world(prompt="Your prompt here")
elapsed = time.time() - start

print(f"⏱️ Generierung dauerte {elapsed/60:.1f} Minuten")
```

### 3. Fehlerbehandlung

```python
try:
    scene = worldgen.generate_world(prompt="Your prompt")
    scene.save("output.ply")
    print("✅ Erfolgreich generiert!")
except Exception as e:
    print(f"❌ Fehler: {e}")
    # VRAM freigeben und erneut versuchen
    torch.cuda.empty_cache()
```

### 4. Mehrere Varianten generieren

```python
prompt = "A fantasy castle on a floating island"

for i in range(3):
    print(f"\nGeneriere Variante {i+1}/3...")
    scene = worldgen.generate_world(prompt=prompt)
    scene.save(f"castle_variant_{i+1}.ply")
    torch.cuda.empty_cache()  # VRAM freigeben
```

## ⚠️ Häufige Probleme

### Problem: "CUDA out of memory"

**Lösung**:
```python
# VRAM freigeben
import torch
torch.cuda.empty_cache()

# Mit niedrigerer Auflösung erneut versuchen
worldgen = WorldGen(mode="t2s", device="cuda", resolution=1024)
```

### Problem: "Runtime disconnected"

**Lösung**: Colab hat Zeitlimits. Bei langen Generierungen:
- Verwende Colab Pro für längere Laufzeiten
- Speichere Zwischenergebnisse regelmäßig in Google Drive
- Teile große Aufgaben in kleinere Schritte

### Problem: Langsame Generierung

**Lösung**:
- Stelle sicher, dass GPU aktiviert ist (nicht TPU!)
- Prüfe, ob `low_vram=True` gesetzt ist
- Verwende `resolution=1024` statt höherer Auflösungen

## 📊 Performance-Übersicht

| GPU-Typ | VRAM | Typische Generierungszeit | Empfohlene Auflösung |
|---------|------|--------------------------|---------------------|
| T4 (Free Tier) | 15 GB | 10-15 Min | 1024-1600 |
| A100 (Colab Pro) | 40 GB | 3-5 Min | 1600-2048 |
| V100 (Colab Pro) | 16 GB | 6-10 Min | 1024-1600 |

## 🔗 Zusätzliche Ressourcen

- **WorldGen Repository**: https://github.com/ZiYang-xie/WorldGen
- **Google Colab Docs**: https://colab.research.google.com/notebooks/intro.ipynb
- **Colab Pro**: https://colab.research.google.com/signup

## 📝 Zusammenfassung

Google Colab ist die **beste Lösung** für macOS-Nutzer:

✅ **Vorteile**:
- Kostenlose NVIDIA GPUs
- Keine lokale Installation nötig
- Einfach zu nutzen
- Funktioniert direkt im Browser

⚠️ **Nachteile**:
- Zeitlimit (Colab Free: ~12 Std, Pro: 24 Std)
- Dateien müssen heruntergeladen werden
- Internet-Verbindung erforderlich

**Empfehlung**: Für gelegentliche Nutzung ist der kostenlose Tier ausreichend. Für intensive Nutzung lohnt sich Colab Pro.
