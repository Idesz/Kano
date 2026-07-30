# KANO 🚀 - Gyors Telepítési Útmutató Render.com-ra

Ezzel az útmutatóval a Kanót **10 percen belül, teljesen ingyen** elindíthatod a felhőben (Render.com), akár helyi gép nélkül is!

---

### 1. Előfeltételek (2 perc)
1.  Készíts egy ingyenes, **privát** GitHub repót, és töltsd fel oda a Kano projekt kódját.
2.  Menj a [console.groq.com](https://console.groq.com/) oldalra, regisztrálj és hozz létre egy ingyenes **Groq API Key**-t.

---

### 2. Telepítés a Render.com-ra (5 perc)
1.  Regisztrálj a [render.com](https://render.com/) oldalon a GitHub fiókoddal.
2.  A dashboardon kattints a **New +** -> **Web Service** gombra.
3.  Válaszd ki a Kano GitHub repódat.
4.  **Beállítások:**
    *   **Name:** `kano-system`
    *   **Region:** Válaszd a legközelebbit (pl. Frankfurt).
    *   **Language:** `Docker` (A Render automatikusan látni fogja a `Dockerfile`-t).
    *   **Instance Type:** `Free` (Teljesen ingyenes szint).
5.  Kattints az **Advanced** gombra, majd az **Add Environment Variable** gombra, és add meg az alábbiakat:
    *   `KANO_API_KEY` = *Egy tetszőleges, erős jelszó a Kano eléréséhez.*
    *   `GROQ_API_KEY` = *A Groq-tól kapott ingyenes kulcsod.*
    *   `DOCKER_IMAGE` = `python:3.11-slim`
6.  Kattints a **Create Web Service** gombra!

A Render elkezdi építeni a konténert. Kb. 3-5 perc múlva a Kano éles és fut! A Render ad neked egy egyedi linket (pl. `https://kano-system.onrender.com`).

---

### 3. Használat és Csatlakozás (3 perc)

Mivel a felhőben futó Kanót az **API Gateway**-en keresztül tudod irányítani, a legegyszerűbb, ha a saját gépedről egy paranccsal küldesz neki feladatokat:

#### Példa feladat küldése:
Írd be a terminálodba (helyettesítsd be a saját Render-linkedet és az API kulcsodat):
```bash
curl -X POST https://kano-system.onrender.com/execute \
  -H "X-KANO-API-KEY: a_te_jelszavad" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate a clean python function to scrape weather data"}'
```

#### Hogyan működik a Hybrid intelligencia?
-   Ha a Kano érzékeli, hogy nincs helyi Ollama (mivel a Renderen fut), **automatikusan átvált a Groq felhős API-jára**, ami elképesztő sebességgel (akár 100+ token/másodperc) hajtja végre a kéréseket.
-   Ha később otthon elindítod a saját Ollama-dat és az ngrok alagutat, a Kano magától visszaáll a helyi modellek futtatására!

---

### 🎉 KÉSZ VAGYUNK!
A Kanód mostantól 24/7 fut a felhőben, és készen áll, hogy kódoljon, tanuljon és menedzselje a projektjeidet!
