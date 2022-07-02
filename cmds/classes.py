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


class MergePdf(StatesGroup):
	folder = State()
	file_name = State()
	temp = State()


class MergeImages(StatesGroup):
	folder = State()
	file_name = State()
	temp = State()


class AddNewFile(StatesGroup):
	file_name = State()
	file_path = State()


class AddNewExtraFile(StatesGroup):
	file_name = State()
	file_path = State()


class Del_File(StatesGroup):
	temp = State()


class Del_Extra_File(StatesGroup):
	temp = State()


class GetBook(StatesGroup):
	temp = State()


class GetFile(StatesGroup):
	temp = State()


class AddNewUser(StatesGroup):
	uid = State()


class DelUser(StatesGroup):
	uid = State()

class ChangeStage(StatesGroup):
	stage = State()
	old_stage = State()
