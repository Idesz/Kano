# KANO 🤖 - Az Autonóm Fejlesztői Ökoszisztéma

A **Kano** egy teljesen autonóm, terminálban futó (CLI) fejlesztői rendszer, amely a "lusta informatikus" tökéletes segédje. Helyetted tanul, kódol, tesztel és menedzseli a projekteket.

## 🚀 Projekt Misszió

- **Funkció:** Autonóm, multi-agent kódoló rendszer.
- **Design:** 'Hacker' stílusú CLI (fekete háttér, zöld betűk).
- **Filozófia:** 'Zero-Cost & Local-First' - kizárólag nyílt forrású technológiák.

## 🏗 Megvalósított Funkciók

### 1. Ponytail Mode: Lazy Senior Dev
A Kano a **Ponytail** filozófiát követi. Mielőtt kódot írna, végigjárja a "Lustaság Létráját" (Laziness Ladder):
1. **YAGNI:** Kell ez? | 2. **DRY:** Van már? | 3. **STDLIB:** Python alap? | 4. **NATIVE:** OS alap? | 5. **DEPS:** Van már csomag? | 6. **MINIMUM:** Legkevesebb kód.

### 2. Integrált Skills Ökoszisztéma (skills.sh inspiráció)
A Kano tartalmazza a [skills.sh](https://www.skills.sh/) legnépszerűbb képességeit:
- **Frontend Designer:** Modern komponensek és design tervezése.
- **Architecture Optimizer:** Kódbázis architektúra elemzés és javítás.
- **Systematic Debugger:** Lépésről lépésre történő hibakeresés és javítási terv.
- **PRD Generator:** Ötletek átalakítása profi termékspecifikációvá.
- **Code Auditor:** Biztonsági elemzés és audit.
- **Network Scanner:** Hálózati felderítés (nmap).
- **Media Fetcher:** YouTube adatok és feliratok kinyerése.
- **Web Browser:** Intelligens webes keresés és tartalomgyűjtés.

### 3. Szelektív Interakciós Protokoll
- **Objektív:** Autonóm végrehajtás.
- **Szubjektív:** UI/UX, kreatív döntések esetén **jóváhagyást kér (y/n)**.

### 4. Autonóm Fejlesztés és Tanulás
- **Self-Healing Coder:** Docker sandboxban validált kódgenerálás.
- **Skill Creator:** Új képességek autonóm létrehozása.
- **Idle Learning:** Háttérben futó tudásbázis építés a `raw_data` mappából.

## 🛠 Technológiai Stack
- **Python 3.11+, Ollama (Llama3, DeepSeek), ChromaDB, Textual, Docker, Nmap.**

## ⚙️ Telepítés és Indítás
1. `pip install -r requirements.txt`
2. `python main.py`

## 📂 Könyvtárszerkezet
- `/agents`: Master, Coder, Control, Ingestor, Scaffold, Security.
- `/skills`: Dinamikus modulok (6+ gyári skill).
- `/core`: Rendszermotor, Memória, Tanulási hurok.
- `/blueprints`: Projekt sablonok.
