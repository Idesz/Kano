# KANO 🤖 - Az Autonóm Fejlesztői Ökoszisztéma

A **Kano** egy teljesen autonóm, terminálban futó (CLI) fejlesztői rendszer, amely a "lusta informatikus" tökéletes segédje. Helyetted tanul, kódol, tesztel és menedzseli a projekteket.

## 🚀 Projekt Misszió

- **Funkció:** Autonóm, multi-agent kódoló rendszer.
- **Design:** 'Hacker' stílusú CLI (fekete háttér, zöld betűk).
- **Filozófia:** 'Zero-Cost & Local-First' - kizárólag nyílt forrású technológiák.

## 🛠 Technológiai Stack

- **Nyelv:** Python 3.11+
- **LLM Motor:** [Ollama](https://ollama.com/) (lokális modellek)
- **Memória (RAG):** ChromaDB (lokális vektoradatbázis)
- **Interfész:** Rich & Textual (CLI design)
- **Adatgyűjtés:** yt-dlp, BeautifulSoup/Scrapy
- **Integrációk:** GitHub, Supabase

## 🏗 Architektúra

1.  **Model Router:** Automatikusan választja ki a feladathoz legmegfelelőbb lokális modellt.
2.  **Ügynökök:**
    - `Master Agent`: Az orchestrator, aki vezényli a folyamatokat.
    - `Worker Agents`: Speciális feladatokra (UI, Coder, Repo, Database).
    - `Control Agent`: Tesztelés és minőségellenőrzés.
    - `Ingestor Agent`: Adatgyűjtés és tanulás.
3.  **Skill Registry:** Moduláris képességtár (`/skills`), ahol minden skill saját metaadattal rendelkezik.

## ⚙️ Telepítés és Beállítás

### 1. Előfeltételek: Ollama

A Kano lokális modelleket használ, ehhez szükséged lesz az Ollama-ra:

1.  Töltsd le és telepítsd az [ollama.com](https://ollama.com/) oldalról.
2.  Indítsd el az Ollama-t.
3.  Tölts le alapvető modelleket a kezdéshez:
    ```bash
    ollama pull deepseek-coder
    ollama pull llama3
    ollama pull qwen2
    ```

### 2. Python Környezet

```bash
# Virtuális környezet létrehozása (ajánlott)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Függőségek telepítése
pip install -r requirements.txt
```

### 3. Futtatás Dockerrel (opcionális)

```bash
docker build -t kano .
docker run -it kano
```
*Megjegyzés: Docker esetén győződj meg róla, hogy az Ollama elérhető a konténerből (alapértelmezett beállítás: `host.docker.internal:11434`).*

## 🤖 Használat

Indítás:
```bash
python main.py
```

### Szelektív Interakciós Protokoll
- **Objektív feladatok:** A Kano automatikusan hajtja végre (kódolás, tesztelés).
- **Szubjektív feladatok:** UI/UX és design döntéseknél a Kano megáll és megkérdezi a véleményedet.

## 📂 Struktúra

- `/agents`: Az ügynökök logikája.
- `/core`: A rendszer motorja (Model Router, Orchestrator).
- `/skills`: Dinamikusan betölthető modulok.
- `/integrations`: Külső szolgáltatások (GitHub, Supabase).
- `/ui`: Textual-alapú felhasználói felület.
