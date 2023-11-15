from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import numpy


def row_keyboard(items: list[str], chunk_size: int) -> ReplyKeyboardMarkup:
    """
    Создаём клавиатуру
    :param items: список лейблов для кнопок
    :param chunk_size: степень разбиения кнопок
    :return: объект клавиатуры
    """

    row = [KeyboardButton(text=item) for item in items]

    chunks = numpy.array_split(row, chunk_size)
    
    return ReplyKeyboardMarkup(keyboard=(chunks), resize_keyboard=True)
