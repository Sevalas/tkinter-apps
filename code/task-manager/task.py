class Task:
    def __init__(self, id=None, created_at=None, description=None, status=False):
        self.id = id
        self.created_at = created_at
        self.description = description
        self.status = status