from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import numpy

def row_keyboard(items: list[str], chunk_size: int) -> ReplyKeyboardMarkup:
    """
    Создаём клавиатуру, метод 1, извращенный
    :param items: список лейблов кнопок
    :param chunk_size: степень разбиения кнопок
    :return: объект клавиатуры (ReplyKeyboardMarkup)
    """

    row = [KeyboardButton(text=item) for item in items]
    chunks = numpy.array_split(row, chunk_size)
    return ReplyKeyboardMarkup(keyboard=(chunks), resize_keyboard=True)

def custom_keyboard(text: list[str], adjust: int) -> ReplyKeyboardMarkup:
    """
    Создаём клавиатуру, метод 2, штатный
    :param text: список лейблов кнопок
    :param adjust: количество кнопок в строке
    :return: объект клавиатуры (ReplyKeyboardMarkup)
    """
    builder = ReplyKeyboardBuilder()
    for item in text:
        builder.add(KeyboardButton(text=str(item)))
    builder.adjust(adjust)
    return builder.as_markup(resize_keyboard=True)

def inline_button_builder(text: str, data: str) -> InlineKeyboardMarkup:
    """
    Создаём inline-кнопку
    :param text: лейбл кнопки
    :param data: callback-функция кнопки
    :return: объект клавиатуры (InlineKeyboardMarkup)
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=str(text),
        callback_data=str(data))
    )
    return builder.as_markup()