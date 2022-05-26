from datetime import datetime

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils import executor

from settings import TOKEN


class StatesInput(StatesGroup):
    message = State()
    name = State()
    date = State()


dp = Dispatcher(Bot(TOKEN), storage=MemoryStorage())


@dp.message_handler(commands=['start', 'new'])
async def command_start(message: Message, state: FSMContext):
    message_answer = await message.answer("Enter name")
    await state.update_data(message=message_answer)
    await StatesInput.name.set()


@dp.message_handler(state=StatesInput.name)
async def input_start(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    data = await state.get_data()
    await data['message'].delete()
    await message.delete()

    message_answer = await message.answer("Enter the date in the format DD.MM.YYYY or DDMMYYYY")
    await state.update_data(message=message_answer)

    await StatesInput.next()


@dp.message_handler(state=StatesInput.date)
async def input_end(message: Message, state: FSMContext):
    try:
        valid_date = datetime.strptime(message.text, '%d%m%Y').date()
        date_is_ok = True
    except ValueError:
        try:
            valid_date = datetime.strptime(message.text, '%d.%m.%Y').date()
            date_is_ok = True
        except ValueError:
            date_is_ok = False

    data = await state.get_data()
    await data['message'].delete()
    await message.delete()

    if date_is_ok:
        await state.update_data(date=valid_date)
        data = await state.get_data()
        await calculation(message, data)
        await state.finish()
    else:
        message_answer = await message.answer("Invalid date! Enter the date in the format DD.MM.YYYY")
        await state.update_data(message=message_answer)


async def calculation(message: Message, data):
    name = data['name']
    date = data['date'].strftime("%d%m%Y")

    calculation_number = ""
    for i in date:
        if i.isdigit() and int(i) > 0:
            calculation_number = calculation_number + i

    number1 = 0
    number2 = 0
    number3 = 0
    number4 = 0

    for i in calculation_number:
        number1 = number1 + int(i)

    for i in str(number1):
        number2 = number2 + int(i)

    number3 = str(abs(int(number1) - 2 * int(calculation_number[0])))

    for i in str(number3):
        number4 = number4 + int(i)

    finish_number = str(calculation_number) + str(number1) + str(number2) + str(number3) + str(number4)

    c = dict()
    for letter in finish_number:
        c[letter] = c.get(letter, 0) + 1

    column_length = max(c.items(), key=lambda item: item[1])[1] + 1

    symbol1 = finish_number.count("1")
    symbol2 = finish_number.count("2")
    symbol3 = finish_number.count("3")
    symbol4 = finish_number.count("4")
    symbol5 = finish_number.count("5")
    symbol6 = finish_number.count("6")
    symbol7 = finish_number.count("7")
    symbol8 = finish_number.count("8")
    symbol9 = finish_number.count("9")
    symbol0 = finish_number.count("0")

    horizontal_separator = '\n' + ('—' * ((column_length + 2) * 3 + 1)) + '\n'
    vertical_separator = '\| '

    result = horizontal_separator
    result += vertical_separator

    # 1
    for i in range(column_length):
        if i < symbol1:
            symbol = "1"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    for i in range(column_length):
        if i < symbol4:
            symbol = "4"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    for i in range(column_length):
        if i < symbol7:
            symbol = "7"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    # 2
    result = result + horizontal_separator
    result += vertical_separator

    for i in range(column_length):
        if i < symbol2:
            symbol = "2"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    for i in range(column_length):
        if i < symbol5:
            symbol = "5"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    for i in range(column_length):
        if i < symbol8:
            symbol = "8"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    # 3
    result = result + horizontal_separator
    result += vertical_separator

    for i in range(column_length):
        if i < symbol3:
            symbol = "3"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    for i in range(column_length):
        if i < symbol6:
            symbol = "6"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator

    for i in range(column_length):
        if i < symbol9:
            symbol = "9"
        else:
            symbol = " "
        result = result + symbol

    result += vertical_separator + horizontal_separator

    await message.answer(name + "`" + result + "`", parse_mode="MarkdownV2")


executor.start_polling(dp, skip_updates=True)
