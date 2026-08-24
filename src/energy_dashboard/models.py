from dataclasses import dataclass
from datetime import datetime

@dataclass
class Rilevazione:
    zona: str
    data: datetime
    fonte: str
    valore_mw: float
    tipo_business: str

    def to_tuple(self):
        return (self.zona, self.data, self.fonte, self.valore_mw, self.tipo_business)