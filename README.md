# Modularbeit 1 - Allgemeine Anforderungen

> **Hinweis:** Dieses Dokument beschreibt die allgemeinen Anforderungen an die Modularbeit.
> Projektdetails und die Spezifikation der REST API werden in separaten Abschnitten ergänzt.

**WICHTIG** Lesen Sie dieses Dokument sorgfältig und vollständig, bevor Sie die Projektbeschreibung lesen und mit Ihrer Umsetzung beginnen!

## Inhaltsverzeichnis

[[_TOC_]]


## Überblick

Die Modularbeit verbindet die ersten Kernthemen der Vorlesung:

| Thema                            | Übung       |
|----------------------------------|-------------|
| Versionsverwaltung mit Git       | Übung 1 & 2 |
| REST API Entwicklung             | Übung 3     |
| Scrum & Requirements Engineering | Übung 4     |
| Testen mit pytest                | Übung 5     |
| CI/CD                            | Übung 6     |

Sie entwickeln innerhalb dieses GitLab-Projekts eine vollständig getestete REST API und durchlaufen dabei einen vereinfachten Scrum-Prozess.

> **WICHTIG:** Ihr Projekt wird an vielen Stellen automatisiert auf Korrektheit geprüft werden.
> Achten Sie daher unbedingt darauf, dass Sie **exakt die geforderten Namen** verwenden.
> Ein falscher Name führt zu fehlschlagenden Tests - und damit zu null Punkten für die betroffene Aufgabe.

## Hinweise zur Nutzung von KI

Der Arbeitsmarkt verändert sich rasant: Tätigkeiten auf Einstiegsniveau werden zunehmend durch KI-Systeme übernommen oder automatisiert. 
Wer wesentliche Teile dieser Modularbeit oder anderer Projekte einfach generieren lässt, ohne die Ergebnisse zu verstehen, zu hinterfragen und selbst nachzuvollziehen wird nie über das Einstiegsniveau hinauskommen und damit für den Arbeitsmarkt unattraktiv bleiben.

**Wie Sie KI intelligent einsetzen sollten**

KI ist ein außerordentlich mächtiges Werkzeug, vorausgesetzt, Sie nutzen es so, dass Sie selbst dabei wachsen:

* **Probleme zuerst selbst durchdenken:** Bevor Sie eine KI befragen, sollten Sie das Problem verstanden und einen eigenen Lösungsansatz formuliert haben. 
  Erst dann ist KI sinnvoll: als Sparringspartner, der Ihren Ansatz bewertet, Alternativen aufzeigt oder blinde Flecken benennt.
* **KI-Ausgaben aktiv prüfen und hinterfragen:** Generierter Code oder Text ist nie einfach zu übernehmen. Verstehen Sie jede Zeile. 
  Fragen Sie nach: Warum dieser Ansatz? Welche Alternativen gibt es? Was passiert, wenn sich die Anforderungen ändern?
* **Fehler als Lernchance nutzen:** Wenn etwas nicht funktioniert, debuggen Sie zunächst selbst. 
  Die KI kann dann helfen, gezielt Hinweise zu geben, aber das Verständnis, das Sie durch eigenes Suchen aufbauen, ist unersetzlich.
* **KI für Recherche und Vertiefung einsetzen:** Nutzen Sie KI, um neue Konzepte zu erkunden, sich komplexe Sachverhalte erklären zu lassen oder Zusammenhänge 
  zu verstehen, nicht um fertige Antworten zu konsumieren, sondern um tiefer in ein Thema einzutauchen.

**KI Nutzung im Rahmen dieser Modularbeit:**

Im Rahmen der Modularbeit dürfen Sie KI-Tools (z.B. ChatGPT, Copilot, etc.) nutzen.
Sie müssen die Nutzung von KI-Tools allerdings in Form von Gitlab Issues protokollieren und reflektieren.
Erstellen Sie für jede KI-Nutzung ein Issue mit Hilfe des weiter unten angegebenen Issue Templates `KI Nutzung.md`.
Unvollständige Angaben gelten als nicht dokumentiert.

