# KANO 🤖 - Az Autonóm Fejlesztői Ökoszisztéma

A **Kano** egy teljesen autonóm, terminálban futó (CLI) fejlesztői rendszer, amely a "lusta informatikus" tökéletes segédje. Helyetted tanul, kódol, tesztel és menedzseli a projekteket.

## 🚀 Projekt Misszió

- **Funkció:** Autonóm, multi-agent kódoló rendszer.
- **Design:** 'Hacker' stílusú CLI (fekete háttér, zöld betűk).
- **Filozófia:** 'Zero-Cost & Local-First' - kizárólag nyílt forrású technológiák.

## 🏗 Megvalósított Funkciók

### 1. Szelektív Interakciós Protokoll (Kiemelt!)
- **Objektív feladatok:** Automatikus végrehajtás (kódolás, algoritmusok, adatkezelés).
- **Szubjektív feladatok:** UI/UX, színek, kreatív döntések esetén a rendszer megáll, alternatívákat mutat és **jóváhagyást kér (y/n)**.

### 2. Autonóm Fejlesztés és Tanulás
- **Self-Healing Coder:** Docker sandboxban validált kódgenerálás automatikus `pytest` tesztekkel.
- **Skill Creator:** Kano képes felismerni, ha hiányzik egy képessége, és autonóm módon megírja/regisztrálja az új Skill-t.
- **Idle Learning:** Amikor nem használd, a Kano a `raw_data` mappából tanul, összegez és vektorizál a memóriájába.
- **Scaffold Agent:** Komplett projektvázak generálása (pl. FastAPI + Supabase).

### 3. Intelligens Adatgyűjtés
- **Ingestor:** Automatikus URL felismerés. A YouTube linkeket magától a `media_fetcher` skillhez irányítja.
- **RAG Memória:** ChromaDB alapú tudásbázis a gyűjtött adatokhoz.

## 🛠 Technológiai Stack
- **Python 3.11+, Ollama (Llama3, DeepSeek), ChromaDB, Textual, Docker, BeautifulSoup, yt-dlp.**

## ⚙️ Telepítés és Indítás
1.  **Ollama & Docker** legyen telepítve és fusson.
2.  `pip install -r requirements.txt`
3.  `python main.py`

## 📂 Könyvtárszerkezet
- `/agents`: Master, Coder, Control, Ingestor, Scaffold.
- `/skills`: Dinamikus modulok (file, web, media).
- `/core`: Rendszermotor, Memória, Tanulási hurok.
- `/raw_data`: Nyers adatok helye.
- `/blueprints`: Projekt sablonok.
