# KANO 🤖 - Az Autonóm Fejlesztői Ökoszisztéma

A **Kano** egy teljesen autonóm, terminálban futó (CLI) fejlesztői rendszer, amely a "lusta informatikus" tökéletes segédje. Helyetted tanul, kódol, tesztel és menedzseli a projekteket.

## 🚀 Projekt Misszió

- **Funkció:** Autonóm, multi-agent kódoló rendszer.
- **Design:** 'Hacker' stílusú CLI (fekete háttér, zöld betűk).
- **Filozófia:** 'Zero-Cost & Local-First' - kizárólag nyílt forrású technológiák.

## 🏗 Megvalósított Funkciók

### 1. Security & Pentesting (ÚJ!)
- **Security Agent:** PentestGPT-stílusú érvelés és támadási tervek generálása.
- **Code Auditor:** Automatikus biztonsági elemzés (SQLi, hardkódolt titkok, eval() használata).
- **Network Scanner:** Nmap alapú hálózati szkennelés és szolgáltatásfelderítés.

### 2. Szelektív Interakciós Protokoll
- **Objektív feladatok:** Automatikus végrehajtás (kódolás, algoritmusok, adatkezelés).
- **Szubjektív feladatok:** UI/UX, színek, kreatív döntések esetén a rendszer megáll és **jóváhagyást kér (y/n)**.

### 3. Autonóm Fejlesztés és Tanulás
- **Self-Healing Coder:** Docker sandboxban validált kódgenerálás automatikus `pytest` tesztekkel.
- **Skill Creator:** Kano képes felismerni, ha hiányzik egy képessége, és autonóm módon megírja/regisztrálja az új Skill-t.
- **Idle Learning:** Amikor nem használd, a Kano a `raw_data` mappából tanul, összegez és vektorizál a memóriájába.
- **Scaffold Agent:** Komplett projektvázak generálása (pl. FastAPI + Supabase).

### 4. Intelligens Adatgyűjtés
- **Ingestor:** Automatikus URL felismerés. A YouTube linkeket magától a `media_fetcher` skillhez irányítja.

## 🛠 Technológiai Stack
- **Python 3.11+, Ollama (Llama3, DeepSeek), ChromaDB, Textual, Docker, Nmap, BeautifulSoup, yt-dlp.**

## ⚙️ Telepítés és Indítás
1.  **Ollama, Docker & Nmap** legyen telepítve és fusson.
2.  `pip install -r requirements.txt`
3.  `python main.py`

## 📂 Könyvtárszerkezet
- `/agents`: Master, Coder, Control, Ingestor, Scaffold, **Security**.
- `/skills`: Dinamikus modulok (file, web, media, **security audit, network scan**).
- `/core`: Rendszermotor, Memória, Tanulási hurok.
- `/raw_data`: Nyers adatok helye.
- `/blueprints`: Projekt sablonok.
