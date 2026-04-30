# Pflanzen-Pflegekalender

**Wichtig: Lesen Sie unbedingt zu erst die Datei `README.md` vollständig durch, bevor Sie diese Beschreibung lesen.**

Im Rahmen der ersten Modularbeit soll eine webbasierte Anwendung zur Verwaltung von Zimmerpflanzen und deren Pflegeplänen entwickelt werden.
Die Anwendung soll folgende Features unterstützen:

* Pflanzen anlegen, bearbeiten und löschen
* Pflegepläne für eine Pflanze konfigurieren (Pflegetyp + Intervall)
* Pflegeaktionen protokollieren (mit Datum und optionaler Notiz)
* Nächste fällige Aktionen je Pflanze anzeigen
* Überfällige Aktionen listenweise abrufbar machen
* Statusanzeige je Pflanze (ok / soon / overdue)


## Technischer Rahmen

Der Code für das Frontend (`static/app.js`) ist zusammen mit dem Style Sheet (`static/style.css`) und der `templates/index.html` bereits vorgegeben.
Ihre Aufgabe ist es, den zugehörigen Backend Code mit Hilfe von Python und Flask entwickeln.
Notwendige Details werden im Folgenden beschrieben. 
Sollten Sie Fragen haben, nutzen Sie bitte das Forum (ohne Code einzufügen).

## Datenmodell

Im folgenden werden die von der Anwendung verwalteten Daten beschrieben. 
Setzen Sie diese jeweils als Klassen um.
Das folgende nicht vollständige Klassendiagramm zeigt die wichtigsten Member-Variablen und die Assoziationen zwischen den Klassen.

![](images/class_diagram.svg)

*Tipp: Member-Funktionen wie `to_json()` können Ihnen bei Ihrer Implementierung helfen, Objekte von Ihrem Backend im `json`-Format zurückzuliefern.*

Im Folgenden werden noch die Eigenschaften genauer beschrieben.

**Wichtig:** Diese Eigenschaften müssen nicht zwingend alle Membervariablen Ihrer Klassen sein.
Je nachdem, wie Sie Assoziationen umsetzen, kann dies auch anders aussehen. 
Wichtigster Aspekt ist, dass Sie die weiter unten spezifizierte REST API einhalten.

### Pflanze (`Plant`)

Nutzer können in der Anwendung neue Pflanzen (`Plant`) anlegen und die Eigenschaften bereits angelegter Pflanzen visualisieren.
Eine Pflanze hat folgende Eigenschaften:

