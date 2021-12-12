import json, requests
import os

from colorama import init, Style, Fore, Back

url = "https://discord.com/api/v9/users/@me"


def request(token, url, method, json=None):
    headers = {
        "authorization": token
    }

    return requests.request(method, url, headers=headers, json=json)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def load_settings():
    with open("settings.json", encoding="UTF-8") as fp:
        settings = json.load(fp)

    return settings


def save_settings(settings):
    with open("settings.json", "w") as fp:
        json.dump(settings, fp, indent=4)


def logo():
    print(f"""{Fore.BLUE}{Style.BRIGHT}\
  ____    _    ____ ___ 
 |  _ \  / \  |  _ \_ _|
 | | | |/ _ \ | |_) | | 
 | |_| / ___ \|  __/| | 
 |____/_/   \_\_|  |___|{Style.RESET_ALL}
""")


def bprint(text: str, state="debug"):
    if state == "debug" and not load_settings().get("showDebugInfo"):
        return

    state_translator = {
        "debug": f"{Style.BRIGHT}{Fore.CYAN}[DEBUG]{Style.RESET_ALL}",
        "error": f"{Style.BRIGHT}{Fore.LIGHTRED_EX}[ERROR]{Style.RESET_ALL}",
        "info": f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[INFO]{Style.RESET_ALL}",
    }
    print("{state} {msg}".format(
        state=state_translator[state],
        msg=text
    ))
