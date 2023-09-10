import discord
from discord.ext import commands
import json
import os
from flask import Flask
from flask import render_template
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
description = '''Bot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

with open('setting.json', 'r', encoding='UTF-8') as setting:
    settings = json.load(setting)

add_channel_id = settings["add_channel_id"]
author_id = settings["author_id"]
token = settings["token"]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

def save_to_json(messages):
    with open('news.json', 'w') as json_file:
        json.dump(messages, json_file, indent=4)
        print("Successfully!")

@bot.event
async def on_message(message):
    if message.channel.id == add_channel_id and message.author.id == author_id:
        response = "Successfully Received:"
        await message.channel.send(response + ' ' + '```' + message.content + '```')

        message_data = {
            'announce_by': message.author.name,
            'content': message.content,
            'created_at': str(message.created_at)
        }

        if os.path.exists('news.json') and os.path.getsize('news.json') > 0:
            with open('news.json', 'r') as json_file:
                messages = json.load(json_file)
        else:
            messages = []

        messages.append(message_data)
        save_to_json(messages)

@app.route('/news.html')
def news():
    
    def read_all_news_from_json():
        with open('news.json', 'r', encoding='UTF-8') as news_data:
            data = json.load(news_data)
        return data

    all_news = read_all_news_from_json()

    return render_template("news.html", all_news = all_news)

@app.route('/details.html')
def details():
    
    def read_all_news_from_json():
        with open('news.json', 'r', encoding='UTF-8') as news_data:
            data = json.load(news_data)
        return data

    all_news = read_all_news_from_json()

    return render_template("details.html", all_news = all_news)

def run_flask():
    app.run(host="127.0.0.1", port=5500, debug=False)

def run_discord_bot(token):
    bot.run(token)

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_flask)
        executor.submit(run_discord_bot, token)