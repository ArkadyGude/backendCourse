from src.repositores.base import BaseRepository
from src.models.rooms import RoomsOrm

class RoomsRepository(BaseRepository):
    model = RoomsOrm