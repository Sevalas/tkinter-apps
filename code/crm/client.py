from dataclasses import dataclass

@dataclass
class Client:
    id: int = None
    names: str = None
    phone: str = None
    enterprise: str = None
    creation_date: str = None