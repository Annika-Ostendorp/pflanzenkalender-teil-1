from datetime import timedelta, date # timedelta, um Zeitdifferenz zwischen 2 Zeiten zu berechnen -> Tage, Stunden, Minuten, Sekunden addieren oder subtrahieren
                                             # wichtig für "soon" Status z.B.
                                             # date, um Datums-Bedingung (created_at) umzusetzen

class ActionLog:
    def __init__(self, id: int, plant_id: int, care_type: str, performed_at: date, notes: str) -> None:
        self._id = id
        self._plant_id = plant_id
        self._care_type = care_type
        self._performed_at = performed_at
        self._notes = notes

    def to_json(self) -> dict:
        return {
            "id": self._id,
            "plant_id": self._plant_id,
            "care_type": self._care_type,
            "performed_at": str(self._performed_at),
            "notes": self._notes
        }


class CareSchedule:
    def __init__(self, id: int, plant_id: int, care_type: str, interval_days: int, next_due: date) -> None:
        self._id = id
        self._plant_id = plant_id # Hinzufügen von fehlender plant_id Variable
        self._care_type = care_type
        self._interval_days = interval_days
        self._next_due = next_due
        self._plant = None # beim Erstellen hat Plan noch keine Pflanze -> damit Tests trotzdem nicht fehlschlagen
    
    @property # Property-Dekorator, um nicht immer Klammern mitschreiben zu müssen bei Methode -> auf Methode zugriefen wie auf normale Variablen
    def next_due(self) -> date:
        if self._plant is not None: # Pflanze wurde von außen übergeben -> Datumslogik berechnen
            last_log = None # Ausgangszustand, noch kein Protokoll angesehen

            for log in self._plant._logs:
                if log._care_type == self._care_type: # stimmt Log mit care_type von CareSchedule Objekt überein?
                    if last_log is None or log._performed_at > last_log._performed_at: # wenn noch kein Log gemerkt oder aktuelles Log neuer ist als das gemerkte
                        last_log = log # last_log nun das neuere log zuweisen

            if last_log is not None: # falls last_log vorhanden (Projektbeschreibung) -> Rechenlogik implementieren
                return last_log._performed_at + timedelta(days=self._interval_days)

            return self._plant._created_at + timedelta(days=self._interval_days)
    
        return self._next_due # trotzdem, damit Tests aus Sprint 1 nicht fehlschlagen


    def to_json(self) -> dict:
        return {
            "id": self._id,
            "plant_id": self._plant_id,
            "care_type": self._care_type,
            "interval_days": self._interval_days,
            "next_due": str(self.next_due) # next_due hinzufügen für calculate_status Methode, damit Tests nicht fehlschlagen
        }
    

class Plant:
    def __init__(self, id: int, name: str, species: str, location: str, created_at: date) -> None:
        self._id = id
        self._name = name
        self._species = species
        self._location = location
        self._created_at = created_at
        self._schedules = [] # Liste mit CareSchedule Objekten
        self._logs = [] # Liste mit ActionLog Objekten
    
    def to_json(self) -> dict: # Nutzen to_json, um Zugriff auf private Member-Variablen von Klasse Plant zu bekommen für JSON-Ausgabe
        for schedule in self._schedules: # damit dann jedes CareSchedule-Objekt Zugriff/Referenz auf Daten dieser Pflanze
            schedule._plant = self

        return {
            "id": self._id,
            "name": self._name,
            "species": self._species,
            "location": self._location,
            "created_at": str(self._created_at), # in string umwandeln für richtige Ausgabe 
            "status": self.calculate_status(),
            "schedules": [schedule.to_json() for schedule in self._schedules], # jedes Objekt in der Liste soll zu einem Dictionary umgewandelt werden, und trotzdem leere Listen ausgeben für Variablen schedules, logs falls es diese nicht gibt 
                                                                               # --> bessere Darstellung/ Struktur, um Pflanzen zusammen mit ihren Pflegeplänen etc. anzuzeigen
            "logs": [log.to_json() for log in self._logs]
        }
    
    def calculate_status(self) -> str:
        for schedule in self._schedules: # auch hier verknüpft, damit gerechnet werden kann -> nicht stored sondern calculated
            schedule._plant = self

        today = date.today() # heutiges Datum als Bsp. festlegen, damit Berechnung für z.B. "overdue"-Logik funktioniert
        three_days_from_now = today + timedelta(days = 3)

        for schedule in self._schedules: # erst alles prüfen, ob etwas "overdue" ist
            if schedule.next_due < today: # wenn mind. eine Aktion schon überfällig ist  
                return "overdue"

        for schedule in self._schedules: # danach prüfen, ob etwas "soon" ist
            if schedule.next_due <= three_days_from_now: # wenn mind. eine Aktion in 3 oder weniger Tagen fällig ist
                return "soon"
        
        return "ok" # wenn alle Aktionen mehr als 3 Tage in der Zukunft liegt -> wenn 2 Schleifen durchgelaufen, aber keine Übereinstimmung gefunden haben   