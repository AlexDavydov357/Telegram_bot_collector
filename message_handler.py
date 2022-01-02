import os
import cv2
import sys
from subprocess import Popen
from aiogram import types
from dispatcher import dp, bot
from bot import BotDB
from io import BytesIO

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

message_path = sys.path[0]
suffix = ['ogg', 'wav', 'jpg', 'png']
voice_message_path = os.path.join(message_path, 'voice_message/')
photo_path = os.path.join(message_path, 'photo_message/')


def check_user_exist(message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)


@dp.message_handler(commands = "start")
async def welcome(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    sti = open('sticker/hi.webp', 'rb')
    await message.bot.send_sticker(message.from_user.id, sti)
    await message.bot.send_message(message.from_user.id, f"Добро пожаловать, {message.from_user.first_name}!\n \
    Я <b>Бот</b>, созданный, чтобы сохранять аудио сообщения и фотографии на которых есть лица.", parse_mode='html')


@dp.message_handler(content_types= 'voice')
async def voice_processing(message: types.Voice):
    check_user_exist(message)
    file_name = f"{message.from_user.id}_{message.message_id}.{suffix[0]}" # {message.date}_
    downloaded_file = await bot.download_file_by_id(message.voice.file_id)
    b = BytesIO()
    b.write(downloaded_file.getvalue())
    with open(voice_message_path + file_name, 'wb') as new_file:
        new_file.write(b.getvalue())
    new_file.close()
    new_file_name = f"{file_name.split('.')[0]}.{suffix[1]}"
    command_line = f"opusdec.exe --rate 16000 {file_name} {new_file_name}"
    process = Popen(command_line, cwd=voice_message_path, shell=True)
    process.communicate()
    os.remove(voice_message_path + file_name)
    BotDB.add_record('audio', message.from_user.id, new_file_name)
    print(f"Аудио сообщение от user {message.from_user.id} успешно конвертировано, и добавлено в БД")


@dp.message_handler(content_types=['photo'])
async def photo_processing(message: types.ChatPhoto):
    check_user_exist(message)
    downloaded_file = await bot.download_file_by_id(message.photo[-1].file_id)
    file_name = f"{message.from_user.id}_{message.message_id}.{suffix[2]}"
    b = BytesIO()
    b.write(downloaded_file.getvalue())
    with open(photo_path + file_name, 'wb') as new_file:
        new_file.write(b.getvalue())
    new_file.close()
    # Загружаем фото
    img = cv2.imread(photo_path + file_name)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=10, minSize=(50, 50))
    if len(faces) == 0:
        print(f"Фото от user {message.chat.id} не содержит лиц и будет удалено")
        os.remove(photo_path + file_name)
    else:
        BotDB.add_record('photo', message.from_user.id, file_name)
        print(f"Фото от user {message.chat.id} содержит лица, успешно сохранено")


# here you can setup your password to stop collecting data
@dp.message_handler(commands= 'bye')
async def stop_command(message: types.Message):
    sti = open('sticker/by.webp', 'rb')
    await message.bot.send_sticker(message.chat.id, sti)
    await message.bot.send_message(message.chat.id, f"Досвидания, {message.from_user.first_name}, хорошо поработали сегодня!")
    bot.stop_polling()
    exit("the bot finished his job")
