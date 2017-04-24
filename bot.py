import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from bs4 import BeautifulSoup
import requests

update_id = None
url = 'https://postmates.com/new-york-city'

def main():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('#your API token')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            FoodFinder(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

def FoodFinder(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            webpage = requests.get(url)
            soup = BeautifulSoup(webpage.text, 'html.parser')
            free_food = [s for s in soup.body.stripped_strings if 'free' in s.lower()]
            if free_food:
                body = 'Free Postmates!\n\n' + '\n'.join(free_food)
                #print body #testing
                #replies
                update.message.reply_text(body)
            else:
                update.message.reply_text('Unfortunately there is no free food at the moment on PostMates.\nSorry, bro...')




if __name__ == '__main__':
    main()
