# Útmutató és Prompt a másik Jules projekthez

Ez a fájl tartalmazza azt a kész, azonnal használható indító szöveget (System Prompt-ot), amelyet a másik Jules projektben a beszélgetés elején beillesztve a mesterséges intelligencia azonnal megérti a Kano ökoszisztémát, és képes lesz lefejleszteni neked a webes felületet chat sessionökkel és Supabase adatbázis-kapcsolattal.

---

## 🚀 HOGYAN HASZNÁLD? (Lépésről lépésre)

1. **Hozz létre egy új mappát / repót** a weblap projektnek (pl. `kano-web-ui`).
2. **Indítsd el ott a Jules asszisztenst.**
3. **Másold ki és illeszd be az alábbi PROMPT részt** a legelső üzenetként a másik Jules-nak.
4. Jules ez alapján automatikusan elkészíti a projekt struktúráját, a Supabase sémát, a backendet és a látványos frontendet!

---

# 📝 MÁSOLANDÓ PROMPT (A beszélgetés indításához)

```markdown
Szia Jules! Egy új projektbe kezdünk. Egy modern, látványos webes felületet (Dashboard) fogunk építeni a "Kano" nevű autonóm AI ágens rendszeremhez.

Szeretném, ha teljesen önállóan, a legjobb szoftvertervezési elvek szerint építenéd fel ezt az alkalmazást. Az alábbiakban bemutatom a Kano rendszert, a követelményeket és az elvárt funkciókat.

---

### 🤖 1. MI AZ A KANO? (A háttérrendszer struktúrája)
A Kano egy Python-alapú helyi AI rendszer, amely az alábbi főbb komponensekből áll:
- **Model Router (`core/model_router.py`):** Kapcsolódik a helyi Ollama példányhoz, lekéri az elérhető modelleket (pl. llama3, deepseek-coder), és feladattípustól (coding, reasoning, chat) függően kiválasztja a legjobbat.
- **Base Agent & Master Agent (`agents/base_agent.py`):** Definiálja az ágenseket. A Master Agent az orchestrator, a CoderAgent pedig kódolási feladatokat hajt végre.
- **Supabase Integráció (`integrations/base_interfaces.py`):** Egy interfész, amely adatbázis lekérdezéseket (`query_db`) és adatbeszúrásokat (`insert_data`) kezel.

---

### 🎯 2. A WEBLAP FUNKCIONÁLIS KÖVETELMÉNYEI

Olyan webes alkalmazást kell építenünk (pl. Python FastAPI/Flask backend és modern HTML/CSS/JavaScript frontend használatával), amely a következő funkciókat tudja:

#### A) Interaktív Chat Felület
- Egy letisztult, modern csevegőablak, ahol valós időben tudok beszélgetni a Kano AI-jal.
- Markdown formázás támogatása a válaszokban (kódblokkok kiemelése, félkövér szöveg stb.).
- Töltésjelző (Spinner) megjelenítése, amíg az AI generálja a választ.

#### B) Session / Beszélgetés Kezelés (Sidebar)
- Egy bal oldali sáv (Sidebar), ahol láthatóak a korábbi beszélgetések (Session-ök).
- **Új beszélgetés indítása:** egy gomb, ami új session-t hoz létre tiszta történettel.
- **Session-ök mentése és betöltése:** korábbi beszélgetésekre kattintva a chat ablak betölti a hozzá tartozó üzeneteket.
- **Törlés és átnevezés:** a session-ök elnevezhetők és törölhetők legyenek.

#### C) Supabase Adatbázis Integráció (A háttértár)
Az összes beszélgetést, session-t és beállítást egy Supabase PostgreSQL adatbázisban kell tárolni. Készíts egy adatbázis sémát és a hozzátartozó SQL DDLe-ket az alábbi táblákkal:
1.  `sessions`:
    - `id` (UUID, primary key)
    - `title` (text, a beszélgetés címe)
    - `created_at` (timestamp)
2.  `messages`:
    - `id` (UUID, primary key)
    - `session_id` (UUID, foreign key -> sessions.id CASCADE)
    - `sender` (text: 'user' vagy 'ai')
    - `content` (text, az üzenet szövege)
    - `created_at` (timestamp)
3.  `settings`:
    - `key` (text, primary key - pl. 'active_model', 'temperature')
    - `value` (text)

A backendnek közvetlenül a Supabase API-ján vagy Python kliensén (`supabase-py`) keresztül kell kezelnie az adatokat!

#### D) Beállítások Panel (Settings)
- Egy külön fül vagy felugró ablak (Modal), ahol beállíthatóak a következők:
  - **Ollama Modell:** Egy legördülő menü (Dropdown), ami lekéri a Kano Model Routeréből az elérhető helyi modelleket, és kiválaszthatom, melyiket használja az AI a csevegéshez.
  - **Supabase credentials:** mezők a Supabase URL és a Supabase Anon/Service Key beállítására (amelyeket a backend `.env` fájlba ment el).

---

### 🎨 3. STÍLUS ÉS DIZÁJN (UI/UX)
- **Hacker / Dark Mode stílus:** sötét háttér (mélyszürke/fekete), neon zöld (`#00ff66` vagy `#39ff14`) és hideg kék/neon cián kiegészítő színekkel.
- **Letisztult elrendezés:** reszponzív dizájn (mobilbarát is), rácsos elrendezés (CSS Grid/Flexbox).
- **Modern kártyák és finom animációk:** hover effektek a gombokon és finom áttűnések.

---

### 🛠️ Feladatod:
1. **Tervezd meg a projekt struktúráját.**
2. **Írd meg a Supabase SQL sémát**, amit be tudok másolni a Supabase SQL Editorába a táblák létrehozásához.
3. **Készítsd el a Backend kódot** (FastAPI-t javaslok, mert aszinkron és rendkívül gyors). Integráld a meglévő Kano Model Router / Ollama logikát a végpontokba.
4. **Készítsd el a Frontend kódot** (HTML, CSS, és tiszta modern JS, vagy React/Tailwind ha úgy látod jónak).
5. **Írj egy rövid README.md-t** a futtatáshoz és a függőségek telepítéséhez.

Készen állok, kérlek mutasd be az első lépéseket és a javasolt architektúrát!
```
