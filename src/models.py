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
    
    @property # Property-Dekorator, um nicht immer Klammern mitschreiben zu müssen bei Methode -> auf Methode zugriefen wie auf normale Variablen
    def next_due(self) -> date:
        return self._next_due

    def to_json(self) -> dict:
        return {
            "id": self._id,
            "plant_id": self._plant_id,
            "care_type": self._care_type,
            "interval_days": self._interval_days,
            "next_due": str(self._next_due) # next_due hinzufügen für calculate_status Methode, damit Tests nicht fehlschlagen
        }