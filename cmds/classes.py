from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class AddManager(StatesGroup):
	stage = State()
	uid = State()

class DelManager(StatesGroup):
	stage = State()
	uid = State()

class AddHW(StatesGroup):
	day = State()
	hw = State()

class DelHW(StatesGroup):
	day = State()
	hw = State()

class Anno(StatesGroup):
	m = State()

class AnnoAll(StatesGroup):
	m = State()

class Viewhw(StatesGroup):
	day = State()