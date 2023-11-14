from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import numpy


def row_keyboard(items: list[str], chunk_size: int) -> ReplyKeyboardMarkup:
    """
    Создаём клавиатуру
    :param items: список текстов для кнопок
    :return: объект клавиатуру
    """

    row = [KeyboardButton(text=item) for item in items]

    chunks = numpy.array_split(row, chunk_size)
    
    return ReplyKeyboardMarkup(keyboard=(chunks))
