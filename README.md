# 🌱 Pflanzenkalender – Teil 1

**REST-API-Entwicklung mit Python und Flask | Software Engineering**

## Projektübersicht

Der Pflanzenkalender ist ein Hochschulprojekt aus dem Modul Software Engineering im 2. Semester des Studiengangs Informatik & Design an der Hochschule München.

Ziel war die Entwicklung einer REST-API, mit der Pflanzen verwaltet, Pflegeintervalle organisiert und durchgeführte Pflegeaktivitäten dokumentiert werden können.

Im Mittelpunkt standen neben der eigentlichen Backend-Programmierung auch Requirements Engineering, automatisiertes Testing, Versionsverwaltung und ein strukturierter Entwicklungsprozess.

**Dieser erste Projektteil wurde als Einzelarbeit umgesetzt.**

## Funktionsumfang

### Pflanzenverwaltung

Die REST-API unterstützt grundlegende Funktionen zur Verwaltung von Pflanzen:

- Pflanzen anlegen
- Vorhandene Pflanzen abrufen
- Pflanzeninformationen aktualisieren
- Pflanzen löschen

### Pflegeintervalle

Für Pflanzen können wiederkehrende Pflegeaktivitäten und entsprechende Intervalle hinterlegt und verwaltet werden.

### Pflegeprotokoll

Durchgeführte Pflegemaßnahmen lassen sich dokumentieren und anschließend in einem Verlauf nachvollziehen.

### Anstehende und überfällige Pflegeaufgaben

Das Backend ermöglicht die Berechnung von Pflegeaktivitäten, die demnächst anstehen oder deren geplanter Zeitpunkt bereits überschritten wurde.

Die Kommunikation erfolgt über REST-Endpunkte mit JSON-Antworten und passenden HTTP-Statuscodes.

## Verwendete Technologien

| Technologie | Einsatz |
|---|---|
| Python | Backend-Programmierung |
| Flask | REST-API und HTTP-Verarbeitung |
| JSON | Datenaustausch |
| pytest | Automatisierte Tests |
| Flask-Testclient | Tests der API-Endpunkte |
| pytest-cov | Ermittlung der Testabdeckung |
| Git & GitLab | Versionsverwaltung und Entwicklungsworkflow |

## Meine Aufgaben

Da es sich um eine Einzelarbeit handelte, war ich für die Umsetzung der Projektanforderungen verantwortlich.

Dazu gehörten insbesondere:

- Formulierung und Bearbeitung von zwölf User Stories
- Definition und Berücksichtigung von Akzeptanzkriterien
- Implementierung der Backend-Funktionen mit Python und Flask
- Entwicklung der REST-Endpunkte
- Erstellung und Anpassung automatisierter Tests
- Bearbeitung von GitLab-Issues
- Entwicklung in Feature-Branches und Integration über Merge Requests
- Dokumentation des Entwicklungsprozesses und der KI-Unterstützung

## Software-Engineering-Prozess

### Requirements Engineering

Zu Beginn wurden die geforderten Funktionen in User Stories mit Akzeptanzkriterien und technischen Aufgaben übersetzt.

Die Anforderungen bildeten die Grundlage für die weitere Implementierung und die zugehörigen Tests.

### Sprintplanung und Versionsverwaltung

Die Entwicklung orientierte sich an einem vereinfachten Scrum-Prozess mit Product Backlog, Sprint Backlog und zwei Sprints.

Die Funktionen wurden schrittweise in Feature-Branches entwickelt und über Merge Requests zusammengeführt.

### Testing und Qualitätssicherung

Für die automatisierten Tests verwendete ich pytest und den Flask-Testclient.

Dabei wurden sowohl erfolgreiche API-Aufrufe als auch Fehlerfälle betrachtet, beispielsweise:

- Fehlende Pflichtfelder
- Ungültige Eingaben
- Nicht vorhandene Ressourcen
- Erwartete HTTP-Statuscodes und JSON-Antworten

Die Aufgabenstellung umfasste außerdem eine automatisierte CI/CD-Pipeline zur Ausführung und Auswertung der Tests.

## Lokale Einrichtung und Tests

Voraussetzung ist eine passende Python-Installation.

Eine virtuelle Umgebung kann folgendermaßen erstellt werden:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Anschließend können die im Projekt angegebenen Abhängigkeiten installiert werden:

```bash
python -m pip install -r requirements.txt
```

Die Tests lassen sich mit pytest ausführen:

```bash
python -m pytest
```

**Anwendung starten (im Repository-Hauptverzeichnis):**

```bash
python src/app.py
```

