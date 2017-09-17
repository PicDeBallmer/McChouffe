from telegram.ext import Updater, CommandHandler
import requests
import logging

UNTAPPD_API_URL = 'https://api.untappd.com/v4'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Read keys
key_telegram_file = open('./keys/keytelegram', 'r')
key_telegram = key_telegram_file.read().splitlines()[0]
key_telegram_file.close()

key_untappd_client_id_file = open('./keys/keyuntappdclientid', 'r')
key_untappd_client_id = key_untappd_client_id_file.read().splitlines()[0]
key_untappd_client_id_file.close()

key_untappd_client_secret_file = open('./keys/keyuntappdclientsecret', 'r')
key_untappd_client_secret = key_untappd_client_secret_file.read().splitlines()[0]
key_untappd_client_secret_file.close()

followed_users_file = open('./followedusers', 'r')
followed_users = followed_users_file.read().splitlines()
followed_users_file.close()

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

def check(bot, update):
    chat_id = update.message.chat_id
    return_message = check_followed_users()
    bot.sendMessage(chat_id, text=return_message)

def add_user(bot, update, args):
    chat_id = update.message.chat_id
    words = ' '.join(args)
    add_user_in_file(words)
    bot.sendMessage(chat_id, text=words + " added")

def remove_user(bot, update, args):
    chat_id = update.message.chat_id
    words = ' '.join(args)
    remove_user_in_file(words)
    bot.sendMessage(chat_id, text=words + " removed")

def list_followed_users(bot, update):
    chat_id = update.message.chat_id
    followed_user_list = get_followed_user_list()
    bot.sendMessage(chat_id, text=followed_user_list)
    

# def activity(bot, job):
#     bot.sendMessage(chat_id=chat_id,
#       text=activity_feed_query)
#     job.interval = 60 * 60 * randint(1, 24) + randint(-60*60, 60*60) # environ toutes les douze heures

#def test(message: str) -> str:
#    return "test"

# Functions
#def sample_query(message: str) -> str:
#    url = UNTAPPD_API_URL + 'url'
#    query = {'key': key_untappd,
#             'a': 'a',
#             'b': b}

#    response = requests.post(url, data=query)

#    r = response.json()
#    meta = r.get('meta') or {}
#    if meta.get('code') == 200:
#        print(meta['code'])
#        print(r)

#    else:
#        ret = "Error. (Status code = " + str(meta.get('code', r.status_code)) + ") " + str(meta.get('developer_friendly', meta.get('error_detail', '')))
#    return ret

def add_user_in_file(user_name: str):
    #followed_users_file = open('./followedusers', 'r')
    #followed_users = followed_users_file.read().splitlines()
    #followed_users_file.close()
    followed_users.append(user_name)
    followed_users_file = open('./followedusers', 'w')
    for followed_user in followed_users:
        followed_users_file.write(followed_user + "\n")
    followed_users_file.close()

def remove_user_in_file(user_name: str):
    #followed_users_file = open('./followedusers', 'r')
    #followed_users = followed_users_file.read().splitlines()
    #followed_users_file.close()
    followed_users.remove(user_name)
    followed_users_file = open('./followedusers', 'w')
    for followed_user in followed_users:
        followed_users_file.write(followed_user + "\n")
    followed_users_file.close()

def get_followed_user_list() -> str:
    #followed_users_file = open('./followedusers', 'r')
    #followed_users = followed_users_file.read().splitlines()
    #followed_users_file.close()
    s = "\n".join(followed_users)
    return s

# Get the last
def check_followed_users() -> str:

    # TODO, if there is several threads or process, use a mutex
    min_checkin_id_file = open('./mincheckinid', 'r')
    min_checkin_id = int(min_checkin_id_file.read().splitlines()[0])
    min_checkin_id_file.close()

    max_checkin_id = min_checkin_id

    url = UNTAPPD_API_URL + '/user/checkins/'

    ret = ""

    for followed_user in followed_users:
        query = url 
        query += followed_user 
        query += "?" 
        query += "client_id=" + key_untappd_client_id
        query += "&" 
        query += "client_secret=" + key_untappd_client_secret
        query += "&" 
        query += "min_id=" + str(min_checkin_id)
        query += "&"
        query += "limit=" + str(5)

        #query = {'client_id': key_untappd_client_id,
        #     'client_secret' : key_untappd_client_secret,
        #     'username': message,
        #     'min_id ' :}

        response = requests.get(query)

        r = response.json()
        meta = r.get('meta') or {}
        if meta.get('code') == 200:
            checkins = r['response'].get('items',[])

            if checkins == []:
                checkins = r['response']['checkins'].get('items',[])

            new_min_checkin_id = None
            for checkin in checkins :
                # TODO process the response : https://untappd.com/api/docs#activityfeed
                user = checkin.get('user')
                beer = checkin.get('beer')
                brewery = checkin.get('brewery')
                venue = checkin.get('venue')
                rating = checkin.get('rating_score')
                created_at = checkin.get('created_at')
                checkin_comment = checkin.get('checkin_comment')

                if int(checkin.get('checkin_id')) > max_checkin_id:
                    max_checkin_id = checkin.get('checkin_id')

                ret += user.get("user_name") + " drinks " + beer.get("beer_name") + " at " + created_at +"\n"

                if rating is not None:
                    ret += "\t rating: " + str(rating) + "\n"

    if max_checkin_id is not None: 
        # TODO, if there is several threads or process, use a mutex
        min_checkin_id_file = open('./mincheckinid', 'w')
        min_checkin_id = min_checkin_id_file.write(str(max_checkin_id))
        min_checkin_id_file.close()

    return ret

            # TODO fill ret
        #    ret = "TODO : NO RESPONSE"

        #else:
        #    ret = "Error. (Status code = " + str(meta.get('code', r.status_code)) + ") " + str(meta.get('developer_friendly', meta.get('error_detail', '')))
        #return ret



########################################

updater = Updater(key_telegram)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('check', check))
dispatcher.add_handler(CommandHandler('followedUsers', list_followed_users))
dispatcher.add_handler(CommandHandler('addUser', add_user, pass_args=True))
dispatcher.add_handler(CommandHandler('removeUser', remove_user, pass_args=True))

#jobs = updater.job_queue
#job_mc_chouffe = Job(mc_chouffe, 60 * 60 * 12) # 12 hoursdealy when laucnhed
#jobs.put(job_mc_chouffe)

updater.start_polling()
updater.idle()