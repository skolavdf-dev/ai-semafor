# AI semafor

Web běží na **https://www.skolavdf.cz/hub/ai-semafor/**.

Statický web s pravidly používání umělé inteligence ve výuce na **VOŠ, SPŠ a SOŠ Varnsdorf**. Pro každý obor ukazuje čtyřúrovňový „semafor“, tedy kdy smí žák při úkolu, projektu nebo zkoušce použít AI a kdy má ukázat, co umí sám/sama.

Úrovně vycházejí z rámce AI Assessment Scale (Perkins, Furze, Roe & MacVaugh, 2024/2025):

| Úroveň | Barva na webu | Fixní barva (ikony, odznaky, tisk) | Význam |
| :--- | :--- | :--- | :--- |
| AI povolena | zelená `#A6CE39` | `#137A45` | AI je běžnou součástí procesu |
| AI omezeně | oranžová `#D98100` | `#D98100` | AI jen pro přesně určenou část práce |
| Bez generativní AI | červená `#EF4444` | `#B3261E` | úkol ověřuje vlastní dovednost |
| AI Lab | modrá `#41D7FF` | `#1A56B0` | cílem je naučit se s AI pracovat |

## Struktura projektu

```
index.html          rozcestník (úvod, přehled oborů, odkaz na manuál)
grafika.html        semafor pro obor Grafický design
it.html             semafor pro obor Informační technologie
pedagogika.html     semafor pro obor Předškolní a mimoškolní pedagogika
manual.html         grafický manuál: barvy, ikony a odznaky ke stažení, typografie
assets/
  style.css         sdílené styly všech stránek
  icons/            ikony úrovní (SVG + PNG 512×512)
  badges/           odznaky do zadání (SVG + PNG 1380×312)
design-system/      předpisy designu školy (kopie repozitáře, jen reference, na server se nenahrává)
tools/
  bump-version.py   přidá k assetům v HTML otisk obsahu (?v=...)
web.config          nastavení cache pro IIS
```

Web je čisté HTML a CSS bez build kroku a bez závislostí. Jediný JavaScript je kopírování kódů barev v `manual.html`. Písmo Raleway (a v manuálu JetBrains Mono) se načítá z Google Fonts.

## Lokální náhled

Stačí otevřít `index.html` v prohlížeči. Pokud potřebuješ spustit přes HTTP server:

```bash
python -m http.server 8765
```

a otevřít `http://localhost:8765`.

## Design

Vzhled vychází z design systému školy ([github.com/skolavdf-dev/design-system](https://github.com/skolavdf-dev/design-system)), jehož kopie je ve složce `design-system/` (viz `docs/DESIGN.md` a `docs/LOGO.md`):

- tmavý gradient `#003b4b` → `#006783`, skleněné panely, žádné rámečky,
- ostré hrany panelů, zaoblení 4 px jen u tlačítek a formulářových polí,
- písmo Raleway, žluté odkazy (`#ffd400`) bez podtržení, podtržení až při najetí,
- odrážky ve tvaru trojúhelníku z loga školy.

Barva úrovně semaforu se nastavuje proměnnou `--c` u `section.level` a promítá se do pruhu panelu, odrážek a rámečku s doporučením.

## Úprava obsahu

Texty jednotlivých úrovní jsou přímo v HTML souborech oborů. Každá úroveň má stejnou strukturu: odznak, nadpis, krátký úvod, seznam odrážek (`ul.bullets`) a rámeček `p.callout`.

Při psaní textů pro žáky (15–19 let) dodržuj:

- jednoduché a srozumitelné formulace, odborné pojmy vysvětli nebo nahraď češtinou,
- tvar „sám/sama“, „udělal/a“,
- důležité části zvýrazni pomocí `<strong>`.

Ikony a odznaky jsou SVG v `assets/icons` a `assets/badges`. PNG verze se z nich generují zvlášť. Při změně SVG je nutné PNG znovu vyexportovat (ikony 512×512, odznaky 1380×312), jinak se v manuálu nabídne ke stažení stará verze.

## Nasazení

Web běží na IIS 10 na adrese https://www.skolavdf.cz/hub/ai-semafor/, na serveru je to podsložka `hub/ai-semafor`.

1. Před nahráním spusť:

   ```bash
   python tools/bump-version.py
   ```

   Skript přidá ke každému assetu v HTML krátký otisk jeho obsahu (např. `style.css?v=ed86c7ab`). Verze se mění jen u souborů, které se opravdu změnily, a prohlížeče si tak stáhnou nové CSS a obrázky. Skript je bezpečné pouštět opakovaně.

2. Nahraj na server `*.html`, složku `assets/` a `web.config`. Složky `design-system/`, `tools/` a `.backup/` na server nepatří.

### Cache

`web.config` nastavuje přes `customHeaders`:

- stránky (HTML): `Cache-Control: no-cache`, takže se prohlížeč při každém načtení zeptá serveru, jestli se soubor změnil,
- `assets/`: `Cache-Control: public, max-age=31536000`, protože změna souboru znamená novou adresu (nový otisk v URL).

Hlavičky se přidávají přes `customHeaders`, protože nastavení `clientCache` se na serveru školy neuplatnilo (odpověď měla dál jen `Cache-Control: private`). Funkčnost ověříš v Chrome: `F12` → *Network* → klik na `index.html` → *Response headers*. Očekávaná hodnota je `private,no-cache`. Pokud se po nasazení pořád zobrazuje stará verze, zkus `Ctrl+Shift+R`. Pokud ani to nepomůže, kontroluj nadřazené nastavení serveru a případnou CDN nebo proxy.

## Licence a autorská práva

Logo, barvy a grafické podklady školy jsou duševním vlastnictvím VOŠ, SPŠ a SOŠ Varnsdorf. Podrobnosti viz [design-system](https://github.com/skolavdf-dev/design-system) (`README.md` a `LICENSE`).
