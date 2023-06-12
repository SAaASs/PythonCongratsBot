import asyncio
import logging
import openai
from project import createImage
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, date, time, timedelta
import codecs
import threading
test_photo = FSInputFile("da-poebat-mne-gosling-18.jpg")
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
congrat_query = 'Придумай поздравление от учебного коллектива для студента с именем {0}, длинной 20-30 слов, без использования слов любовь, коллеги, дорог, юбилей, обращайся на ты'
nov = datetime.now()
logging.basicConfig(level=logging.INFO)
token = "6087945888:AAFRDGzwQ9O1fFE3E74FtEAx84QY0WQDiHc"
bot = Bot(token)
dp = Dispatcher()
today_congrats = []
redo_congrats = []
manual_congrat_id = "-----------------------------------------------------------------------------"

f = open("data.csv", encoding='utf-8')
data = [i.strip().split(';') for i in f.readlines()]
data.pop(0)
data.pop(0)
while ['', '', '', '', ''] in data:
    data.pop(data.index(['', '', '', '', '']))


class AdminStates(StatesGroup):
    writing_congrat = State()
    standart_state = State()


async def create_congrat(msg_for_chat_gpt: str):
    openai.api_key = "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"
    model = "gpt-3.5-turbo"
    data_openai = [{"role": "user", "content": msg_for_chat_gpt}]
    response = openai.ChatCompletion.create(model=model, messages=data_openai)
    return response.choices[0].message.content


def check_date():
    curr_date = date.today()
    curr_day = curr_date.day
    curr_month = curr_date.month

    for i in range(0, len(data)):
        bdaydate = datetime.strptime(data[i][2], '%d.%m.%Y')
        dd = bdaydate.day
        mm = bdaydate.month
        if curr_day == dd and curr_month == mm:
            name = data[i][1].split(' ')[1]
            lastname = data[i][1].split(' ')[0]
            group = "Академия ВИШ"
            today_congrats.append(
                [asyncio.run(create_congrat(congrat_query.format(name))), name, lastname, BufferedInputFile(createImage(name,lastname,group), filename="name343422") ,-1001956903015, i])


async def cmd_start(current_congrats):
    for i in range(0, len(current_congrats)):
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Подтвердить",
            callback_data="Send_" + str(current_congrats[i][-1]))
        )
        builder.add(types.InlineKeyboardButton(
            text="Переделать",
            callback_data="ReDo_" + str(current_congrats[i][-1]))
        )
        builder.add(types.InlineKeyboardButton(
            text="Отправить вручную",
            callback_data="SendManually_" + str(current_congrats[i][-1]))
        )
        await bot.send_photo(487539481, current_congrats[i][3], caption=current_congrats[i][0], reply_markup=builder.as_markup())
    await bot.session.close()


@dp.callback_query(F.data.startswith("Send_"))
async def r1(callback: types.CallbackQuery):
    target_text_id = int(callback.data.split("_")[1])
    for i in range(0, len(today_congrats)):
        if today_congrats[i][-1] == target_text_id:
            await bot.send_photo(today_congrats[i][-2], today_congrats[i][3] , caption=today_congrats[i][0])


@dp.callback_query(F.data.startswith("SendManually_"))
async def r2(callback: types.CallbackQuery, state: FSMContext):
    global manual_congrat_id
    manual_congrat_id = int(callback.data.split("_")[1])
    await state.set_state(AdminStates.writing_congrat)


@dp.callback_query(F.data.startswith("ReDo_"))
async def r3(callback: types.CallbackQuery):
    target_text_id = int(callback.data.split("_")[1])
    for i in range(0, len(today_congrats)):
        if today_congrats[i][-1] == target_text_id:
            redo_congrats.append(
                [await create_congrat(congrat_query.format(today_congrats[i][1])), today_congrats[i][1],
                 today_congrats[i][2], today_congrats[i][3], today_congrats[i][4], today_congrats[i][5]])
            await cmd_start(redo_congrats)
    redo_congrats.clear()


@dp.message(AdminStates.writing_congrat)
async def Send_manual_congrat(message: types.Message, state: FSMContext):
    for i in range(0, len(today_congrats)):
        if today_congrats[i][-1] == manual_congrat_id:
            await bot.send_photo(today_congrats[i][-2], today_congrats[i][3], caption=message.text)
    await state.set_state(AdminStates.standart_state)



check_date()
asyncio.run(cmd_start(today_congrats))

#scheduler.add_job(check_date, 'cron', hour=21, minute='16')
#scheduler.add_job(cmd_start, 'cron', [today_congrats], hour=21, minute='17')


async def main():
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
