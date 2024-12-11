import os
import random
from pathlib import Path
from PIL import Image
from io import BytesIO
from aiogram.types import InputFile

from loader import dp
from module.TinyDB.config import Query, db_users

from config import QR_DIR, QR_TEMPLATE



