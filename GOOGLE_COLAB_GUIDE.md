# WorldGen auf Google Colab nutzen

Diese Anleitung zeigt dir, wie du **WorldGen** in Google Colab verwenden kannst, um 3D-Szenen aus Text oder Bildern zu generieren.

## Systemanforderungen

WorldGen benötigt:
- Python 3.11 oder höher (Google Colab verwendet Python 3.12)
- CUDA-fähige GPU (empfohlen: mindestens 12GB VRAM, funktioniert auch mit weniger im Low-VRAM-Modus)
- Ubuntu/Linux-Umgebung (Google Colab verwendet Ubuntu 22.04)

⚠️ **Hinweis**: Google Colab bietet kostenlose GPU-Zugriff, aber die verfügbare VRAM kann variieren. Verwende den `low_vram=True` Modus, wenn du Speicherprobleme hast.

## Schritt 1: Notebook-Umgebung einrichten

Erstelle ein neues Google Colab Notebook und wähle eine GPU-Runtime:
1. Gehe zu `Runtime` → `Change runtime type`
2. Wähle `GPU` als Hardware accelerator
3. Klicke auf `Save`

## Schritt 2: Repository klonen

```python
# Repository klonen
!git clone https://github.com/ZiYang-xie/WorldGen.git
%cd WorldGen
```

## Schritt 3: Abhängigkeiten installieren

⚠️ **Wichtig für Python 3.12 (Google Colab)**: Da Google Colab Python 3.12 verwendet und das WorldGen-Repository eine Python 3.11-Version von nunchaku spezifiziert, musst du nunchaku manuell installieren, bevor du WorldGen installierst.

```python
# PyTorch mit CUDA-Unterstützung installieren
# Für Google Colab mit CUDA 12.x
!pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# WICHTIG: Nunchaku manuell für Python 3.12 installieren
# Dies muss VOR der WorldGen-Installation erfolgen
!pip install https://github.com/mit-han-lab/nunchaku/releases/download/v0.2.0/nunchaku-0.2.0+torch2.8-cp312-cp312-linux_x86_64.whl

# WorldGen installieren (ohne nunchaku-Abhängigkeit)
!pip install --no-deps .

# Alle anderen Abhängigkeiten installieren
!pip install diffusers>=0.33.1 xformers>=0.0.30 transformers>=4.48.3 py360convert>=0.1.0 einops>=0.7.0 pillow>=8.0.0 scikit-image>=0.24.0 sentencepiece>=0.2.0 peft>=0.7.1 open3d>=0.19.0 trimesh>=4.6.1
!pip install git+https://github.com/ZiYang-xie/viser.git
!pip install git+https://github.com/lpiccinelli-eth/UniK3D.git

# Optional: Für Background-Inpainting (experimentell)
# !pip install iopaint --no-dependencies
```

## Schritt 4: GPU-Verfügbarkeit prüfen

```python
import torch

print(f"CUDA verfügbar: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA Version: {torch.version.cuda}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
```

## Schritt 5: WorldGen verwenden

### Option A: Text zu 3D-Szene (Text-to-Scene)

```python
from worldgen import WorldGen
import torch

# Device einrichten
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# WorldGen initialisieren (Low-VRAM Modus für GPUs mit weniger als 24GB VRAM)
worldgen = WorldGen(mode="t2s", device=device, low_vram=True)

# 3D-Szene generieren
prompt = "A beautiful landscape with a river and mountains"
splat = worldgen.generate_world(prompt)

# Szene speichern
splat.save("output_scene.ply")

print("✅ 3D-Szene erfolgreich generiert und gespeichert als 'output_scene.ply'")
```

### Option B: Bild zu 3D-Szene (Image-to-Scene)

