class VisitStorage:
    def __init__(self):
        self.storage = {}

    def save(self, visit_id: str, utm_data: dict):
        self.storage[visit_id] = utm_data

    def get_and_delete(self, visit_id: str) -> dict:
        data = self.storage.get(visit_id)
        if data:
            del self.storage[visit_id]
        return data
