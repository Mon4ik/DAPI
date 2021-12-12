import argparse, json, enquiries, os
import threading
import time
from random import choice

from pypresence import Presence

from extra import utils
from colorama import Fore, Style

if not os.path.isdir("results"):
    os.mkdir("results")

utils.clear()
utils.logo()

settings: dict = utils.load_settings()


def token_req(func):
    def wrapper(*args, **kwargs):
        login_vs = [
            "Via export",
            "Via config file",
            "How to get token?"
        ]
        login_v = enquiries.choose("Choose login variant:", login_vs)

        if login_v == login_vs[0]:
            token = os.environ.get('DAPI_TOKEN')
            if token is None:
                utils.bprint(
                    "No token in env. Add to env(Linux, MacOS): export DAPI_TOKEN=mfa.le19...",
                    "error"
                )
                exit(1)
        elif login_v == login_vs[1]:
            if settings.get('token') is None:
                utils.bprint(
                    "Invalid Discord authorization token!",
                    "error"
                )
                exit(1)
            else:
                token = settings['token']
        else:
            print("""\
How to login
 1. Get your discord token (search f.e on google)
    P.s It can be discord bot's token.
        Example of command: export DAPI_TOKEN=Bot ODI3NTE...
                                                     ^
                                                     |
                                                Bot's token
 2. Paste""")
            return
        return func(token, *args, **kwargs)

    return wrapper


@token_req
def dm(token, args: argparse.Namespace):
    vicid = args.id
    threads_count = args.threads

    utils.bprint(
        "Starting load emojis...",
        "debug"
    )
    with open("extra/emojis.txt") as fp:
        emojis = fp.readline()

    utils.bprint(
        "Emojis are loaded!",
        "debug"
    )

    if len(vicid) < 2:
        utils.bprint(
            "Count of victims are below 2",
            "error"
        )
        exit(1)
    j = 0

    def gen_group(thread_id):
        i = 0
        while True:
            i += 1

            dm_group = utils.request(token, "https://discord.com/api/v9/users/@me/channels", "POST", {
                "recipients": vicid
            }).json()
            utils.bprint(
                f"Thread #{thread_id} | DM #{i + 1} > Created",
                "info"
            )

            utils.request(token, f"https://discord.com/api/v9/channels/{dm_group['id']}", "PATCH", {
                "name": "".join([choice(emojis) for i in range(16)])
            })
            utils.bprint(
                f"Thread #{thread_id} | DM #{i + 1} > Renamed",
                "info"
            )
            utils.bprint(
                f"Thread #{thread_id} | DM #{i + 1} > Finish",
                "info"
            )

    threads = []
    for i in range(threads_count):
        threads.append(threading.Thread(target=gen_group, args=[i+1]))

    for thread in threads:
        thread.start()


@token_req
def status_anim(token, args: argparse.Namespace):
    profile_name = args.profile
    profile = settings['statusAnimProfiles'].get(profile_name)

    if profile is None:
        utils.bprint(
            f"Invalid profile",
            "error"
        )
        return

    utils.bprint(
        f"Animation is starting...",
        "info"
    )

    frame = 0
    while True:
        if frame == len(profile['texts']):
            frame = 0
        response = utils.request(token, f"https://discord.com/api/v9/users/@me/settings", "PATCH", {
            "custom_status": {
                "text": profile['texts'][frame],
                "emoji_name": profile['emoji']
            }
        })

        time.sleep(0.2)
        frame += 1


def rpc(args: argparse.Namespace):
    profile_name = args.profile
    profile = settings['richPresenceProfiles'][profile_name]

    if profile['startTimestamp'] == "$now":
        start_time = time.time()
    elif profile['startTimestamp'] is None:
        start_time = None
    else:
        start_time = float(profile['startTimestamp'])

    end_time = profile['endTimestamp']

    lg_img = profile['largeImage']
    sm_img = profile['smallImage']

    buttons = profile['buttons'][:2] or []

    RPC = Presence(profile['clientID'])  # Initialize the client class
    RPC.connect()

    animation_frame = 0

    if type(profile['details']) == list and type(profile['state']) == list:
        if len(profile['details']) != len(profile['state']):
            utils.bprint(
                f"Details and state has different count of frames",
                "error"
            )

    utils.bprint(
        "RPC is starting...",
        "info"
    )

    while True:
        if profile['animation']:
            wait = profile['animation']['intervalSec']
            pick = profile['animation']['pick']

            if pick == "next":
                if animation_frame == len(profile['details']):
                    if profile['animation']['looped']:
                        animation_frame = 0

                if type(profile['details']) == list:
                    details = profile['details'][animation_frame]
                else:
                    details = profile['details']

                if type(profile['state']) == list:
                    state = profile['state'][animation_frame]
                else:
                    state = profile['state']

                animation_frame += 1
        else:
            wait = 3
            details = profile['details']
            state = profile['state']

        RPC.update(
            pid=os.getpid(),

            details=details,
            state=state,

            large_image=lg_img['imgName'],
            large_text=lg_img['text'],
            small_image=sm_img['imgName'],
            small_text=sm_img['text'],

            buttons=buttons,
        )
        time.sleep(wait)


