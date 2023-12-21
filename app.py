import re
import os
import aiohttp
from fake_useragent import UserAgent
import logging
import asyncio
import json
import time
import uuid
import openai_async
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
import requests
import db
from PIL import Image

bot = Bot(token="") #тут токен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

async def anti_flood_gpt(*args, **kwargs):
    message = args[0]
    await message.reply("Лимит использования данной функции раз в 25 секунд!")
    pass

async def anti_flood(*args, **kwargs):
    message = args[0]
    pass
    
@dp.message_handler(commands="start")
@dp.throttled(anti_flood,rate=3)
async def start(message: types.Message):
    if message.chat.type == 'private':
        check_fun = db.get_status_work('start')
        if str(check_fun) == 'no work':
            await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
        elif str(check_fun) == 'off':
            await message.reply(f"Данная функция была переведена в режим тех работ!")
        else:
            print(f"[LOG] - id[{message.from_user.id}] использует команду /start")
            result = db.check_ban_user(message.from_user.id)
            print(f"[LOG] - id[{message.from_user.id}] Проверка на бан")
            if str(result[0]) == '0':
                await bot.send_message(message.chat.id, f"Привет, я бот ChatGPT созданый для работы только в группах.\nРазработчик: @CTOHKC")
            else:
                await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
    else:
        pass
   
