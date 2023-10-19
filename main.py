import telebot
import requests

token = '6411835600:AAELuDRHCjbDU80uk2tboPQUj8ypzSw7Ic4'

bot = telebot.TeleBot(token)

TMDB_API_KEY = '7972cc74b54bc4aa947c3cc5a4434a35'  # Отримайте ключ API на сайті TMDb
TMDB_API_URL = 'https://api.themoviedb.org/3/search/movie'


@bot.message_handler(commands = ['start'])
def send_velcome(message):
    bot.reply_to(message, 'Вітаю! Я бот для пошуку інформації про фільми. Просто введіть назву фільму.')

@bot.message_handler(func=lambda message: True)
def search_movie(message):
    movie_name = message.text
    params = {
        "api_key" : TMDB_API_KEY,
        "query" : movie_name
    }
    try:
        response = requests.get(TMDB_API_URL, params=params)
        data = response.json()
        
        if data['results']:
            movie = data['results'][0]
            watch_link = f'https://www.themoviedb.org/movie/{movie["id"]}/watch?locale=uk-UA'
            title = movie['title']
            overview = movie['overview']
            popularity = movie['popularity']
            vote = movie['vote_average']
            release = movie['release_date']
            poster_path = movie['poster_path'] 
            bot.send_photo(message.chat.id, f'https://image.tmdb.org/t/p/w500{poster_path}', caption=f"""
Назва фільму: {title}

Опис: {overview}

Перегляди: {popularity}

Оцінка: {vote}

Дата виходу фільму: {release}

Посилання: {watch_link}
""")
        else:
            bot.reply_to(message, 'Фільм не знайдено.')
    except Exception as ex:
        bot.reply_to(message, f'Сталася помилка при пошуку фільму {message.text}')
        print(ex)
        
bot.polling()