```python
from worldgen import WorldGen
from PIL import Image
import torch

# Device einrichten
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# WorldGen initialisieren
worldgen = WorldGen(mode="i2s", device=device, low_vram=True)

# Bild laden (ersetze mit deinem Bildpfad)
# Du kannst Bilder hochladen mit: files.upload() aus google.colab
image = Image.open("path/to/your/image.jpg")

# 3D-Szene aus Bild generieren
splat = worldgen.generate_world(
    image=image,
    prompt="Optional: Beschreibung der Szene"
)

# Szene speichern
splat.save("output_scene.ply")

print("✅ 3D-Szene erfolgreich generiert!")
```

### Option C: Mesh-Generierung

```python
from worldgen import WorldGen
import torch
import open3d as o3d

# Device einrichten
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# WorldGen initialisieren
worldgen = WorldGen(mode="t2s", device=device, low_vram=True)

# 3D-Mesh generieren
prompt = "A cozy living room with furniture"
mesh = worldgen.generate_world(prompt, return_mesh=True)

# Mesh speichern
o3d.io.write_triangle_mesh("output_mesh.ply", mesh)

print("✅ 3D-Mesh erfolgreich generiert und gespeichert als 'output_mesh.ply'")
```

## Schritt 6: Bilder in Google Colab hochladen

Um eigene Bilder für die Image-to-Scene Generierung zu verwenden:

```python
from google.colab import files
from PIL import Image
import io

# Bild hochladen
uploaded = files.upload()

# Erstes hochgeladenes Bild laden
for filename in uploaded.keys():
    image = Image.open(io.BytesIO(uploaded[filename]))
    print(f"Bild geladen: {filename}")
    break
```

## Schritt 7: Generierte Dateien herunterladen

```python
from google.colab import files

# PLY-Datei herunterladen
files.download('output_scene.ply')

# Oder alle Ausgabedateien herunterladen
# files.download('output_mesh.ply')
```

## Vollständiges Beispiel-Notebook

Hier ist ein vollständiges Beispiel, das alle Schritte kombiniert:

```python
# 1. Repository klonen und installieren
!git clone https://github.com/ZiYang-xie/WorldGen.git
%cd WorldGen

# 2. Abhängigkeiten installieren
!pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# WICHTIG: Nunchaku manuell für Python 3.12 installieren
!pip install https://github.com/mit-han-lab/nunchaku/releases/download/v0.2.0/nunchaku-0.2.0+torch2.8-cp312-cp312-linux_x86_64.whl

# WorldGen und restliche Abhängigkeiten installieren
!pip install --no-deps .
!pip install diffusers>=0.33.1 xformers>=0.0.30 transformers>=4.48.3 py360convert>=0.1.0 einops>=0.7.0 pillow>=8.0.0 scikit-image>=0.24.0 sentencepiece>=0.2.0 peft>=0.7.1 open3d>=0.19.0 trimesh>=4.6.1
!pip install git+https://github.com/ZiYang-xie/viser.git
!pip install git+https://github.com/lpiccinelli-eth/UniK3D.git

# 3. WorldGen verwenden
import torch
from worldgen import WorldGen

# GPU prüfen
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

if torch.cuda.is_available():
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"GPU VRAM: {vram_gb:.2f} GB")
    low_vram = vram_gb < 24
else:
    low_vram = True

# WorldGen initialisieren
worldgen = WorldGen(mode="t2s", device=device, low_vram=low_vram)

# Szene generieren
prompt = "A beautiful beach at sunset with palm trees"
print(f"Generating scene: {prompt}")
splat = worldgen.generate_world(prompt)

# Speichern
splat.save("beach_scene.ply")
print("✅ Scene generated successfully!")

# Herunterladen
from google.colab import files
files.download('beach_scene.ply')
```

## Tipps und Fehlerbehebung

### Low-VRAM Modus
Wenn du Out-of-Memory Fehler erhältst, verwende:
```python
worldgen = WorldGen(mode="t2s", device=device, low_vram=True)
```

### Python 3.12 Kompatibilitätsproblem beheben