@token_req
def customreq(token, args: argparse.Namespace):
    path = f"/{args.path}" if not args.path.startswith("/") else args.path
    method = args.method

    js = None if args.json == "{}" else json.loads(args.json)
    version = args.version

    response = utils.request(token, f"https://discord.com/api/v{version}{path}", method, js)

    try:
        response.json()
        is_json = True

    except:
        is_json = False

    if is_json:
        resp_ = json.dumps(response.json(), indent=2, ensure_ascii=False)
        resp = ""
        for line in resp_.split("\n"):
            resp += f"         {line}\n"
    else:
        resp = f"         {response.text}"

    times = time.strftime("%d.%m.%y-%H:%M:%S")
    with open(f"results/fetching_{times}.json", "x") as fp:
        json.dump({
            "request": {
                "api_version": f"v{version}",
                "path": path,
                "method": method,
                "json_payload": js,
                "full_url": f"https://discord.com/api/v{version}{path}"
            },
            "response": {
                "status_code": response.status_code,
                "data": response.json() if is_json else response.text
            }
        }, fp, indent=2, ensure_ascii=False)

    utils.bprint(f"""Fetched data:
       Status code: {Style.BRIGHT}{Fore.GREEN + str(response.status_code) if str(response.status_code).startswith("2") else Fore.RED + str(response.status_code)} {Style.RESET_ALL}
       Data <{"JSON" if is_json else "NOT JSON"}>: 
{resp}
""",
                 "info")


parser = argparse.ArgumentParser(description='DiscordAPI client')
options = parser.add_subparsers(title='Functions',
                                description=f'{Fore.LIGHTYELLOW_EX}Functions with API{Style.RESET_ALL}')

dm_parser = options.add_parser('dm_nuke', help='Nuke DB (Give more than 1 id) (Please, use it ONLY on your accounts)')
dm_parser.add_argument("-id", "--userid", dest="id",
                       help="Victim(s) ID",
                       action='append', required=True)
dm_parser.add_argument("-c", "--threads_count", dest="count",
                       help="Threads count",
                       default=1, type=int,
                       required=True)
dm_parser.set_defaults(func=dm)

rpc_parser = options.add_parser('rpc', help='Creates rich presence')
rpc_parser.add_argument("profile",
                        help="RichPresence profile")
rpc_parser.set_defaults(func=rpc)

sanim_parser = options.add_parser('status_animation', help='Creates status animation')
sanim_parser.add_argument("profile",
                          help="StatusAnimation profile")
sanim_parser.set_defaults(func=status_anim)

customreq_parser = options.add_parser('request', help='Make your custom request to Discord API')
customreq_parser.add_argument("path",
                              help="Path to API method",
                              type=str)
customreq_parser.add_argument("-m", "--method", dest="method",
                              help="JSON payload",
                              default="GET")
customreq_parser.add_argument("-j", "--json", dest="json",
                              help="JSON payload",
                              type=str, default="{}")
customreq_parser.add_argument("-v", "--version", dest="version",
                              help="API version",
                              default=9, type=int)
customreq_parser.set_defaults(func=customreq)

if __name__ == '__main__':
    if not settings['_disclaimerShowed']:
        print("""
    Disclaimer:
        This project is for educational and research purposes only.
        Данный проект был создан только в целях обучения.
    """)
        if not enquiries.confirm("Accept?"):
            utils.clear()
            print("why 😐 u r need this")
            exit(1)

        settings['_disclaimerShowed'] = True
        utils.save_settings(settings)

    utils.bprint(
        "Parsing args...",
        "debug"
    )
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        utils.bprint(
            "Starting function!",
            "debug"
        )
        args.func(args)
else:
    utils.bprint(
        "No import! Use: \"python3 main.py -h\" for help",
        "error"
    )
