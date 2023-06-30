import os
from dotenv import load_dotenv
import keyring
import keyboard
import pyautogui
import rpa_pyautogui_methods as rpa_methods
from os.path import exists

load_dotenv()


def start_1C():
    server_ip = os.getenv('SERVER_IP')
    login = os.getenv('LOGIN')
    base = os.getenv('BASE')
    path_1C = os.getenv('PATH_1C')
    pwd = keyring.get_password("system", login)

    cmd = 'echo \"start\" && \"{path_1C}\" ENTERPRISE /S {server_ip} /IBName "{base}" /N "{login}" /P "{pwd}" && exit'
    command = cmd.format(pwd=pwd, login=login, base=base, path_1C=path_1C, server_ip=server_ip)
    os.system(command)


def activate_1C():
    img = 'info.png'
    name_base = 'Управление торговлей'  # В моем случае база называлась Управление торговлей 11.4
    success = False
    for w in pyautogui.getWindowsWithTitle(name_base):
        # w.maximize()
        w.activate()
        if rpa_methods.wait_element(img, 2):
            rpa_methods.hower_click(img)
            success = True
            print('success')
            break

    if not success:
        raise Exception('Ошибка активации окна 1С')


def open_epf(path_epf, img_check=""):
    if not exists(path_epf):
        raise Exception('Файл обработки не существует')
    rpa_methods.press('ctrl+o', interval=1)
    keyboard.write(path_epf)
    rpa_methods.press('enter', interval=1)
    img = "attention.png"
    img_yes = "attention_yes.png"

    if rpa_methods.wait_element(img, timeout=5):
        x, y = rpa_methods.get_center(img)
        region = (x, y, 80, 50)  # область в которой искать (left, top, width, height)
        if not rpa_methods.wait_element(img_yes, timeout=5, region=region):
            raise Exception('Ошибка поиска кнопик Да')
        rpa_methods.hower_click(img_yes, region=region)

    if not img_check == "":
        if not rpa_methods.wait_element(img_check, timeout=5):
            raise Exception('Ошибка открытия обработки')


if __name__ == '__main__':
    start_1C()
    activate_1C()
    open_epf("D:\\1C\\КонсольЗапросовУФ.epf", "console.png")