## 1  GitLab-Projekt einrichten

In den folgenden Schritten werden Sie Ihr Gitlab-Projekt analog der Praktikumsaufgaben einrichten.

### 1.1  Issue Boards

Löschen Sie in Ihrem GitLab-Projekt das vorhandene Issue Board `Development`.
Legen Sie anschließend die zwei folgenden Issue Boards an:

| Board-Name        | Zweck                                                  |
|-------------------|--------------------------------------------------------|
| `Product Backlog` | Sammlung aller User Stories, nach Priorität sortiert   |
| `Sprint Backlog`  | Aktuell bearbeitete User Stories des laufenden Sprints |

### 1.2  Labels

Legen Sie die folgenden Labels an und verwenden Sie diese konsequent für die erzeugten Issues:

| Label              | Farbe                  | Bedeutung                       |
|--------------------|------------------------|---------------------------------|
| `Type::User Story` | Blau (#6699cc)         | Issue ist eine User Story       |
| `Type::Bug`        | Rot (#dc143c)          | Fehlerbericht                   |
| `AI Usage Doc`     | Magenta-Pink (#cc338b) | Dokumentiert die Nutzung von KI |

### 1.3  Milestones / Sprints

Legen Sie zwei Milestones an:

| Title      | Start Date | Due Date   |
|------------|------------|------------|
| `Sprint 1` | 2026-05-01 | 2026-05-15 |
| `Sprint 2` | 2026-05-18 | 2026-05-29 |

Konfigurieren Sie das Issue Board `Sprint Backlog` so, dass dort genau **vier Listen** sichtbar sind.
Die Listen werden in GitLab jeweils über ein Label oder einen Milestone definiert:

| # | Listen-Typ           | Konfiguration                                                                      |
|---|----------------------|------------------------------------------------------------------------------------|
| 1 | Offen (open)         | Alle offenen Issues mit Label `Type::User Story` oder `Type::Bug`                  |
| 2 | Sprint 1             | Alle Issues mit Milestone `Sprint 1` und Label `Type::User Story` oder `Type::Bug` |
| 3 | Sprint 2             | Alle Issues mit Milestone `Sprint 2` und Label `Type::User Story` oder `Type::Bug` |
| 4 | Geschlossen (closed) | Alle geschlossenen Issues mit Label `Type::User Story` oder `Type::Bug`            |

### 1.4  Issue-Templates

#### User Story Template

Legen Sie das Issue-Template `User Story.md` an. Das Template muss **exakt** folgenden Inhalt haben:

```markdown
## User Story

**As a** [type of user],
**I want to** [do something],
**So that** [achieve some goal].

### Acceptance Criteria

1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]
   - [Sub-criterion, if applicable]

### Technical Requirements (optional)

Describe, e.g., REST endpoints here

### Tasks

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Additional Information (optional)

[Include any relevant information, links, or resources here.]
```

#### Bug Report Template

Legen Sie das Issue-Template `Bug Report.md` an. Das Template muss **exakt** folgenden Inhalt haben:

```markdown
## Bug Report 

### Brief Description of the Issue

Short description.

### Steps to Reproduce

1. [ ] Go to '...'
2. [ ] Click on '....'
3. [ ] Scroll down to '....'
4. [ ] The error occurs.

### Expected Behavior

Describe the expected behavior here.

### Actual Behavior

Describe the observed behavior here.

### System Information

* Operating System: (e.g., Windows 11, macOS 14.4)
* Browser & Version: (e.g., Firefox 120, Chrome 122)
* App Version: (e.g., v1.2.4 or commit hash)
* User Role: (e.g., Admin, Guest)

### Logs / Error Messages

Insert error messages or console logs here.
```

#### KI Nutzungs-Template

Erstellen Sie ein Gitlab Issue Template namens `KI Nutzung.md` mit folgendem Inhalt: 

```markdown
# KI-Nutzungsprotokoll

> Für **jede KI-Anfrage** muss ein Eintrag erstellt werden.
> Unvollständige oder zusammengefasste Angaben gelten als nicht dokumentiert.

## Eintrag

**Datum & Uhrzeit:**
**Tool / Modell:**

**Ziel der Anfrage (1 Satz):**

**Prompt:**

<exakter Prompt>

**Antwort (gekürzt erlaubt):**

<wesentliche Teile der Antwort>

**Verwendung im Projekt:**

* Datei / Modul:
* Art:

  * [ ] direkt übernommen
  * [ ] angepasst
  * [ ] nur als Idee genutzt

**Kurze Bewertung (1–2 Sätze):**

* hilfreich / problematisch weil:
```

Nutzen Sie die ersten beiden Issue Templates für **alle** User Stories, sowie von Bugs.
Protokollieren Sie jegliche Nutzung der KI mit Hilfe des KI-Nutzungstemplates.

Für alle erstellten Issues wird außerdem die Zuweisung des passenden Labels erwartet. 
Sie dürfen obige Templates erweitern, um die Auswahl des zugehörigen Labels zu automatisieren.

## 2  User Stories anlegen

Legen Sie mindestens für **jeden einzelnen geforderten REST-Endpunkt** der API (siehe Projektbeschreibung) eine eigene User Story als GitLab-Issue an.

Jede User Story muss folgende Angaben enthalten:

- **Title** im Format `As a [type of user], I want to [do something].`
- **Template** `User Story.md` vollständig ausgefüllt
- **Label** `Type::User Story`
- **Milestone** `Sprint 1` oder `Sprint 2`
- **Weight** in Story Points - schätzen Sie vor Bearbeitungsbeginn; ändern Sie das Weight im Sprint nicht mehr

Verwenden Sie für die Schätzung folgendes T-Shirt-Weight-Mapping:

| T-Shirt-Größe | Weight |
|---------------|--------|
| S             | 1      |
| M             | 2      |
| L             | 3      |
| XL            | 5      |
| XXL           | 8      |


Sollten weitere User Stories zur Umsetzung des Projekts notwendig sein, können Sie diese selbstverständlich anlegen.

## 3  Planung der Sprints

### Erster Sprint (1.5. bis 15.5.)

Sortieren Sie den Product Backlog nach der gewünschten Implementierungsreihenfolge.
Ordnen Sie dem Milestone `Sprint 1` mit Hilfe des Sprint Backlog Issue Boards jene User Stories zu, die Sie bis zum **15. Mai** umsetzen können (inklusive Tests).
Versuchen Sie realistisch zu planen: Wer nicht am 1. Mai beginnt, plant entsprechend für den ersten Sprint weniger ein.

Beachten Sie bei Ihrer Planung, dass bis zum 29.5. um 23:59 Uhr, d.h. zum Ende des zweiten Sprints, die vollständig funktionierende Backend-Anwendung vorliegen muss.
Planen Sie Ihre Zeit entsprechend ein!

Wenn Sie eine User Story fertig umgesetzt haben (mehr dazu weiter unten), muss diese mit Hilfe des zugehörigen Merge Requests geschlossen werden (Stichwort `Closes #<Issue-Nr.>`).

### Zweiter Sprint (18.5. bis 29.5.)

Verschieben Sie am Ende des ersten "Sprints" die noch offenen User Stories im Sprint Backlog Issue Board in den `Sprint 2`.
Dokumentieren Sie Fehler der aktuellen Implementierung mit Hilfe des Bug Templates und planen Sie die Behebung ebenfalls für den `Sprint 2`.
Zum Ende des zweiten Sprints sollten alle User Stories fertig und korrekt umgesetzt, alle Bugs behoben und so eine vollständige mit dem Frontend zusammenarbeitende Anwendung vorliegen.

## 4  Projektstruktur

Das Repository muss folgender Struktur entsprechen:

| Pfad               | Inhalt                                          |
|--------------------|-------------------------------------------------|
| `src/`             | Backend-Implementierung (ggf. mit Unterordnern) |
| `tests/`           | Alle Tests                                      |
| `requirements.txt` | Alle benötigten Python-Pakete                   |
| `pytest.ini`       | pytest-Konfiguration                            |
| `.vscode/`         | VS-Code-Konfigurationsdateien für Tests         |
| `.gitignore`       | Ausschlussliste für temporäre Dateien           |

> Temporäre Dateien wie `__pycache__`, virtuelle Umgebungen o. Ä. dürfen **nicht** im Repository landen.
> Lesen Sie nach, wofür eine `.gitignore`-Datei ist, und tragen Sie alle nicht versionierungswürdigen Ordner und Dateien ein (gerne mit Hilfe eines LLMs).


## 5  Entwicklung mit Merge Requests

Jede User Story **muss** über mindestens einen eigenen **Merge Request (MR)** mit zugehörigem Feature-Branch bearbeitet werden.
User Stories, die nicht nach diesem Workflow abgearbeitet werden, gelten als nicht bearbeitet.

### Anforderungen an Merge Requests

- Die MR-Beschreibung referenziert die zugehörige User Story: `Closes #<Issue-Nr.>`
- Der MR enthält **sowohl die Implementierung als auch die zugehörigen Tests**.
- In `main` dürfen nur getestete MRs gemergt werden.
- Ab **Sprint 2** (18.5.) ist die CI aktiv: ab dann dürfen nur noch MRs mit **grüner CI** gemergt werden.

### Commit-Regeln

Features müssen **schrittweise und manuell** in Feature Branches umgesetzt werden.
Das automatisierte Test-Tool prüft folgende Regeln:

#### Regel 1 - Maximale Commit-Größe: 30 Zeilen

Pro Commit dürfen maximal **30 Zeilen** geändert werden (Summe aus hinzugefügten und gelöschten Zeilen, ohne Leerzeilen).
Das entspricht etwa einer kleinen Funktion oder einem einzelnen Testfall. 
Genug für echte Schritte, aber zu wenig für stupides KI-generiertes Copy & Paste Coding.

#### Regel 2 - Mindestabstand zwischen Commits: 1 Minute

Zwischen zwei aufeinanderfolgenden Commits im gleichen Branch müssen mindestens **60 Sekunden** liegen.
Automatisiert erzeugte Commits (z. B. per Skript oder KI-Tool) entstehen typischerweise in Millisekunden - diese Regel macht das sichtbar.

#### Regel 3 - Commits nur im Rahmen von MRs, kein Commit in `main`

* Sie dürfen nicht direkt im `main`-Branch committen.
* Sie dürfen nur in Feature Branches committen.
* Jeder Feature Branch muss einem Merge Request zugeordnet sein (ergibt sich automatisch aus dem Workflow).

#### Regel 4 - Keine Squash Commits; Merge statt Rebase

Sie dürfen im Rahmen des Projekts Commits nicht squashen. 
Dies würde zu deutlich größeren Commits führen und die Nachvollziehbarkeit im Projekt erschweren.
Somit können Ergebnisse nicht gewertet werden.

Verzichten Sie auf die Verwendung von Rebase beim Zusammenführen von Branches.
Nutzen Sie hierfür ausschließlich Merge, um so eine Nachvollziehbarkeit zu garantieren.

#### Ausnahmen (für die Regeln)

| Ausnahme                                                                                 | Begründung                           |
|------------------------------------------------------------------------------------------|--------------------------------------|
| Merge Commits                                                                            | Enthalten keinen neuen, eigenen Code |
| Konfigurationsdateien (`.gitlab-ci.yml`, `requirements.txt`, `pytest.ini`, `.gitignore`) | Projekt-Setup, kein Feature-Code     |
| Dateien unter `.gitlab/` (Issue-Templates)                                               | Projekt-Setup                        |
| `README.md`                                                                              | Dokumentation                        |

*Hinweis:* Issue Templates und Konfigurationsdateien können Sie ohne User Story und Merge Request direkt anlegen und in `main` einchecken.

#### Commits lokal prüfen

Die folgenden Befehle helfen bei der Überprüfung vor einem Commit:

```bash
# Geänderte Zeilen in der Stage (ohne Konfigurationsdateien)
git diff --cached --shortstat -- . ":!*.yml" ":!*.yaml" ":!*.txt" ":!*.ini" ":!*.md"

# Zeit seit dem letzten Commit
git log -1 --format=%ar
```

### Anforderungen an die Implementierung

Die Projektbeschreibung [ProjectDescription.md](ProjectDescription.md) gibt vor, welche Endpunkte Ihre REST API bereitstellen muss.
Setzen Sie die Implementierung vollständig und Endpunkt für Endpunkt um.

**API-Anforderungen:**

- Alle in der Projektbeschreibung geforderten Endpunkte sind vollständig implementiert.
- Alle Antworten verwenden `Content-Type: application/json`.
- Die API verwendet **korrekte HTTP-Statuscodes** (z. B. `201` für erstellte Ressourcen, `404` für nicht gefundene, `400` für fehlerhafte Anfragen).
- Fehlerhafte Anfragen liefern eine Fehlermeldung im folgenden JSON-Format:
  ```json
  { "error": "Beschreibung des Fehlers" }
  ```
- Die Anwendung läuft auf Port **5000**.
- Verwenden Sie **Flask** als Backend-Framework.

**Test-Anforderungen:**

- Nutzen Sie `pytest` für Komponenten-, Integrations- und Systemtests.
- Nutzen Sie den Flask-Testclient für API-Tests aller Endpunkte.
- Nutzen Sie das vorgegebene Frontend für manuell durchgeführte Acceptance Tests.
- Tests decken sowohl den **Happy Path** als auch **Fehlerfälle** ab (z. B. fehlende Felder, ungültige IDs).
- Nutzen Sie **pytest-Fixtures**, um Code Duplikation bei der Implementierung von Tests zu vermeiden.
- Testnamen folgen dem Format `test_<endpunkt>_<szenario>`.
- Testen Sie das **Verhalten** von Klassen / Funktionen (öffentliche Schnittstelle), nicht der interne Zustand.
- Die **Code Coverage** muss mindestens **90 %** betragen. Liegt sie darunter, gilt dieser Punkt der Modularbeit als nicht bestanden.
  Verwenden Sie `pytest-cov` zur Messung sowie Coverage Gutters in VS Code zur visuellen Überprüfung nicht abgedeckter Codebereiche.



## 6  CI/CD-Pipeline

In der kommenden Vorlesung wird das Thema „Continuous Integration" behandelt.
Nach der Vorlesung wird automatisch eine entsprechende User Story in Ihrem Projekt angelegt.
Diese muss spätestens als erste Story in **Sprint 2** (ab 18.5.) umgesetzt werden - früher ist möglich.

Anforderungen an Ihre Pipeline:

* Pipeline korrekt mittels `.gitlab-ci.yml` konfiguriert 
* Vorhandene Tests werden automatisch in einer Stage namens `test` bei einem Commit auf einem beliebigen Branch ausgeführt
* junit-Berichte von pytest werden in Gitlab angezeigt
* Die Code Coverage wird automatisiert ermittelt und in Gitlab angezeigt
* Merge Requests werden nur noch durchgeführt, wenn die Pipeline grün ist (alles OK)


## 7 Bug Documentation

Im Rahmen Ihrer Umsetzung werden Sie Fehler in der Anwendung finden.
Dokumentieren Sie mindestens zwei Fehler mit Hilfe des Bug Templates.
Beheben Sie dann diese Fehler, indem Sie einen zugehörigen Merge Request und Branch erstellen.


## 8  Bewertungskriterien (Übersicht)

*Projektdetails und REST-API-Spezifikation werden in separaten Abschnitten ergänzt.*

Die Modularbeit wird mit insgesamt **100 Punkten** bewertet.
Implementierung und Tests machen bewusst nicht mehr als 40 % aus - der Fokus liegt auf dem Engineering-Prozess, der auch beim Einsatz von KI nachvollziehbar und korrekt durchgeführt werden muss.

> **Hinweis 1:** Betrachten Sie die unten aufgeführten Punkte eher als Richtwert und unter Vorbehalt.
> Diese können durchaus noch angepasst werden.

> **Hinweis 2:** Viele Kriterien werden automatisiert geprüft (Commit-Regeln, Benennung, Coverage).
> Abweichungen von den exakten Vorgaben führen zu 0 Punkten für das jeweilige Kriterium.

### 8.1  GitLab-Projekt einrichten - 10 Punkte

| Kriterium                                                                                                          | Punkte |
|--------------------------------------------------------------------------------------------------------------------|--------|
| Issue Boards `Product Backlog` und `Sprint Backlog` korrekt angelegt und konfiguriert (4 Listen im Sprint Backlog) | 3      |
| Alle drei Labels mit korrektem Namen und Farbe vorhanden                                                           | 2      |
| Milestones `Sprint 1` und `Sprint 2` mit korrekten Daten angelegt                                                  | 2      |
| Alle drei Issue-Templates vollständig und inhaltlich korrekt (`User Story.md`, `Bug Report.md`, `KI Nutzung.md`)   | 3      |

### 8.2  User Stories & Requirements Engineering - 12 Punkte

| Kriterium                                                                         | Punkte |
|-----------------------------------------------------------------------------------|--------|
| Für jeden geforderten REST-Endpunkt eine eigene User Story als Issue vorhanden    | 5      |
| Jede User Story folgt dem Titelformat und hat das Template vollständig ausgefüllt | 6      |
| Label `Type::User Story`, Milestone und Weight bei jeder Story korrekt gesetzt    | 1      |

### 8.3  Sprint-Planung & Scrum-Prozess - 6 Punkte

| Kriterium                                                                       | Punkte |
|---------------------------------------------------------------------------------|--------|
| Product Backlog vor Sprint 1 priorisiert                                        | 2      |
| Sprint 1 und 2 wurden geplant; Stories den Milestones korrekt zugeordnet        | 2      |
| Abgeschlossene Stories werden ausschließlich über `Closes #x` im MR geschlossen | 2      |

### 8.4  KI-Nutzungsdokumentation - 7 Punkte

| Kriterium                                                                                             | Punkte |
|-------------------------------------------------------------------------------------------------------|--------|
| Für jede KI-Anfrage ein eigenes Issue mit Template `KI Nutzung.md` und Label `AI Usage Doc` vorhanden | 4      |
| Template vollständig ausgefüllt (Datum/Uhrzeit, Tool, Prompt, Antwort, Verwendung, Bewertung)         | 3      |

> **Pflichtbedingung:** Nicht dokumentierte KI-Nutzung gilt als Täuschungsversuch und führt zur Bewertung der gesamten Arbeit mit 0 Punkten.

### 8.5  Commit- & Merge-Request-Workflow - 15 Punkte

| Kriterium                                                                               | Punkte |
|-----------------------------------------------------------------------------------------|--------|
| Jede User Story besitzt einen eigenen Feature Branch und zugehörigen Merge Request      | 3      |
| MR-Titel referenziert die zugehörige User Story (`Closes #<Nr.>`)                       | 2      |
| Alle relevanten Commits halten die Größenbeschränkung von ≤ 30 Zeilen ein               | 5      |
| Mindestabstand von ≥ 60 Sekunden zwischen aufeinanderfolgenden Commits im selben Branch | 3      |
| Kein Commit direkt in `main` (ausgenommen erlaubte Konfigurationsdateien)               | 2      |

### 8.6  Implementierung der REST API - 20 Punkte

| Kriterium                                                   | Punkte |
|-------------------------------------------------------------|--------|
| Alle geforderten Endpunkte vollständig implementiert        | 11     |
| Korrekte HTTP-Statuscodes (`200`, `201`, `400`, `404` etc.) | 6      |
| Fehlermeldungen im Format `{ "error": "..." }`              | 3      |

### 8.7  Tests - 20 Punkte

| Kriterium                                                                                | Punkte |
|------------------------------------------------------------------------------------------|--------|
| Flask-Testclient für alle Endpunkte verwendet                                            | 3      |
| Happy Path **und** Fehlerfälle (fehlende Felder, ungültige IDs, …) abgedeckt             | 5      |
| pytest-Fixtures eingesetzt; keine Code-Duplikation                                       | 3      |
| Sinnvolle Nutzung von MagicMocks                                                         | 2      |
| Code Coverage ≥ 90 % (`pytest-cov`); darunter: **0 Punkte für den gesamten Testbereich** | 7      |

### 8.8  CI/CD-Pipeline - 5 Punkte

| Kriterium                                                                                                                      | Punkte |
|--------------------------------------------------------------------------------------------------------------------------------|--------|
| Pipeline korrekt konfiguriert (`.gitlab-ci.yml` vorhanden, Tests werden ausgeführt, Berichte angezeigt und Coverage ermittelt) | 2      |
| Alle Tests laufen in der CI grün durch; ab Sprint 2 nur grüne MRs gemergt                                                      | 3      |

### 8.9  Bug-Dokumentation - 5 Punkte

| Kriterium                                                                         | Punkte |
|-----------------------------------------------------------------------------------|--------|
| Mindestens 2 Bugs mit Template `Bug Report.md` und Label `Type::Bug` dokumentiert | 3      |
| Jeder Bug über einen eigenen Merge Request mit zugehörigem Branch behoben         | 2      |

### Zusammenfassung

| Bereich                                      |  Punkte |
|----------------------------------------------|--------:|
| 8.1  GitLab-Projekt einrichten               |      10 |
| 8.2  User Stories & Requirements Engineering |      12 |
| 8.3  Sprint-Planung & Scrum-Prozess          |       6 |
| 8.4  KI-Nutzungsdokumentation                |       7 |
| 8.5  Commit- & MR-Workflow                   |      15 |
| 8.6  Implementierung der REST API            |      20 |
| 8.7  Tests                                   |      20 |
| 8.8  CI/CD-Pipeline                          |       5 |
| 8.9  Bug-Dokumentation                       |       5 |
| **Gesamt**                                   | **100** |

Implementierung (8.6) + Tests (8.7) = **40 Punkte (40 %)**.
Die verbleibenden **60 Punkte** entfallen auf Prozess, Planung, Workflow und Dokumentation.


## 9 Noten

**Achtung:** Das erfolgreiche Abschließen dieser Modularbeit ist Voraussetzung für das Antreten des zweiten Teils. 
Die Modularbeit gilt als erfolgreich angetreten, wenn mindestens 50% der Punkte erreicht werden. 

Für die Notenbildung kann die folgende Tabelle als Orientierungspunkt dienen (Anpassungen sind möglich):

| von | bis | Note |
|-----|-----|------|
| 0   | 49  | 5.0  |
| 50  | 54  | 4.0  |
| 55  | 59  | 3.7  |
| 60  | 64  | 3.3  |
| 65  | 69  | 3.0  |
| 70  | 74  | 2.7  |
| 75  | 79  | 2.3  |
| 80  | 84  | 2.0  |
| 85  | 89  | 1.7  |
| 90  | 94  | 1.3  |
| 95  | 100 | 1.0  |


## 10  Abgabetermin

Am 29.5.2026 um 23:59 Uhr werden Ihnen die Schreibrechte in Ihrem Gitlab-Projekt automatisch entzogen. 
Der zu diesem Zeitpunkt vorliegende Stand gilt als abgegebene Modularbeit. 