@dp.message_handler(commands="balaboba")
async def balaboba(message: types.Message):
    if message.chat.type != 'private':
        check_fun = db.get_status_work('balaboba')
        if str(check_fun) == 'no work':
            await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
        elif str(check_fun) == 'off':
            await message.reply(f"Данная функция была переведена в режим тех работ!")
        else:
            result = db.check_ban_user(message.from_user.id)
            result2 = db.check_ban_chat(message.chat.id)
            if str(result[0]) != '1' and (result2[0]) != '1':
                if message.get_args():
                    print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Используется /balaboba text[{message.get_args()}]")
                    try:
                        headers = {
                            'Content-Type': 'application/json',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                                          '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                            'Origin': 'https://yandex.ru',
                            'Referer': 'https://yandex.ru/',
                        }

                        API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
                        payload = {"query": f"{message.get_args()}", "intro": 0, "filter": 1}
                        async with aiohttp.ClientSession() as session:
                            async with session.post(API_URL, json=payload, headers=headers) as response:
                                result = await response.json()
                                if result['text'] != "":
                                    await message.reply(f"Balaboba: {result['text']}")
                                else:
                                    await message.reply(f"Ошибка генерации!\nСкорее всего вы использовали мат или нарушили правила использования.")
                    except Exception as er:
                        await message.reply(f"Ошибка: {er}")
                else:
                    await message.reply(f"Я без аргумента не работаю😡")
                    
            elif str(result2[0]) == '1':
                try:
                    await message.reply(f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
            elif str(result[0]) == '1':
                try:
                    await message.reply(f"Вы находитесь в черном списке!")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
   
@dp.message_handler(commands="status")
@dp.throttled(anti_flood,rate=3)
async def dreams(message: types.Message):
    if message.chat.type != 'private':
        result = db.check_ban_user(message.from_user.id)
        result2 = db.check_ban_chat(message.chat.id)
        if str(result[0]) != '1' and (result2[0]) != '1':
            results = db.count()
            if results >= 1:
                stat_work = "Все работает!"
            if results == 0:
                stat_work = "Все плохо!"
            await message.reply(f"<b>Статус:</b> {stat_work}\n<b>Всего ключей осталось:</b> {results}", parse_mode="HTML")
   
@dp.message_handler(commands="dream")
@dp.throttled(anti_flood,rate=3)
async def dreams(message: types.Message):
    if message.chat.type != 'private':
        check_fun = db.get_status_work('dream')
        if str(check_fun) == 'no work':
            await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
        elif str(check_fun) == 'off':
            await message.reply(f"Данная функция была переведена в режим тех работ!")
        else:
            result = db.check_ban_user(message.from_user.id)
            result2 = db.check_ban_chat(message.chat.id)
            if str(result[0]) != '1' and (result2[0]) != '1':
                if message.get_args():
                    print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Используется /dream text[{message.get_args()}]")
                    try:
                        limits = db.get_limit_dream(message.chat.id)
                        if int(limits)+1 <= len(message.get_args()):
                            await message.reply(f"Вы не можете отправлять сообщения больше {str(limits)} символов!")
                            pass
                        else:
                            for i in range(5):
                                try:
                                    random_uuid = uuid.uuid4()
                                    uuid_str = str(random_uuid).replace('-', '')
                                    formatted_uuid = f"{uuid_str[0:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:20]}-{uuid_str[20:]}"
                                    user_agent = UserAgent()
                                    random_user_agent = user_agent.random
                                    print(random_user_agent)

                                    headers = {
                                        'Accept': '*/*',
                                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                        'Connection': 'keep-alive',
                                        'Content-Type': 'application/json',
                                        'Origin': 'https://dreaminterpreter.ai',
                                        'Referer': 'https://dreaminterpreter.ai/',
                                        'Sec-Fetch-Dest': 'empty',
                                        'Sec-Fetch-Mode': 'cors',
                                        'Sec-Fetch-Site': 'cross-site',
                                        'User-Agent': f'{random_user_agent}',
                                        'country': 'RU',
                                        'language': 'ru',
                                        'sec-ch-ua': '"Chromium";v="112", "Not_A Brand";v="24", "Opera";v="98"',
                                        'sec-ch-ua-mobile': '?0',
                                        'sec-ch-ua-platform': '"Windows"',
                                        'uid': f'{formatted_uuid}',
                                    }

                                    json_data = {
                                        'dream': f'{message.get_args()}',
                                        'lat': None,
                                        'long': None,
                                    }
                                    
                                    async with aiohttp.ClientSession(headers=headers) as session:
                                        async with session.post('https://dream-interpreter-ai.herokuapp.com/dream', json=json_data) as response:
                                            result = await response.json()
                                            await message.reply(f"{result['dream']['interpretation']}")
                                            return
                                            break
                                except Exception as er:
                                    print(f"[ERROR] - {er}")
                                    continue
                            await message.reply(f"Ошибка генерации!\nС чем это может быть связано:\n1.Ваш запрос слишком короткий\n2.Нейронная сеть перегружена\n3.Вы использовали запрещенные выражения")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                else:
                    await message.reply(f"Я без аргумента не работаю😡")
                    
            elif str(result2[0]) == '1':
                try:
                    await message.reply(f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
            elif str(result[0]) == '1':
                try:
                    await message.reply(f"Вы находитесь в черном списке!")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
                    
                    
@dp.message_handler(commands="img")
@dp.throttled(anti_flood,rate=3)
async def img(message: types.Message):
    if message.chat.type != 'private':
        check_fun = db.get_status_work('img')
        if str(check_fun) == 'no work':
            await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
        elif str(check_fun) == 'off':
            await message.reply(f"Данная функция была переведена в режим тех работ!")
        else:
            result = db.check_ban_user(message.from_user.id)
            result2 = db.check_ban_chat(message.chat.id)
            if str(result[0]) != '1' and (result2[0]) != '1':
                if message.get_args():
                    print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Используется /img text[{message.get_args()}]")
                    try:
                        limits = db.get_limit_img(message.chat.id)
                        if int(limits)+1 <= len(message.get_args()):
                            await message.reply(f"Вы не можете отправлять сообщения больше {str(limits)} символов!")
                            pass
                        else:
                            result = await img_generate(message.get_args())
                            if result == 'error':
                                await message.reply(f"Не удалось сгенерировать изображение!")
                                pass
                            if result == 'no key':
                                await message.reply(f"В данный момент закончились api ключи!\nВы можете добавить свой ключ используя команду /token <key>")
                                pass
                            else:
                                await bot.send_photo(message.chat.id, result, caption=f'Текст для генерации: {message.get_args()}')
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                        
                else:
                    await message.reply(f"Я без аргумента не работаю😡")
                    pass
                    
            elif str(result2[0]) == '1':
                try:
                    await message.reply(f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
            elif str(result[0]) == '1':
                try:
                    await message.reply(f"Вы находитесь в черном списке!")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
        
@dp.message_handler(content_types=["photo"]) #Этот фрагмент забагован и не работает корректно!
@dp.throttled(anti_flood,rate=3)
async def photo_edit(message):
    if message.chat.type != "private":
        if message.caption and message.caption == "/edit":
            check_fun = db.get_status_work('photo')
            if str(check_fun) == 'no work':
                await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
            elif str(check_fun) == 'off':
                await message.reply(f"Данная функция была переведена в режим тех работ!")
            else:
                print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Проверка на бан")
                result = db.check_ban_user(message.from_user.id)
                result2 = db.check_ban_chat(message.chat.id)
                if str(result[0]) != '1' and (result2[0]) != '1':
                    try:
                        print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Используется /edit")
                        await message.photo[-1].download(f'{message.from_user.id}.jpg')
                        im = Image.open(f'{message.from_user.id}.jpg')
                        new_image = im.resize((1024, 1024))
                        new_image.save(f'{message.from_user.id}.png')
                        result = await edit_photo(image=open(f"{message.from_user.id}.png", 'rb').read(), n=2, size="1024x1024")
                        if result == 'no key':
                            await message.reply(f"В данный момент закончились api ключи!\nВы можете добавить свой ключ используя команду /token <key>")
                        if result == 'error':
                            await message.reply(f"Ошибка редактирования!")
                        else:
                            await bot.send_photo(message.chat.id, result[0], caption=f'Успешно отредактировано!\n(Фото было ужато до формата 1024х1024)')
                        
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                elif str(result2[0]) == '1':
                    try:
                        await message.answer(f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                    except:
                        try:
                            await bot.send_message(message.chat.id, f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                        except Exception as er:
                            print(f"[ERROR] - {er}")
                    pass
                elif str(result[0]) == '1':
                    try:
                        await message.answer(f"Вы находитесь в черном списке!")
                    except:
                        try:
                            await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
                        except Exception as er:
                            print(f"[ERROR] - {er}")
                pass
        else:
            pass
            
    elif message.caption and "/mailing" in message.caption:
        check = db.check_adm(message.from_user.id)
        if str(check) == '2':
            await message.photo[-1].download(f'mailing_photo.jpg')
            text_mailing = message.caption.replace('/mailing', '')
            msg = await bot.send_message(message.chat.id, 'Начинаю рассылку...')
            row = db.receive_chats()
            good = 0
            bad = 0
            for result in row:
                with open('mailing_photo.jpg', 'rb') as photos:
                    try:
                        await bot.send_photo(result[1], photos, caption=f'{text_mailing}', parse_mode="HTML")
                        print(f"[MAILING] - id[{result[1]}] Успешно отправлено сообщение")
                        good = good + 1
                    except Exception as er:
                        print(f"[MAILING] - id[{result[1]}] Ошибка отправки сообщения [{er}]")
                        bad = bad + 1
                    await asyncio.sleep(1)
            await msg.edit_text(f"Рассылка окончена!\n✅Успешно: {good}\n⛔️Ошибок: {bad}")
        
@dp.message_handler(commands="mailing")
@dp.throttled(anti_flood,rate=30)
async def mailing(message: types.Message):
    check = db.check_adm(message.from_user.id)
    if str(check) == '2':
        print(f"[ADMIN] - id[{message.from_user.id}] chat[{message.chat.id}] Использовал /mailing")
        if message.get_args():
            msg = await bot.send_message(message.chat.id, 'Начинаю рассылку...')
            row = db.receive_chats()
            print(f'[LOG] - Ответ базы данных [{row}]')
            good = 0
            bad = 0
            progress = len(row)
            for result in row:
                try:
                    await bot.send_message(result[1], f'{message.get_args()}', parse_mode="HTML")
                    print(f"[MAILING] - id[{result[1]}] Успешно отправлено сообщение")
                    good = good + 1
                except Exception as er:
                    print(f"[MAILING] - id[{result[1]}] Ошибка отправки сообщения error[{er}]")
                    bad = bad + 1
                await asyncio.sleep(1)
            await msg.edit_text(f"Рассылка окончена!\n✅Успешно: {good}\n⛔️Ошибок: {bad}")
                
        else:
            await bot.send_message(message.chat.id, 'Текст для рассылки не может быть пустым!')
            pass
    else:
        pass
        
@dp.message_handler(commands="set_func")
@dp.throttled(anti_flood,rate=3)
async def set_limit(message: types.Message):
    check = db.check_adm(message.from_user.id)
    if str(check) == '2':
        if message.chat.type != 'private':
            try:
                result = db.set_status_work(f'{message.get_args()}')
                if result == 'off':
                    await message.reply(f"Функция {message.get_args()} была успешно переведена на тех работы!")
                elif result == 'on':
                    await message.reply(f"Функция {message.get_args()} была успешно переведена в рабочий режим!")
                elif result == 'error':
                    await message.reply(f"Ошибка!")
            except Exception as er:
                print(f'[ERROR] - {er}')
    else:
        pass
        
@dp.message_handler(commands="set_limit")
@dp.throttled(anti_flood,rate=3)
async def set_limit(message: types.Message):
    check = db.check_adm(message.from_user.id)
    if str(check) == '2' or str(check) == '1':
        if message.chat.type != 'private':
            try:
                types = message.get_args().split(' ')[0] #Люблю аню
                limit = message.get_args().split(' ')[1]
                if int(limit) >= 3001:
                    await bot.send_message(message.chat.id, f"Максиальное значение лимитов 3000!")
                else:
                    result = db.edit_limit(message.chat.id, types, int(limit))
                    if result == 'good':
                        await bot.send_message(message.chat.id, f"Лимиты были успешно изменены!")
                    else:
                        await bot.send_message(message.chat.id, f"Ошибка изменения лимитов!")
            except Exception as er:
                await bot.send_message(message.chat.id, f"Ошибка изменения лимитов!")
                print(f"[ERROR] - {er}")
    else:
        pass
   
@dp.message_handler(commands="token")
@dp.throttled(anti_flood,rate=3)
async def token(message: types.Message):
    if message.chat.type != 'private':
        check_fun = db.get_status_work('token')
        if str(check_fun) == 'no work':
            await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
        elif str(check_fun) == 'off':
            await message.reply(f"Данная функция была переведена в режим тех работ")
        else:
            print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Проверка на бан")
            result = db.check_ban_user(message.from_user.id)
            result2 = db.check_ban_chat(message.chat.id)
            if str(result[0]) != '1' and (result2[0]) != '1':
                if message.get_args():
                    regex = r'sk-[a-zA-Z0-9]{48}'
                    matches = re.findall(regex, message.get_args())
                    msg_check = await bot.send_message(message.chat.id, f"Начал проверку...")
                    text = "Результат проверки:\n"
                    for match in matches:
                        try:
                            response = await openai_async.complete(f"{match}", timeout=2, payload={"model": "text-davinci-002", "prompt": "What is the capital of France?"})
                            check = response.json()["choices"][0]["text"].strip()
                            db.add_token(match)
                            text = text + f"[✅] {match[:8]}******** - Успешно добавлен!\n"
                        except Exception as er:
                            try:
                                error = response.json()["error"]["message"]
                                text = text + f"[⛔️]{match[:8]}******** - Ошибка: {error}!\n\n"
                            except:
                                text = text + f"[⛔️]{match[:8]}******** - Ошибка!\n"
                        await msg_check.edit_text(text)
                else:
                    await message.answer(f"Токен не указан!")
            elif str(result2[0]) == '1':
                try:
                    await message.answer(f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
            elif str(result[0]) == '1':
                try:
                    await message.answer(f"Вы находитесь в черном списке!")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
    else:
        pass 
            
@dp.message_handler(commands="chat")
@dp.throttled(anti_flood,rate=3)
async def chat(message: types.Message):
    if message.chat.type != 'private':
        check_fun = db.get_status_work('chat')
        if str(check_fun) == 'no work':
            await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
        elif str(check_fun) == 'off':
            await message.reply(f"Данная функция была переведена в режим тех работ")
        else:
            print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Проверка на бан")
            result = db.check_ban_user(message.from_user.id)
            result2 = db.check_ban_chat(message.chat.id)
            if str(result[0]) != '1' and (result2[0]) != '1':
                if message.get_args():
                    limits = db.get_limit_chat(message.chat.id)
                    if int(limits)+1 <= len(message.get_args()):
                        await message.reply(f"Вы не можете отправлять сообщения больше {str(limits)} символов!")
                        pass
                    else:
                        work = await chat_respons(message.get_args())
                        print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] запрос чата text[{message.get_args()}]")
                        if work == 'no key':
                            await message.reply(f"В данный момент закончились api ключи!\nВы можете добавить свой ключ используя команду /token <key>")
                            pass
                        else:
                            await message.reply(f"ChatGPT: {work}")
                else:
                    await message.reply(f"Я без аргумента не работаю😡")
            elif str(result2[0]) == '1':
                try:
                    await message.reply(f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
            elif str(result[0]) == '1':
                try:
                    await message.reply(f"Вы находитесь в черном списке!")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
    else:
        pass
        
@dp.message_handler(commands="gpt")
@dp.throttled(anti_flood_gpt,rate=25)
async def gpt_chat(message: types.Message):
    if message.chat.type != 'private':
        check_fun = db.get_status_work('gpt')
        if str(check_fun) == 'no work':
            await message.reply(f"У бота отпуск🏕🌅🛶!\n(Тех Работы)")
        elif str(check_fun) == 'off':
            await message.reply(f"Данная функция была переведена в режим тех работ")
        else:
            print(f"[LOG] - id[{message.from_user.id}] chat[{message.chat.id}] Проверка на бан")
            result = db.check_ban_user(message.from_user.id)
            result2 = db.check_ban_chat(message.chat.id)
            if str(result[0]) != '1' and (result2[0]) != '1':
                if message.get_args():
                    limits = db.get_limit_chat(message.chat.id)
                    if int(limits)+1 <= len(message.get_args()):
                        await message.reply(f"Вы не можете отправлять сообщения больше {str(limits)} символов!")
                        pass
                    else:
                        work = await gpt(message.get_args())
                        if work == 'no key':
                            await message.reply(f"В данный момент закончились api ключи!\nВы можете добавить свой ключ используя команду /token <key>")
                            pass
                        else:
                            await message.reply(f"ChatGPT: {work}")
                else:
                    await message.reply(f"Я без аргумента не работаю😡")
            elif str(result2[0]) == '1':
                try:
                    await message.reply(f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTPHKC")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Ваш чат был заблокирован!\nЭто ошибка? Обратитесь к @CTOHKC!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
            elif str(result[0]) == '1':
                try:
                    await message.reply(f"Вы находитесь в черном списке!")
                except:
                    try:
                        await bot.send_message(message.chat.id, f"Вы находитесь в черном списке!")
                    except Exception as er:
                        print(f"[ERROR] - {er}")
                pass
    else:
        pass
    
@dp.message_handler(commands="cfg")
@dp.throttled(anti_flood,rate=3)
async def cfg(message: types.Message):
    if message.chat.type != 'private':
        limits_chat = db.get_limit_chat(message.chat.id)
        limits_img = db.get_limit_img(message.chat.id)
        limits_dream = db.get_limit_dream(message.chat.id)
        ban = db.check_ban_chat(message.chat.id)
        if str(ban[0]) == "1":
            status = "Заблокирован"
        else:
            status = "Не заблокирован"
        await bot.send_message(message.chat.id, f"<b>Конфигурация данного чата</b>\n\n<b>Идентификатор чата:</b> <code>{message.chat.id}</code>\n<b>Лимит символов на /chat:</b> <code>{limits_chat}</code>\n<b>Лимит символов на /img:</b> <code>{limits_img}</code>\n<b>Лимит символов на /dream:</b> <code>{limits_dream}</code>\n<b>Статус блокировки:</b> <code>{status}</code>", parse_mode="HTML")
    else:
        pass
    
@dp.message_handler(commands="delmoder")
@dp.throttled(anti_flood,rate=3)
async def del_moder(message: types.Message):
    check = db.check_adm(message.from_user.id)
    if str(check) == '2':
        try:
            target = message.reply_to_message.from_user.id
        except:
            try:
                target = message.get_args()
            except Exception as er:
                print(f"[ERROR] - {er}")
                pass
        result = db.del_moderator(target)
        if result == 'good':
            await message.reply(f"Модератор успешно снят с должности!")
        if result == 'bad':
            await message.reply(f"Пользователь не являлся модератором!")
        print(f"[ADMIN] - id[{message.from_user.id}] Использовал удаление админа с конфы на юзере [{target}]")
    if str(check) == '1':
        print(f"[ADMIN] - id[{message.from_user.id}] попытался убрать админа [{target}]")
        await message.reply(f"У вас не достаточно прав!")
    else:
        pass
    
@dp.message_handler(commands="addmoder")
@dp.throttled(anti_flood,rate=3)
async def add_moder(message: types.Message):
    check = db.check_adm(message.from_user.id)
    if str(check) == '2':
        try:
            target = message.reply_to_message.from_user.id
        except:
            try:
                target = message.get_args()
            except Exception as er:
                print(f"[ERROR] - {er}")
                pass
        result = db.add_moderator(target)
        if result == 'good':
            await message.reply(f"Пользователь успешно добавлен состав модерации!")
        if result == 'already':
            await message.reply(f"Пользователь уже является модератором!")
        print(f"[ADMIN] - id[{message.from_user.id}] Использовал добавление админа в конфу на юзере [{target}]")
    if str(check) == '1':
        print(f"[ADMIN] - id[{message.from_user.id}] попытался сделать админом [{target}]")
        await message.reply(f"У вас не достаточно прав!")
    else:
        pass
        
@dp.message_handler(commands="ban")
@dp.throttled(anti_flood,rate=3)
async def ban(message: types.Message):
    check = db.check_adm(message.from_user.id)
    if str(check) == '1' or str(check) == '2':
        try:
            target = message.reply_to_message.from_user.id
        except:
            try:
                target = message.get_args()
            except Exception as er:
                print(f"[ERROR] - {er}")
        result = db.ban(target)
        if result == 'no user':
            await message.reply(f"Вы не можете заблокировать пользователя который не использовал бота!")
        if result == 'good':
            await message.reply(f"Пользователь успешно заблокирован!")
        if result == 'admin':
            await message.reply(f"Пользователь является частью админ состава!")
        if result == 'already':
            await message.reply(f"Пользователь уже находится в черном списке!")
        print(f"[ADMIN] - id[{message.from_user.id}] Использовал бан на юзера [{target}]")
    else:
        pass
        
@dp.message_handler(commands="unban")
@dp.throttled(anti_flood,rate=3)
async def unban(message: types.Message):
    check = db.check_adm(message.from_user.id)
    if str(check) == '1' or str(check) == '2':
        try:
            target = message.reply_to_message.from_user.id
        except:
            try:
                target = message.get_args()
            except Exception as er:
                print(f"[ERROR] - {er}")
        result = db.unban(target)
        if result == 'no user':
            await message.reply(f"Данный пользователь не использовал бота!")
        if result == 'good':
            await message.reply(f"Пользователь успешно разблокирован!")
        if result == 'admin':
            await message.reply(f"Пользователь является частью админ состава!")
        if result == 'already':
            await message.reply(f"Пользователь не находится в черном списке!")
        print(f"[ADMIN] - id[{message.from_user.id}] Использовал разбан на юзера [{target}]")
    else:
        pass

async def img_generate(text):
    print(f"[LOG] - Делаю запрос в опенАи /img")
    while True:
        keys = db.get_key()
        if keys == 'no key':
            return 'no key'
            break
        response = await openai_async.generate_img(
            f"{keys}",
            timeout=30,
            payload={
                "prompt": f"{text}",
                "n": 1
            },
        )
        try:
            print(f"[LOG] - Запрос прошел успешно!")
            print(f"[LOG] - {response.json()}")
            return response.json()['data'][0]['url']
            break
        except Exception as er:
            print(f"[ERROR] - ({er})")
            error = response.json()["error"]["message"]
            print(f'[ERROR] - text[{error}]')
            if "You exceeded your current quota, please check your plan and billing details." in str(error):
                db.del_key(keys)
            elif "Incorrect API key provided" in str(error):
                db.del_key(keys)
            else:
            	return f"error"
    

async def edit_photo(image: bytes, n: int = 2, size: str = "1024x1024") -> list:
    print(f"[LOG] - Делаю запрос в опенАи edit")
    while True:
        try:
            keys = db.get_key()
            if keys == 'no key':
                return 'no key'
                break
            async with aiohttp.ClientSession() as session:
                res = await session.post(
                    url="https://api.openai.com/v1/images/variations",
                    headers={
                        "Authorization": f"Bearer {keys}"
                    },
                    data={
                        "image": image,
                        "size": size,
                        "n": str(n)
                    }
                )
                return [img['url'] for img in (await res.json())['data']]
        except:
            return 'error'
        

async def gpt(text):
    print(f"[LOG] - Делаю запрос в опенАи gpt")
    while True:
        keys = db.get_key()
        if keys == 'no key':
            return 'no key'
            break
        print(f"[LOG] - Выполняется запрос по ключу {keys}")
        chat_response = await openai_async.chat_complete(
            f"{keys}",
            timeout=130,
            payload={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": f"{text}"}],
                },
            )
        try:
            print(f"[LOG] - Запрос прошел успешно!")
            print(f"[LOG] - {chat_response.json()}")
            result_resp = chat_response.json()["choices"][0]["message"]
            return result_resp['content']
            break
        except Exception as er:
            print(f"[ERROR] - ({er})")
            error = chat_response.json()["error"]["message"]
            print(f'[ERROR] - text[{error}]')
            if "You exceeded your current quota, please check your plan and billing details." in str(error):
                db.del_key(keys)
            elif "Incorrect API key provided" in str(error):
                db.del_key(keys)
            else:
            	return f"Была вызвана ошибка!\n(Эта функция не стабильна, поэтому это норма)"

async def chat_respons(text):
    print(f"[LOG] - Делаю запрос в опенАи")
    while True:
        keys = db.get_key()
        if keys == 'no key':
            return 'no key'
            break
        print(f"[LOG] - Выполняется запрос по ключу {keys}")
        chat_response = await openai_async.complete(
            f"{keys}",
            timeout=130,
            payload={
                "model": "text-davinci-003",
                'max_tokens': 2400,
                "prompt": f"{text}",
                'n': 1,
                "temperature": 0.2,
                },
            )
        try:
            print(f"[LOG] - Запрос прошел успешно!")
            print(f"[LOG] - {chat_response.json()}")
            result_resp = chat_response.json()["choices"][0]["text"].strip()
            return result_resp
            break
        except Exception as er:
            print(f"[ERROR] - ({er})")
            error = chat_response.json()["error"]["message"]
            print(f'[ERROR] - text[{error}]')
            if "You exceeded your current quota, please check your plan and billing details." in str(error):
                db.del_key(keys)
            elif "Incorrect API key provided" in str(error):
                db.del_key(keys)
            else:
            	return f"Была вызвана ошибка: {er}"
        
while True:
    try:
        if __name__ == "__main__":
            executor.start_polling(dp, skip_updates=True)
        break
    except:
        print("Ошика.\nОжидаем перезапуск 20 сек...")
        time.sleep(20)