Danach ist die Anwendung lokal unter **http://127.0.0.1:5000** erreichbar. Der Start über `app.run(debug=True, port=5000)` ist für die lokale Entwicklung vorgesehen; den Debug-Modus nicht öffentlich betreiben.

## Technische Referenz: Datenmodell und API

Der Anwendungscode befindet sich in `src/app.py`; die Klassen `Plant`, `CareSchedule` und `ActionLog` sind in `src/models.py` definiert. Das HTML-/JavaScript-Frontend liegt unter `src/templates/` und `src/static/` und war im Rahmen der Aufgabenstellung vorgegeben. **Meine Entwicklungsaufgabe war die Flask-Backend-Implementierung.**

### REST-Endpunkte

| Methode | Pfad | Funktion |
|---|---|---|
| GET | `/api/plants` | Alle Pflanzen einschließlich ihres Status abrufen |
| POST | `/api/plants` | Pflanze anlegen |
| GET | `/api/plants/<id>` | Eine Pflanze abrufen |
| PUT | `/api/plants/<id>` | Pflanzeninformationen aktualisieren |
| DELETE | `/api/plants/<id>` | Pflanze löschen |
| GET | `/api/plants/<id>/schedules` | Pflegepläne abrufen |
| POST | `/api/plants/<id>/schedules` | Pflegeplan anlegen oder aktualisieren |
| DELETE | `/api/plants/<id>/schedules/<care_type>` | Pflegeplan für einen Pflegetyp entfernen |
| GET | `/api/plants/<id>/logs` | Pflegeprotokoll abrufen |
| POST | `/api/plants/<id>/logs` | Pflegeaktivität dokumentieren |
| GET | `/api/plants/<id>/next-actions` | Nächste fällige Pflegeaufgaben berechnen |
| GET | `/api/overdue` | Überfällige Pflegeaufgaben aller Pflanzen abrufen |

Der HTML-Einstiegspunkt ist zusätzlich unter `/` erreichbar. Die API verarbeitet JSON-Anfragen beziehungsweise JSON-Antworten. Für Pflegepläne sind die Typen `watering`, `fertilizing` und `repotting` vorgesehen.

### Termin- und Statuslogik

Das nächste Fälligkeitsdatum wird anhand der letzten protokollierten Aktivität und des hinterlegten Pflegeintervalls berechnet; falls noch kein Protokoll existiert, dient das Erstellungsdatum der Pflanze als Ausgangspunkt. Der berechnete Pflanzenstatus unterscheidet zwischen `ok`, `soon` und `overdue`.

### Datenhaltung und Tests

Teil 1 verwendet **In-Memory-Datenhaltung**. Nach einem Neustart der Anwendung müssen bisher angelegte Pflanzen daher nicht mehr vorhanden sein. Die Tests befinden sich unter `tests/`; `pytest.ini` setzt den Python-Pfad auf `src`. Zum lokalen Testen aus dem Repository-Hauptverzeichnis:

```bash
python -m pytest
```

Die vorhandene `requirements.txt` enthält Flask, Flask-CORS, pytest, pytest-cov und pytest-mock. Die separate [API-Spezifikation](ProjectDescription.md) beschreibt Datenfelder und erwartete Antworten im Detail.

## KI-Unterstützung

Während des Projekts verwendete ich ChatGPT als Lern- und Entwicklungsunterstützung.

Besonders hilfreich war die Unterstützung beim Verständnis von REST-APIs, Python- und Flask-Konzepten, automatisierten Tests sowie bei der Untersuchung technischer Fehlermeldungen.

Der KI-Einsatz wurde entsprechend den Anforderungen des Hochschulmoduls dokumentiert.

Mein Ziel war es, die vorgeschlagenen Lösungen kritisch zu prüfen, ihre Funktionsweise nachzuvollziehen und mein eigenständiges Programmierverständnis weiterzuentwickeln.

## Projektkontext

**Hochschule:** Hochschule München  
**Studiengang:** Informatik & Design (B.Sc.)  
**Modul:** Software Engineering  
**Semester:** Sommersemester 2026  
**Projektform:** Einzelarbeit  
**Status:** Abgeschlossen

## Weiterentwicklung

Im zweiten Teil der Modularbeit wurde der Pflanzenkalender als Teamprojekt weiterentwickelt.

Dabei kamen unter anderem Benutzerregistrierung, JWT-basierte Anmeldung und Zugriffsschutz für benutzerspezifische Daten hinzu.

**[Pflanzenkalender – Teil 2 auf GitHub](https://github.com/Annika-Ostendorp/pflanzenkalender-teil-2)**
