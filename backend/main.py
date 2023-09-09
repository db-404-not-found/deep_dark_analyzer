from backend.config import Settings
from backend.factory import setup_app

settings = Settings()
app = setup_app(settings)
