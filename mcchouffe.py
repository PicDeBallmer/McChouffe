from telegram.ext import Updater, CommandHandler
import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Read keys
key_telegram = open('./keys/keytelegram').read().splitlines()[0]
key_untappd = open('./keys/keyuntappd').read().splitlines()[0]

chat_id = 0


# Basic commands
def start(bot, update):
    chat_id = update.message.chat_id
    # TODO Init goes here
    message = 'Hey, I am McChouffe!'
    bot.sendMessage(chat_id, text=message)


# def mc_chouffe(bot, update, args):
#     chat_id = update.message.chat_id
#     words = ' '.join(args)
#     messag = words
#     # TODO add logic
#     bot.sendMessage(chat_id, text=message)


def mc_chouffe(bot, job):
    bot.sendMessage(chat_id=chat_id,
                    text='Hey')
    job.interval = 60 * 60 * randint(1, 24) + randint(-60*60, 60*60) # environ toutes les douze heures


# Functions
def sample_query(message: str) -> str:
    url = "url"
    query = {'key': key,
             'a': 'a',
             'b': b}

    r = requests.post(url, data=query)

    if r.status_code == 200:
        print(r.status_code)
        print(r.text)
        print(r.json())

        text = r.json()['text']
        print(text)

    else:
        ret = "Error. (Status code = " + str(r.status_code) + ")"
    return ret





########################################

updater = Updater(key_telegram)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
# dispatcher.add_handler(CommandHandler('mc_chouffe', emo, pass_args=True))

jobs = updater.job_queue
job_ctrlv = Job(ctrlv, 60 * 60 * 12) # douze heures de délai au démarrage pour éviter le pollupostage en cas de redémarrage
jobs.put(job_ctrlv)

updater.start_polling()
updater.idle()