| Eigenschaft  | Typ             | Beschreibung                                      |
|--------------|-----------------|---------------------------------------------------|
| `id`         | integer         | Eindeutiger nummerischer Bezeichner               |
| `name`       | string          | Frei gewählter Name (z. B. „Mein Gummibaum")      |
| `species`    | string          | Botanische Art / Gattung (z. B. „Ficus elastica") |
| `location`   | string          | Standort (z. B. „Wohnzimmer Südfenster")          |
| `created_at` | date (ISO 8601) | Datum, an dem die Pflanze angelegt wurde          |

### Pflegeplan (`CareSchedule`)

Es gibt drei verschiedene Arten, eine Pflanze zu pflegen: Gießen (`watering`), Düngen (`fertilizing`) und Umtopfen (`repotting`).
Für jede Pflanze kann man festlegen, was von diesen drei Pflegearten in welchem Intervall (in Tagen) gemacht werden muss.

Jede Pflanze kann für jeden Pflegetyp **genau einen** Pflegeplan haben.

| Eigenschaft     | Typ         | Beschreibung                                               |
|-----------------|-------------|------------------------------------------------------------|
| `id`            | integer     | Eindeutiger Bezeichner                                     |
| `plant_id`      | integer     | ID der zugehörigen Pflanze                                 |
| `care_type`     | string      | Pflegetyp: `watering`, `fertilizing` oder `repotting`      |
| `interval_days` | integer ≥ 1 | Wie viele Tage zwischen zwei Pflegeaktionen liegen sollen  |

### Aktionsprotokoll (`ActionLog`)

Wurde eine Aktion durchgeführt, wird dies mit Hilfe eines `ActionLog`s gespeichert.
Ein `ActionLog` speichert folgende Daten:

| Eigenschaft    | Typ             | Beschreibung                                   |
|----------------|-----------------|------------------------------------------------|
| `id`           | integer         | Eindeutiger Bezeichner                         |
| `plant_id`     | integer         | ID der zugehörigen Pflanze                     |
| `care_type`    | string          | Art der durchgeführten Pflege                  |
| `performed_at` | date (ISO 8601) | Datum der Durchführung                         |
| `notes`        | string          | Optionale Notiz (z. B. „Volldünger verwendet") |


## Datumslogik

Das nächste Fälligkeitsdatum (`next_due`) einer Pflegeaktion wird **immer zur Laufzeit berechnet** und nie gespeichert:

```
last_log = letzter ActionLog für (plant, care_type)

if last_log vorhanden:
    next_due = last_log.performed_at + interval_days
else:
    next_due = plant.created_at + interval_days
```

Damit „schiebt" sich das Fälligkeitsdatum bei jeder Protokollierung nach vorne.
Eine Pflege gilt als **überfällig**, wenn `next_due < heute` (strikt kleiner).
Genau heute fällige Aktionen sind *nicht* überfällig.

**Beispiel:**
- Pflanze angelegt am 01.05., Gieß-Intervall 7 Tage → erste Fälligkeit: 08.05.
- Gegossen am 10.05. (2 Tage zu spät) → nächste Fälligkeit: 17.05. (nicht 15.05.)

---

## REST API

Alle Endpunkte geben JSON zurück und erwarten JSON im Request-Body (Content-Type: `application/json`).
Datumswerte sind immer im Format `YYYY-MM-DD`.

### Pflanzenstatus

Der Endpunkt `GET /api/plants` und `GET /api/plants/<id>` liefert zusätzlich zu den oben aufgeführten Eigenschaften der Pflanze(n) für jede Pflanze ein berechnetes Feld `status` zurück:

| Wert      | Bedeutung                                                 |
|-----------|-----------------------------------------------------------|
| `ok`      | Alle Pflegeaktionen liegen mehr als 3 Tage in der Zukunft |
| `soon`    | Mindestens eine Aktion ist in ≤ 3 Tagen fällig            |
| `overdue` | Mindestens eine Aktion ist bereits überfällig             |

---

### Pflanzen

#### `GET /api/plants`
Gibt alle Pflanzen zurück, jeweils inklusive berechnetem `status`.

**Response 200**
```json
[
  {
    "id": 1,
    "name": "Mein Gummibaum",
    "species": "Ficus elastica",
    "location": "Wohnzimmer",
    "created_at": "2026-03-01",
    "status": "soon"
  }
]
```

---

#### `POST /api/plants`
Legt eine neue Pflanze an.

**Request-Body** (alle Felder Pflicht außer `created_at`)
```json
{
  "name": "Efeutute",
  "species": "Epipremnum aureum",
  "location": "Küche",
  "created_at": "2026-04-01"
}
```

**Response 201** - die angelegte Pflanze als JSON-Objekt.

---

#### `GET /api/plants/<id>`
Gibt eine einzelne Pflanze zurück, inklusive `status` und der Liste ihrer Pflegepläne (`schedules`).

**Response 200**
```json
{
  "id": 1,
  "name": "Mein Gummibaum",
  "species": "Ficus elastica",
  "location": "Wohnzimmer",
  "created_at": "2026-03-01",
  "status": "ok",
  "schedules": [
    { "id": 1, "plant_id": 1, "care_type": "watering", "interval_days": 7 },
    { "id": 2, "plant_id": 1, "care_type": "fertilizing", "interval_days": 14 }
  ]
}
```

**Response 404** - Pflanze nicht gefunden.

---

#### `PUT /api/plants/<id>`
Aktualisiert Name, Art oder Standort einer Pflanze (partielle Updates sind erlaubt).

**Request-Body** (alle Felder optional)
```json
{ "name": "Neuer Name", "location": "Schlafzimmer" }
```

**Response 200** - die aktualisierte Pflanze.  
**Response 400** - ungültige(s) Feld(er) (das gilt auch für Zugriffe auf `id`, `status`, `created_at` oder `schedules`).
**Response 404** - Pflanze nicht gefunden.

---

#### `DELETE /api/plants/<id>`
Löscht eine Pflanze **inklusive** aller zugehörigen Pflegepläne und Protokolleinträge.

**Response 204** - kein Body.  
**Response 404** - Pflanze nicht gefunden.

---

### Pflegepläne

#### `GET /api/plants/<id>/schedules`
Gibt alle Pflegepläne einer Pflanze zurück.

**Response 200**
```json
[
  { "id": 1, "plant_id": 1, "care_type": "watering", "interval_days": 7 },
  { "id": 2, "plant_id": 1, "care_type": "fertilizing", "interval_days": 30 }
]
```

**Response 404** - Pflanze nicht gefunden.

---

#### `POST /api/plants/<id>/schedules`
Legt einen Pflegeplan an oder aktualisiert ihn, falls für diesen `care_type` bereits einer existiert.

**Request-Body**
```json
{ "care_type": "watering", "interval_days": 7 }
```

Erlaubte Werte für `care_type`: `watering`, `fertilizing`, `repotting`.  
`interval_days` muss ≥ 1 sein.

**Response 201** - der angelegte oder aktualisierte Pflegeplan.  
**Response 400** - fehlende oder ungültige Felder.  
**Response 404** - Pflanze nicht gefunden.

---

#### `DELETE /api/plants/<id>/schedules/<care_type>`
Entfernt den Pflegeplan für den angegebenen Pflegetyp.

**Response 204** - kein Body.  
**Response 404** - Pflegeplan nicht gefunden (auch falls Pflanze nicht gefunden).

---

### Aktionsprotokoll

#### `GET /api/plants/<id>/logs`
Gibt alle protokollierten Aktionen einer Pflanze zurück, absteigend nach Datum sortiert.

**Response 200**
```json
[
  {
    "id": 5,
    "plant_id": 1,
    "care_type": "watering",
    "performed_at": "2026-04-20",
    "notes": "Etwas weniger als sonst"
  }
]
```

**Response 404** - Pflanze nicht gefunden


---

#### `POST /api/plants/<id>/logs`
Protokolliert eine durchgeführte Pflegeaktion.

**Request-Body** (`performed_at` optional, Standard: heute)
```json
{
  "care_type": "watering",
  "performed_at": "2026-04-20",
  "notes": "Etwas weniger als sonst"
}
```

**Response 201** - der angelegte Protokolleintrag.  
**Response 400** - `care_type` fehlt.  
**Response 404** - Pflanze nicht gefunden.

---

### Fälligkeitsberechnung

#### `GET /api/plants/<id>/next-actions`
Berechnet für jeden Pflegeplan der Pflanze das nächste Fälligkeitsdatum und gibt die Liste aufsteigend nach Dringlichkeit sortiert zurück.

**Response 200**
```json
[
  {
    "care_type": "watering",
    "interval_days": 7,
    "next_due": "2026-04-28",
    "days_until": -1,
    "overdue": true
  },
  {
    "care_type": "fertilizing",
    "interval_days": 30,
    "next_due": "2026-05-10",
    "days_until": 11,
    "overdue": false
  }
]
```

`days_until` ist negativ, wenn die Aktion überfällig ist.

---

#### `GET /api/overdue`
Gibt alle überfälligen Pflegeaktionen **aller** Pflanzen zurück, absteigend nach Anzahl der Tage überfällig sortiert.

**Response 200**
```json
[
  {
    "plant_id": 2,
    "plant_name": "Bogenhanf",
    "plant_location": "Flur",
    "care_type": "repotting",
    "next_due": "2026-01-15",
    "days_overdue": 104
  }
]
```

---

## Persistenz

Verzichten Sie in dieser Anwendung auf eine persistente Speicherung der Daten.
Wir werden diesen Teil im zweiten Teil der Modularbeit adressieren.
Konkret bedeutet das: Wenn Sie den Server neu starten, müssen die vorher über das Frontend konfigurierten Pflanzen nicht wieder auftauchen.

## Frontend

Das Frontend ist eine Single-Page Application in Vanilla JS ohne externe Bibliotheken und bereits mit den Dateien `src/templates/index.html`, `src/static/app.js` und `src/static/style.css` vorgegeben.
Es kommuniziert ausschließlich über die REST API mit dem Backend.
Das Backend muss das Frontend unter `http://127.0.0.1:5000` zur Verfügung stellen.

## Starten

Die Anwendung ist muss nach dem Start unter `http://127.0.0.1:5000` erreichbar sein.