**Problem**: Beim Ausführen von `!pip install .` in Google Colab erhältst du den Fehler:
```
ERROR: nunchaku-0.2.0+torch2.7-cp311-cp311-linux_x86_64.whl is not a supported wheel on this platform.
```

**Ursache**: Das WorldGen-Repository enthält eine Abhängigkeit zu nunchaku für Python 3.11, aber Google Colab verwendet Python 3.12.

**Lösung in Colab**: Installiere nunchaku manuell vor der WorldGen-Installation:

```python
# Schritt 1: Nunchaku für Python 3.12 installieren
!pip install https://github.com/mit-han-lab/nunchaku/releases/download/v0.2.0/nunchaku-0.2.0+torch2.8-cp312-cp312-linux_x86_64.whl

# Schritt 2: WorldGen ohne Abhängigkeiten installieren
!pip install --no-deps .

# Schritt 3: Restliche Abhängigkeiten installieren
!pip install diffusers>=0.33.1 xformers>=0.0.30 transformers>=4.48.3 py360convert>=0.1.0 einops>=0.7.0 pillow>=8.0.0 scikit-image>=0.24.0 sentencepiece>=0.2.0 peft>=0.7.1 open3d>=0.19.0 trimesh>=4.6.1
!pip install git+https://github.com/ZiYang-xie/viser.git
!pip install git+https://github.com/lpiccinelli-eth/UniK3D.git
```

Dieser Workaround stellt sicher, dass die richtige Version von nunchaku für Python 3.12 verwendet wird, ohne dass Änderungen am Repository-Code erforderlich sind.

### Dependency Conflicts Warnung (kann ignoriert werden)

**Warnung während der Installation**:
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
worldgen 0.1.0 requires UniK3D@ git+https://github.com/lpiccinelli-eth/UniK3D.git, which is not installed.
```

**Erklärung**: Diese Warnung erscheint, weil wir die Abhängigkeiten in mehreren Schritten installieren (zuerst `viser`, dann `UniK3D`). Pip zeigt diese Warnung an, bevor `UniK3D` installiert wird.

**Lösung**: Diese Warnung kann **ignoriert** werden. Solange die Installation mit `!pip install git+https://github.com/lpiccinelli-eth/UniK3D.git` erfolgreich fortgesetzt wird, ist alles in Ordnung. Die Warnung verschwindet, sobald alle Abhängigkeiten installiert sind.

**Überprüfung**: Nach der vollständigen Installation kannst du prüfen, ob alle Pakete korrekt installiert wurden:
```python
import worldgen
import UniK3D
print("✅ Alle Pakete erfolgreich installiert!")
```

### KNN Kompilierungs-Warnung (kann ignoriert werden)

**Warnung beim ersten Ausführen**:
```
/usr/local/lib/python3.12/dist-packages/unik3d/utils/chamfer_distance.py:9: UserWarning: !! To run evaluation you need KNN. Please compile KNN: `cd unik3d/ops/knn && bash compile.sh`.
```

**Erklärung**: Diese Warnung erscheint beim ersten Import von WorldGen. KNN (K-Nearest Neighbors) wird nur für Evaluierungszwecke benötigt, nicht für die Szenen-Generierung.

**Lösung**: Diese Warnung kann **ignoriert** werden. WorldGen funktioniert vollständig ohne KNN-Kompilierung. Die Generierung von 3D-Szenen ist nicht betroffen.

Falls du KNN benötigst (nur für fortgeschrittene Evaluation), kannst du es in Colab kompilieren:
```python
# Optional: Nur wenn KNN wirklich benötigt wird
!cd /usr/local/lib/python3.12/dist-packages/unik3d/ops/knn && bash compile.sh
```

**Hinweis**: Für normale Nutzung ist dies nicht erforderlich.

### ModuleNotFoundError beheben

