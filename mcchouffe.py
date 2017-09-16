from telegram.ext import Updater, CommandHandler
import requests
import logging

UNTAPPD_API_URL = 'https://api.untappd.com/v4/'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Read keys
key_telegram_file = open('./keys/keytelegram', 'r')
key_telegram = key_telegram_file.read().splitlines()[0]
key_telegram_file.close()

key_untappd_file = open('./keys/keytelegram', 'r')
key_untappd = key_untappd_file.read().splitlines()[0]
key_untappd_file.close()

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

def check(bot, update, args):
    chat_id = update.message.chat_id
    words = ' '.join(args)
    message = words
    # TODO change cehck to activity_feed_query
    bot.sendMessage(chat_id, text=test)

# def activity(bot, job):
#     bot.sendMessage(chat_id=chat_id,
#       text=activity_feed_query)
#     job.interval = 60 * 60 * randint(1, 24) + randint(-60*60, 60*60) # environ toutes les douze heures

def test(message: str) -> str:
    return "test"

# Functions
def sample_query(message: str) -> str:
    url = UNTAPPD_API_URL + 'url'
    query = {'key': key_untappd,
             'a': 'a',
             'b': b}

    response = requests.post(url, data=query)

    r = response.json()
    meta = r.get('meta') or {}
    if meta.get('code') == 200:
        print(meta['code'])
        print(r)

    else:
        ret = "Error. (Status code = " + str(meta.get('code', r.status_code)) + ") " + str(meta.get('developer_friendly', meta.get('error_detail', '')))
    return ret

# Get the last
def activity_feed_query(message: str) -> str:

    # TODO, if there is several threads or process, use a mutex
    min_checkin_id_file = open('./kmincheckinid', 'r')
    min_checkin_id = min_checkin_id_file.read().splitlines()[0]
    min_checkin_id_file.close()


    url = UNTAPPD_API_URL + '/checkin/recent'
    query = {'access_token': key_untappd,
             'min_id': min_checkin_id}

    response = requests.post(url, data=query)

    r = response.json()
    meta = r.get('meta') or {}
    if meta.get('code') == 200:
        checkins = r['checkins'].get('items',[])

        new_min_checkin_id = None
        for checkin in checkins :
            # TODO process the response : https://untappd.com/api/docs#activityfeed
            user = checkin.get('user')
            beer = checkin.get('beer')
            rating = checkin.get('rating')
            created_at = checkin.get('created_at')
            checkin_comment = checkin.get('checkin_comment')
            new_min_checkin_id = checkin.get('checkin_id')

        if new_min_checkin_id is not None: 
            # TODO, if there is several threads or process, use a mutex
            min_checkin_id_file = open('./mincheckinid', 'w')
            min_checkin_id = min_checkin_id_file.write(str(new_min_checkin_id))
            min_checkin_id_file.close()

        # TODO fill ret
        ret = "TODO : NO RESPONSE"

    else:
        ret = "Error. (Status code = " + str(meta.get('code', r.status_code)) + ") " + str(meta.get('developer_friendly', meta.get('error_detail', '')))
    return ret



########################################

updater = Updater(key_telegram)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('check', check, pass_args=True))

#jobs = updater.job_queue
#job_mc_chouffe = Job(mc_chouffe, 60 * 60 * 12) # 12 hoursdealy when laucnhed
#jobs.put(job_mc_chouffe)

updater.start_polling()
updater.idle()