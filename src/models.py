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