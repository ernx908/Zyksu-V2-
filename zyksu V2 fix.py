import requests
from datetime import datetime
import time
import sys
import os
import random
import secrets
import uuid
import json
import base64
import re
import webbrowser
from threading import Thread, Lock
from cfonts import render
from colorama import Fore, init

init(autoreset=True)

EXPIRY_FILE = ".expiry_start"
VALID_HOURS = 2400
PASSWORD = "ZYKSUGOD"

LAVENDER = "\033[38;5;183m"
RESET = "\033[0m"

red     = "\033[1m\033[31m"
green   = "\033[1m\033[32m"
yellow  = "\033[1m\033[33m"
blue    = "\033[1m\033[34m"
magenta = "\033[1m\033[35m"
cyan    = "\033[1m\033[36m"
white   = "\033[1m\033[37m"
reset   = "\033[0m"

hit = 0
zyksu_bad = 0
empire_checked = 0
token = ""
chat_id = ""
current_email = ""
selected_domains_list = ["@hi2.in"]
print_lock = Lock()
script_running = True
recent_logs = []

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typing(text, delay=0.02, color=green):
    for ch in text:
        sys.stdout.write(color + ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def spinner(text, duration=1.0, color=green):
    frames = ['|', '/', '-', '\\']
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(f"\r{color}▸ {text} {frames[i % len(frames)]}{reset}   ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{color}▸ {text} ✓{reset}   \n")
    sys.stdout.flush()

def hline(color=yellow, width=60):
    print(f"{color}{'─' * width}{reset}")
    
def header():
    clear()
    logo = render(' ZYKSU', font='block', colors=['cyan', 'magenta'], align='left', space=True)
    print(logo)
    hline(yellow)
    left  = f"{yellow}{reset} {yellow}𝐓𝐆 - 𝐙𝐘𝐊𝐒𝐔 𝐄𝐌𝐏𝐈𝐑𝐄{reset}"
    mid   = f"{cyan}𝐇𝐈𝟐 & 𝐓𝐄𝐋𝐄𝐆𝐌𝐀𝐈𝐋{reset}"
    right = f"{magenta}𝐃𝐄𝐕 𝐙𝐘𝐊𝐒𝐔{reset}"
    print(f" {left}  {white}|{reset}  {mid}  {white}|{reset}  {right}")
    hline(yellow)
    print()

# FILE ACTIVE CHECK
def file_active_check():
    spinner("𝐂𝐇𝐄𝐂𝐊𝐈𝐍𝐆 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄 𝐒𝐓𝐀𝐓𝐔𝐒", duration=3.0, color=green)

    if not os.path.exists(EXPIRY_FILE):
        with open(EXPIRY_FILE, "w") as f:
            f.write(str(time.time()))
        print(f"  {green}✓ 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄.....{reset}\n")
        return True

    try:
        with open(EXPIRY_FILE, "r") as f:
            started = float(f.read().strip())
    except (ValueError, OSError):
        with open(EXPIRY_FILE, "w") as f:
            f.write(str(time.time()))
        print(f"  {green}✓ 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄.....{reset}\n")
        return True

    if time.time() - started >= VALID_HOURS * 3600:
        print(f"  {red}✗ 𝐅𝐈𝐋𝐄 𝐄𝐗𝐏𝐈𝐑𝐄𝐃.....{reset}\n")
        return False

    print(f"  {green}✓ 𝐅𝐈𝐋𝐄 𝐀𝐂𝐓𝐈𝐕𝐄.....{reset}\n")
    return True

def check_instagram_email(email):
    url = "https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/"
    
    device = str(uuid.uuid4())
    family = str(uuid.uuid4())
    android = "android-" + secrets.token_hex(8)
    
    brands = ["samsung", "Google", "Xiaomi", "OnePlus", "Nothing", "Realme", "Redmi"]
    models = ["SM-G973F", "Pixel 7", "M2102J20SG", "ONEPLUS A6003", "A063"]
    dpi_values = ["420", "450", "440"]
    res_values = ["1080x2280", "1080x2400", "1440x3088"]
    android_versions = ["11", "12", "13", "14"]
    instagram_versions = [280, 290, 300, 310, 320, 330, 340]
    
    brand = random.choice(brands)
    model = random.choice(models)
    dpi_val = random.choice(dpi_values)
    res_val = random.choice(res_values)
    android_ver = random.choice(android_versions)
    insta_ver = random.choice(instagram_versions)
    
    ua = f"Instagram {insta_ver}.0.0.{random.randint(10,99)} Android ({android_ver}; {dpi_val}dpi; {res_val}; {brand}; {model}; en_US)"
    tz_offset = str(random.choice([60, 330, 480, 570]))
    
    payload = {
        'params': json.dumps({
            "client_input_params": {
                "aac": json.dumps({
                    "aac_init_timestamp": int(time.time()),
                    "aacjid": str(uuid.uuid4()),
                    "aaccs": secrets.token_urlsafe(32)
                }),
                "flash_call_permissions_status": {
                    "READ_PHONE_STATE": "PERMANENTLY_DENIED",
                    "READ_CALL_LOG": "DENIED",
                    "ANSWER_PHONE_CALLS": "DENIED"
                },
                "was_headers_prefill_available": 0,
                "network_bssid": None,
                "sfdid": "",
                "fetched_email_token_list": {},
                "search_query": email,
                "auth_secure_device_id": "",
                "ig_oauth_token": [],
                "cloud_trust_token": None,
                "was_headers_prefill_used": 0,
                "sso_accounts_auth_data": [],
                "encrypted_msisdn": "",
                "device_network_info": None,
                "text_input_id": f"akyuf0:{random.randint(50, 70)}",
                "zero_balance_state": None,
                "android_build_type": "release",
                "accounts_list": [],
                "is_oauth_without_permission": 0,
                "ig_android_qe_device_id": device,
                "gms_incoming_call_retriever_eligibility": "client_not_supported",
                "search_screen_type": "email_or_username",
                "is_whatsapp_installed": 1,
                "lois_settings": {"lois_token": ""},
                "ig_vetted_device_nonce": None,
                "headers_infra_flow_id": "",
                "fetched_email_list": []
            },
            "server_params": {
                "event_request_id": str(uuid.uuid4()),
                "is_from_logged_out": 0,
                "layered_homepage_experiment_group": None,
                "device_id": android,
                "login_surface": "login_home",
                "waterfall_id": str(uuid.uuid4()),
                "INTERNAL__latency_qpl_instance_id": random.uniform(6.3e13, 6.5e13),
                "is_platform_login": 0,
                "context_data": "",
                "login_entry_point": "logged_out",
                "INTERNAL__latency_qpl_marker_id": 36707139,
                "family_device_id": family,
                "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
                "access_flow_version": "pre_mt_behavior",
                "is_from_logged_in_switcher": 0,
                "qe_device_id": device
            }
        }),
        'bk_client_context': json.dumps({
            "bloks_version": "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
            "styles_id": "instagram"
        }),
        'bloks_versioning_id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b"
    }
    
    headers = {
        'User-Agent': ua,
        'accept-language': 'en-IN, en-US',
        'x-bloks-version-id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
        'x-fb-friendly-name': 'IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/',
        'x-ig-android-id': android,
        'x-ig-app-id': '567067343352427',
        'x-ig-app-locale': 'en_IN',
        'x-ig-device-id': device,
        'x-ig-family-device-id': family,
        'x-ig-timezone-offset': tz_offset,
        'x-mid': base64.urlsafe_b64encode(secrets.token_bytes(18)).decode().rstrip('='),
        'x-pigeon-rawclienttime': str(time.time()),
        'x-pigeon-session-id': f'UFS-{uuid.uuid4()}-0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if email.lower() in response.text.lower():
            return True
        return False
    except Exception:
        return False
      
def get_ig_user_info(username):
    try:
        url = "https://i.instagram.com/api/v1/users/web_profile_info/"
        headers = {
            'User-Agent': "Instagram 320.0.0.34.109 Android (33/13; 420dpi; 1080x2340; samsung; SM-A546B; a54x; exynos1380; en_US; 465123678)",
            'x-ig-app-id': '936619743392459',
            'Accept': '*/*',
        }
        r = requests.get(f"{url}?username={username}", headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            user = data.get("data", {}).get("user")
            if user:
                return {
                    "username": user.get("username", username),
                    "full_name": user.get("full_name", "N/A"),
                    "bio": user.get("biography", "No bio").replace("\n", " ")[:60],
                    "followers": user.get("edge_followed_by", {}).get("count", 0),
                    "following": user.get("edge_follow", {}).get("count", 0),
                    "monetization": "Yes" if (user.get("is_business_account") or user.get("is_professional_account") or user.get("is_verified")) else "No"
                }
        return None
    except:
        return None

def icdcm(mail, user_info=None):
    global hit
    uname = user_info['username'] if user_info else mail.split('@')[0]
    
    msg = f"""
╭━━━𝐙𝐘𝐊𝐒𝐔 𝐈𝐍𝐒𝐓𝐀 𝐇𝐈𝐓𝐒━━━╮

   𝗛𝗜𝗧𝗦     ➜  {hit}
   𝗘𝗠𝗔𝗜𝗟 ➜ {mail}
"""
    if user_info:
        msg += f"""   𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘 ➜ @{uname}
   𝗙𝗢𝗟𝗟𝗢𝗪𝗘𝗥𝗦 ➜ {user_info['followers']}
   𝗙𝗢𝗟𝗟𝗢𝗪𝗜𝗡𝗚 ➜ {user_info['following']}
   𝗠𝗢𝗡𝗘𝗧𝗜𝗭𝗔𝗧𝗜𝗢𝗡 ➜ {user_info['monetization']}
   𝗕𝗜𝗢 ➜ {user_info['bio']}
"""
    msg += f"""
━━━━━━━━━━━━━━━━━━━━━━

   𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥  ➜  @zyksu
   𝗖𝗛𝗔𝗡𝗡𝗘𝗟       ➜ @zyksufirst
╰━━━━━━━━━━━━━━━━━━━━╯
"""
    
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "📢 CHANNEL", "url": "https://t.me/zyksufirst"},
                {"text": "👤 DEV", "url": "https://t.me/zyksu"}
            ]
        ]
    }

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id, 
        'text': msg, 
        'parse_mode': 'Markdown',
        'reply_markup': json.dumps(reply_markup)
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except:
        pass

