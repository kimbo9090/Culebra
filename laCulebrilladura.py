import telebot
from telebot import types
import random
import giphypop
import pprint
from giphypop import translate
import re
import telegram
import pafy


bot= telebot.TeleBot("")
g = giphypop.Giphy("")
pattern = re.compile("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")

#  Método para el comando /help. Muestra lo que el bot puede hacer.
'''
@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Bienvenido "+message.from_user.first_name+". Estoy todavía en mi versión alpha! "
    "No me pidas mucho colega, a continuación tendrás una lista con lo que soy capaz de hacer:\n"
    "\n"
    "- Responderá al mensaje: Me cago en tus muertos\n"
    "- /creador: Recibiras un gif del creador\n"
    "- /adivina: Un juego de adivinanzas.\n"
    "-/gif: Busca un gif en gihpy\n"
    "-/random: Te da un gif aleatorio totalmente gratis.\n")

'''




#  Método para la palabra "Me cago en tus muertos". Devuelve el insulto
@bot.message_handler(func=lambda message: message.text == "me cago en tus muertos" or message.text == "Me cago en tus muertos")
def send_something(message):
    bot.send_message(message.chat.id,"Tu madre en patinete "+message.from_user.first_name.lower())
    print(message.chat.id)
    print(message.chat.id)

# Método para el comando /gif. Manda un gif mio alojado en mi pc.
@bot.message_handler(commands=['creador','Creador'])
def send_gif(message):
    video = open('video.mp4', 'rb')
    bot.send_video(message.chat.id, video)
    print(message.chat.id)
    print(message.text)

# Método muy cutre. Juega a un pequeño juego de adivinanzas
@bot.message_handler(commands=['adivina','Adivina'])
def send_welcome(message):
    msg = bot.reply_to(message,"¿Quieres jugar a un juego? "
    "Estoy pensando en un numero que está entre 0 y 1000. Intenta adivinarlo.")
    bot.register_next_step_handler(msg, process_number_step)

def process_number_step(message):
        number = random.randrange(0,1000)
        print(number)
        chat_id = message.chat.id
        numberHuman = message.text
        print(numberHuman)
        if not numberHuman.isdigit():
            msg = bot.reply_to(message, 'Tienes que introducir un numero')
            bot.register_next_step_handler(message, process_number_step)
            return
        def logica(message):

            try:
                numberHuman = message.text
                numberHuman2=int(numberHuman)
                if numberHuman2<number:
                    print("El usuario eligio un numero mayor")
                    bot.send_message(message.chat.id,"Más alto")
                    bot.register_next_step_handler(message, logica)

                elif numberHuman2>number:
                    print("El usuario eligio un numero menor")
                    bot.send_message(message.chat.id,"Más bajo")
                    bot.register_next_step_handler(message, logica)

                elif numberHuman2==number:
                    print("El usuario gano")
                    bot.send_message(message.chat.id, "Exacto! El número era "+str(number))
            except Exception as e:
                bot.reply_to(message, 'Vaya. Has introducido algo que no era un numero. El juego se acaba :(')
        logica(message)
# Busca un gif en GIPHY dependiendo de lo que el usuario quiera buscar
@bot.message_handler(commands=['gif','Gif'])
def send_gif(message):
    bot.send_message(message.chat.id,"Dime que gif debo buscar")
    bot.register_next_step_handler(message,dame_gif)

def dame_gif(message):
    try:
        busqueda = message.text
        img = translate(busqueda, api_key='')
        bot.send_document(message.chat.id, img.fixed_height.url)
    except Exception as e:
        bot.send_message(message.chat.id, "No se ha encontrado ningún gif")

# Te da un gif aleatorio
@bot.message_handler(commands=['random','Random'])
def send_random_gif(message):
    bot.send_message(message.chat.id,"Aquí tienes un gif aleatorio")
    random=g.screensaver()
    bot.send_document(message.chat.id,random.fixed_height.url)

@bot.message_handler(commands=['youtube','Youtube'])
def send_youtube_validation(message):
    bot.send_message(message.chat.id,"Dame un link de yutuba")
    bot.register_next_step_handler(message,valida_link)


def valida_link(message):
    if pattern.match(message.text):
        bot.send_message(message.chat.id, "Es un link de youtube valido")
        markup = types.ReplyKeyboardMarkup()
        itembtna = types.KeyboardButton('Descripcion')
        itembtnv = types.KeyboardButton('Visitas')
        print(bot.forward_message(message.chat.id,message.chat.id,message.chat.id))

        markup.row(itembtna, itembtnv)
        bot.send_message(message.chat.id, "Elige una opcion:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Pero que haces pedazo de toto")


# Cualquier otro mensaje será llevado aquí
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Opción no comprendida. Usa /help o /start para ver los comandos disponibles")
bot.polling()
