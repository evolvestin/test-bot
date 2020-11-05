import re
import os
from time import sleep
import _thread
from selenium import webdriver
from bs4 import BeautifulSoup
import pickle
from telegraph import upload
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from collections import defaultdict

username = 'hervogv@gmail.com'
password = 'Slava2629'
language_dict = defaultdict(dict)
os.environ['DISPLAY'] = 1
language_dict['en'] = {
    'login': 'log in',
    'save_info': 'not now',  # 'save info',
    'cancel': 'cancel'
}
language_dict['ru'] = {
    'login': 'войти',
    'save_info': 'не сейчас',  # 'сохранить данные',
    'cancel': 'отмена'
}

def image():
    uploaded = upload.upload_file(open('screen.png', 'rb'))
    return '<a href="https://telegra.ph' + uploaded[0] + '">​​</a>️'


userProfile = r"C:\Users\ASUS\AppData\Local\Google\Chrome\User Data\Default"
options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# options.add_argument("user-data-dir={}".format(userProfile))
options.add_argument('--disable-logging')
# options.add_argument('--log-level=3')
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
options.add_experimental_option('mobileEmulation', {"deviceName": "Pixel 2"})
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

print('Успешно запущен браузер')

driver.get('https://instagram.com/')

driver.delete_all_cookies()
driver.refresh()
sleep(3)
driver.save_screenshot('screen.png')
print('Загрузили главную страницу ' + image())
sleep(10)


def lang(text):
    language = driver.find_element_by_tag_name('html').get_attribute('lang')
    if language == 'en':
        lang_text = language_dict['en'][text]
    else:
        lang_text = language_dict['ru'][text]
    return lang_text


def guaranteed(search_tag):
    global driver
    func_of_search = driver.find_elements_by_tag_name(search_tag)
    func = func_of_search
    while len(func) == 0:
        print('Кнопок нет никаких, обновляю страницу')
        driver.refresh()
        sleep(6)
        func = func_of_search
    return func


def click_on_button(raw_focus_text):
    global driver
    focus_text = lang(raw_focus_text)
    buttons = guaranteed('button')
    for i in buttons:
        button_text = re.sub('\s+', ' ', i.text.lower().strip())
        if button_text == focus_text and (i.get_attribute('type') == 'button' or i.get_attribute('tabindex') == '0'):
            i.click()
            print('Кнопку ' + raw_focus_text.capitalize() + ' нашли и нажали')
            break


def click_on_post_button():
    global driver
    divs = guaranteed('div')
    stamp1 = datetime.now().timestamp()
    for i in divs:
        if i.get_attribute('data-testid') == 'new-post-button' and i.get_attribute('role') == 'menuitem':
            print(os.getcwd() + '\logo.jpg')
            cancel()
            sleep(2)
            i.click()
            sleep(3)
            print(os.getcwd() + r'\logo.jpg')
            # i.send_keys(os.getcwd() + r'\logo.jpg')
            #sleep(10)
            #autoit.win_activate("Open")
            #autoit.control_send("Open", "Edit1", os.getcwd() + r'\logo.jpg')
            #autoit.control_send("Open", "Edit1", "{ENTER}")
            pyautogui.write(os.getcwd() + r'\logo.jpg', interval=0.01)
            #sleep(10)
            #autoit.win_activate("Open")
            #autoit.control_send("Open", "Edit1", os.getcwd() + r'\logo.jpg')
            #autoit.control_send("Open", "Edit1", "{ENTER}")
            sleep(2)

            pyautogui.press('return')
            sleep(2)
            cancel()
            print('Кнопку запостить нашли и нажали')
            break
    stamp2 = datetime.now().timestamp()
    print('время отзалупливания = ', str(stamp2 - stamp1))
    print('длина массива = ', len(divs))


def login():
    click_on_button('login')
    sleep(3)
    user = driver.find_element_by_name('username')
    if user:
        user.send_keys(username)
        sleep(2)
        print('Поле логина нашли и отправили в него логин')
        user_pass = driver.find_element_by_name('password')
        if user_pass:
            user_pass.send_keys(password)
            driver.save_screenshot('screen.png')
            print('Поле пароля нашли и отправили в него пароль ' + image())
            sleep(3)
            user_pass.send_keys(Keys.RETURN)
            sleep(6)
            driver.save_screenshot('screen.png')
            print('После ввода логина и пароля нажали на кнопку. Логин успешен ' + image())


def modal_save_info():
    click_on_button('save_info')


def cancel():
    click_on_button('cancel')


def new_post():
    click_on_button('')


login()
modal_save_info()
sleep(6)
cancel()
sleep(6)
click_on_post_button()
driver.save_screenshot('screen.png')
print('Сказоньке конец ' + image())
_thread.exit()


sleep(9)





_thread.exit()