def status():
    global hit, zyksu_bad, empire_checked, recent_logs
    if not script_running: return
    
    pyanuj = f"""
{yellow}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮

   {blue}𝗧𝗚 - 𝗭𝗬𝗞𝗦𝗨 𝗘𝗠𝗣𝗜𝗥𝗘{reset} {white}|{reset} {cyan} 𝗜𝗚 - 𝗛𝗨𝗡𝗧𝗘𝗥{reset} {white}|{reset} {magenta} 𝗗𝗘𝗩 - 𝗭𝗬𝗞𝗦𝗨{reset}
{yellow}
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

{yellow}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮

     {green}𝗛𝗜𝗧𝗦 {green}➜{green}{hit}{reset}      {red}𝗕𝗔𝗗 𝗜𝗚{red}➜{red}{zyksu_bad}{reset}      {yellow}𝗖𝗛𝗘𝗖𝗞𝗘𝗗 {yellow}➜{yellow}{empire_checked} {reset}      
        
{yellow}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""
    for log in recent_logs[-2:]:
        pyanuj += log + "\n"

    with print_lock:
        sys.stdout.write("\033[H\033[J") 
        print(pyanuj)
        sys.stdout.flush()

def genprefix():
    char = 'abcdefghijklmnopqrstuvwxyz'
    lent = random.randint(6, 7)
    return ''.join(random.choices(char, k=lent))
   
def process_hit_bg(email, prefix):
    try:
        user_info = get_ig_user_info(prefix)
        icdcm(email, user_info)
        if user_info:
            with print_lock:
                print(f'{cyan}  ↳ @{prefix} | Followers: {user_info["followers"]} | Mon: {user_info["monetization"]}{reset}')
    except Exception:
        pass

def adh():
    global hit, zyksu_bad, empire_checked, current_email, recent_logs
    
    while True:
        if not script_running: break
        prefix = genprefix()
        domain = random.choice(selected_domains_list)
        email = f'{prefix}{domain}'
        empire_checked += 1
        current_email = email

        if check_instagram_email(email):
            hit += 1
            recent_logs.append(f"{green}✓ Hit found: {email}{reset}")
            if len(recent_logs) > 2: recent_logs.pop(0)
            
            status()
            with open('Tempmail.txt', 'a') as f:
                f.write(email + '\n')
            
            Thread(target=process_hit_bg, args=(email, prefix), daemon=True).start()
            
        else:
            zyksu_bad += 1
            recent_logs.append(f"{red}BAD MAIL: {email}{reset}")
            if len(recent_logs) > 2: recent_logs.pop(0)
            
            if empire_checked % 2 == 0:
                status()
               
def page_one():
    global script_running
    header()

    typing("  >>> 𝗦𝗧𝗔𝗥𝗧𝗜𝗡𝗚 𝗝𝗔𝗖𝗞𝗜𝗡𝗚 𝗙𝗜𝗟𝗘...", 0.02, green)
    typing("  >>> 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗡𝗚 𝗦𝗘𝗥𝗩𝗘𝗥...", 0.02, green)
    typing("  >>> 𝗥𝗨𝗡𝗡𝗜𝗡𝗚 𝗦𝗘𝗥𝗩𝗘𝗥...   ", 0.02, green)
    typing("  >>> 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗡𝗚 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗕𝗢𝗧... ", 0.02, green)
    typing("  >>> 𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗡𝗚 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗜𝗗", 0.02, green)
    typing("  >>> 𝗔𝗖𝗖𝗘𝗦𝗦 𝗚𝗥𝗔𝗡𝗧𝗘𝗗 ", 0.02, green)

    if not file_active_check():
        script_running = False
        raise SystemExit

    print("✅ 𝗦𝗖𝗥𝗜𝗣𝗧 𝗜𝗦 𝗔𝗖𝗧𝗜𝗩𝗘 ")
    print()

    entered = input(f"{LAVENDER}𝐄𝐍𝐓𝐄𝐑 𝐏𝐀𝐒𝐒𝐖𝐎𝐑𝐃: {RESET}")
    if entered != PASSWORD:
        print("❌ 𝗪𝗥𝗢𝗡𝗚 𝗣𝗔𝗦𝗦𝗪𝗢𝗥𝗗")
        script_running = False
        sys.exit()

    print("✅ 𝗟𝗢𝗚𝗜𝗡 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 ")
    try:
        webbrowser.open("https://t.me/zyksufirst")
    except:
        pass
        
    time.sleep(1)

def page_two():
    global token, chat_id
    header()
    print(f"  {cyan}▸{reset} {blue}𝐓𝐆 𝐁𝐎𝐓 𝐓𝐎𝐊𝐄𝐍{reset}")
    token = input(f"  {cyan}➜ {reset}").strip()
    print()
    print(f"  {cyan}▸{reset} {blue}𝐓𝐆 𝐂𝐇𝐀𝐓 𝐈𝐃{reset}")
    chat_id = input(f"  {cyan}➜ {reset}").strip()
    time.sleep(0.8)

# ==============================
# PAGE 3 — DOMAIN SELECT
# ==============================
def page_domain():
    global selected_domains_list
    header()

    print(f"  {yellow}SELECT DOMAIN ( 3 option best){reset}")
    hline(yellow)
    print()
    print(f"  {green}[1]{reset} {white}HI2          {cyan}@hi2.in{reset}")
    print(f"  {green}[2]{reset} {white}TELEGMAIL    {cyan}@telegmail.com{reset}")
    print(f"  {green}[3]{reset} {white}BOTH         {cyan}@hi2.in + @telegmail.com{reset}")
    hline(yellow)
    print()

    choice = input(f"  {cyan}➤ CHOOSE (1/2/3) : {reset}").strip()

    if choice == '2':
        selected_domains_list = ["@telegmail.com"]
        print(f"\n  {green}→ telegmail domain running...{reset}")
    elif choice == '3':
        selected_domains_list = ["@hi2.in", "@telegmail.com"]
        print(f"\n  {green}→ both domain running...{reset}")
    else:
        selected_domains_list = ["@hi2.in"]
        print(f"\n  {green}→ 𝐅𝐈𝐋𝐄 𝐈𝐒 𝐑𝐔𝐍𝐍𝐈𝐍𝐆.....{reset}")

    time.sleep(1.5)

def page_three():
    clear()
    
    for _ in range(50):
        Thread(target=adh, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        global script_running
        script_running = False
        print("\nStopped.")

if __name__ == '__main__':
    page_one()
    page_two()
    page_domain()
    page_three()