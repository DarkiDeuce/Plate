import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("")

def link():
    link_plate = []
    url = 'https://collectomania.ru/collection/7-vinyl-single'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    card = soup.find('div', class_='catalog').find_all(action='/cart_items')

    for i in card:
        link_plate.append('https://collectomania.ru'+i.find('a').get('href'))

    return link_plate

def record_information(message, list_link):
    title = []
    value = []
    new = '        New -\xa0Новая запечатанная пластинка.Still Sealed -\xa0Винтажная фабрично запечатанная пластинка.M (Mint) -\xa0Пластинку не проигрывали или проигрывали не более 3 раз. Пластинка не имеет видимых дефектов. Конверт не имеет видимых дефектов.NM (Near Mint) -\xa0Пластинку проигрывали более 3 раз. Пластинка может иметь незначительные потертости или царапины от бумажного конверта, не влияющие на качество звука. Конверт может иметь незначительные изломы или дефекты, не портящие его общий вид.EX (Excellent) -\xa0Пластинка проигрывалась часто, но с соблюдением основных правил пользования и хранения. На пластинке допускаются поверхностные царапины и потёртости, не вызывающие слышимых дефектов звучания. Возможен поверхностный шум в паузах. На обложке допускаются потёртости в виде незначительных кругов и небольшие дефекты на углах или изгибах.VG (Very Good) -\xa0Пластинка проигрывалась большое количество раз. На пластинке имеются царапины или потёртости, которые могут быть слышны. Возможен эффект «песка» между дорожек и в тихих местах. Не допускаются любые заедания или пропуски. Конверт может иметь значительные дефекты или небольшие разрывы.    '

    for i in list_link:
        url = i

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        information = soup.find('div', 'product__chars--list')
        availability = soup.find('span', class_='product__availeable__button').text.replace('\n', ' ').strip()

        if availability == 'есть в наличии':
            product_title = information.find_all('span', class_='product__chars--item--title')
            product_value = information.find_all('span', class_='product__chars--item--value')

            for j in product_value:
                value.append(j.text.replace('\n', ' ').replace('               ', '').replace(new, '').strip())

            for j in product_title:
                title.append(j.text.replace('\n', ' ').replace('               ', '').strip())

            photo = soup.find('a', class_='img-ratio img-fit product__photo').get('href')
            name = soup.find('h1', class_='product__title heading').text.replace('\n', ' ').strip()
            cost = soup.find('span', class_='current-price').text.replace('                  ', '').replace('\n', ' ')

            uniq_and_fifa = dict(zip(title, value))

            planned = '\n'.join([i + ': ' +  uniq_and_fifa[i] for i in uniq_and_fifa])
            text = f'Название: {name}]\nСтоимость: {cost}\n{planned}\n'

            bot.send_photo(message.chat.id, photo=photo, caption=text)

        else:
            break

@bot.message_handler(commands=['plate'])
def plate(message):
    record_information(message, link())

bot.polling(none_stop=True)