**Problem**: Beim Ausführen von `worldgen.generate_world()` erhältst du einen `ModuleNotFoundError`.

**Mögliche Ursachen und Lösungen**:

1. **Neustart der Runtime erforderlich**: Nach der Installation aller Pakete musst du möglicherweise die Colab Runtime neu starten:
   - Gehe zu `Runtime` → `Restart runtime`
   - Führe dann nur den Code-Block mit der WorldGen-Nutzung aus (ohne die Installationsbefehle)

2. **Fehlende Abhängigkeit**: Stelle sicher, dass alle Installationsschritte erfolgreich abgeschlossen wurden:
```python
# Überprüfe, ob alle wichtigen Module importiert werden können
try:
    import torch
    import diffusers
    import transformers
    import UniK3D
    import worldgen
    print("✅ Alle Module erfolgreich importiert!")
except ImportError as e:
    print(f"❌ Fehlendes Modul: {e}")
```

3. **Installation wiederholen**: Falls Module fehlen, führe die Installation erneut aus:
```python
!pip install diffusers>=0.33.1 xformers>=0.0.30 transformers>=4.48.3 py360convert>=0.1.0 einops>=0.7.0 pillow>=8.0.0 scikit-image>=0.24.0 sentencepiece>=0.2.0 peft>=0.7.1 open3d>=0.19.0 trimesh>=4.6.1
!pip install git+https://github.com/ZiYang-xie/viser.git
!pip install git+https://github.com/lpiccinelli-eth/UniK3D.git
```

### Speicherplatz prüfen
```python
!df -h
```

### VRAM-Nutzung überwachen
```python
!nvidia-smi
```

### Verschiedene Auflösungen
```python
# Niedrigere Auflösung für schnellere Generierung
worldgen = WorldGen(mode="t2s", device=device, low_vram=True, resolution=1024)

# Höhere Auflösung für bessere Qualität (benötigt mehr VRAM)
worldgen = WorldGen(mode="t2s", device=device, low_vram=False, resolution=2048)
```

### Experimentelles Background Inpainting
```python
# Installiere iopaint
!pip install iopaint --no-dependencies

# Verwende mit inpaint_bg=True
worldgen = WorldGen(mode="t2s", device=device, low_vram=True, inpaint_bg=True)
```

## Ausgabedateien

- **PLY-Dateien**: Können mit 3D-Viewing-Software wie:
  - [Polycam](https://poly.cam/) (Web-basiert)
  - [MeshLab](https://www.meshlab.net/)
  - [CloudCompare](https://www.cloudcompare.org/)
  - Gaussian Splatting Viewern
  - Blender

## Bekannte Einschränkungen auf Google Colab

1. **Session-Zeitlimit**: Google Colab Free hat ein 12-Stunden-Zeitlimit
2. **VRAM-Variabilität**: Die verfügbare GPU kann variieren (T4, P100, V100)
3. **Speicherplatz**: ~100GB auf Google Colab Free
4. **Keine persistente Speicherung**: Dateien gehen verloren, wenn die Session endet
   - Verwende Google Drive oder lade Dateien herunter

## Google Drive Integration (Optional)

Um Ausgaben dauerhaft zu speichern:

```python
from google.colab import drive
drive.mount('/content/drive')

# Speichere in Google Drive
splat.save('/content/drive/MyDrive/worldgen_outputs/scene.ply')
```

## Weitere Ressourcen

- [WorldGen GitHub Repository](https://github.com/ZiYang-xie/WorldGen)
- [WorldGen Project Page](https://worldgen.github.io/)
- [Hugging Face Model](https://huggingface.co/LeoXie/WorldGen)

## Kontakt

Bei Fragen oder Problemen:
- GitHub Issues: https://github.com/ZiYang-xie/WorldGen/issues
- Email: ziyangxie01@gmail.com

---

**Viel Erfolg bei der 3D-Szenen-Generierung! 🌍✨**
