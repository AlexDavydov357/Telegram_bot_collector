from subprocess import Popen
import os
import cv2


face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# idrd_bot
def start_bot(bot, message_path):
    suffix = ['ogg', 'wav', 'jpg', 'png']
    voice_message_path = os.path.join(message_path, 'voice_message/')
    photo_path = os.path.join(message_path, 'photo_message/')


    @bot.message_handler(content_types=['voice'])
    def voice_processing(message):
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = f"{message.from_user.id}_{message.date}_{message.message_id}.{suffix[0]}"
        with open(voice_message_path + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        new_file.close()
        command_line = f"opusdec.exe --rate 16000 {file_name} {file_name.split('.')[0]}.{suffix[1]}"
        process = Popen(command_line, cwd=voice_message_path, shell=True)
        process.communicate()
        os.remove(voice_message_path + file_name)
        print(f"Аудио сообщение от user {message.from_user.id} успешно конвертировано")


    @bot.message_handler(content_types=['photo'])
    def photo_processing(message):
        print(message.message_id)
        file_info = bot.get_file(message.photo[2].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = f"{message.from_user.id}_{message.date}_{message.message_id}.{suffix[2]}"
        with open(photo_path + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        new_file.close()
        # Загружаем фото
        img = cv2.imread(photo_path + file_name)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=10, minSize=(50, 50))
        if len(faces) == 0:
            print(f"Фото от user {message.chat.id} не содержит лиц и будет удалено")
            os.remove(photo_path + file_name)
        else:
            print(f"Фото от user {message.chat.id} содержит лица, успешно сохранено")
