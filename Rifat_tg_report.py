import asyncio
import sys
import os
import time
import random
import glob
from telethon import TelegramClient
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.functions.account import ReportPeerRequest

from telethon.tl.types import (
    InputReportReasonSpam,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonChildAbuse,
    InputReportReasonCopyright,
    InputReportReasonGeoIrrelevant,
    InputReportReasonFake,
    InputReportReasonIllegalDrugs,
    InputReportReasonPersonalDetails,
    InputReportReasonOther
)

from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIGURATION ---
API_ID = 37745734          # আপনার API ID
API_HASH = 'a3451a8959597f48f2d56a4caf0861ab'  # আপনার API Hash
# ---------------------

def animate_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner_art = f"""
{Fore.CYAN}{Style.BRIGHT}====================================================
{Fore.RED}{Style.BRIGHT}  ____  _  __       _       _______ _____ 
 {Fore.YELLOW}{Style.BRIGHT}|  _ \\(_)/ _|     | |     |__   __/ ____|
 {Fore.GREEN}{Style.BRIGHT}| |_) |_| |_  __ _| |_       | | | |  __ 
 {Fore.CYAN}{Style.BRIGHT}|  _ <| |  _|/ _` | __|      | | | | |_ |
 {Fore.BLUE}{Style.BRIGHT}| |_) | | | | (_| | |_       | | | |__| |
 {Fore.MAGENTA}{Style.BRIGHT}|____/|_|_|  \\__,_|\\__|      |_|  \\_____|
                                          
         {Fore.MAGENTA}{Style.BRIGHT}R I F A T   T G   R E P O R T
{Fore.CYAN}{Style.BRIGHT}====================================================
"""
    print(banner_art)
    
    loading_text = f"{Fore.GREEN}[*] Initializing Rifat Tg Report Framework..."
    for char in loading_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")

def get_all_sessions():
    """ডিফাইন করা ফোল্ডার থেকে সব .session ফাইল খুঁজে বের করে"""
    files = glob.glob("*.session")
    session_names = [os.path.splitext(f)[0] for f in files]
    return session_names

async def add_tg_account():
    print(f"\n{Fore.CYAN}--- Add Telegram Account ---")
    session_file = input(f"{Fore.YELLOW}একাউন্টের একটি নাম দিন (Session Name) [মেইন মেনুতে ফিরতে '0' বা 'b' চাপুন]: {Fore.WHITE}").strip()
    if session_file in ['0', 'b', 'B']:
        return

    if not session_file:
        session_file = f"session_{int(time.time())}"

    client = TelegramClient(session_file, API_ID, API_HASH)
    try:
        await client.connect()
        
        if not await client.is_user_authorized():
            phone = input(f"{Fore.YELLOW}ফোন নম্বর লিখুন (কান্ট্রি কোড সহ, যেমন +880...): {Fore.WHITE}").strip()
            if phone in ['0', 'b', 'B']:
                return
                
            await client.send_code_request(phone)
            code = input(f"{Fore.YELLOW}টেলিগ্রাম অ্যাপে আসা লগইন কোডটি দিন: {Fore.WHITE}").strip()
            try:
                await client.sign_in(phone, code)
            except Exception:
                password = input(f"{Fore.YELLOW}টু-স্টেপ ভেরিফিকেশন পাসওয়ার্ড (যদি থাকে): {Fore.WHITE}").strip()
                await client.sign_in(password=password)
                
        me = await client.get_me()
        print(f"\n{Fore.GREEN}[+] সফলভাবে একাউন্ট যুক্ত হয়েছে: {me.first_name} (@{me.username})")
    except Exception as e:
        print(f"{Fore.RED}[-] একাউন্ট যুক্ত করতে সমস্যা হয়েছে: {e}")
    finally:
        await client.disconnect()

async def remove_tg_account():
    print(f"\n{Fore.CYAN}--- Logout / Remove Telegram Account ---")
    sessions = get_all_sessions()
    
    if not sessions:
        print(f"{Fore.RED}[-] কোনো একাউন্ট/Session ফাইল পাওয়া যায়নি।")
        return

    print(f"{Fore.YELLOW}বর্তমানে যুক্ত থাকা একাউন্টসমূহ:")
    for idx, s in enumerate(sessions, 1):
        print(f"  [{idx}] {s}")
    print(f"  [{len(sessions) + 1}] সব একাউন্ট একসাথে লগআউট করুন")

    choice = input(f"\n{Fore.YELLOW}যে একাউন্টটি রিমুভ করতে চান তার নম্বর লিখুন [মেইন মেনুতে ফিরতে '0' বা 'b' চাপুন]: {Fore.WHITE}").strip()
    
    if choice in ['0', 'b', 'B']:
        return

    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(sessions):
            target_session = sessions[idx - 1]
            await logout_session_file(target_session)
        elif idx == len(sessions) + 1:
            confirm = input(f"{Fore.RED}আপনি কি সত্যিই সব একাউন্ট রিমুভ করতে চান? (y/n): {Fore.WHITE}").strip().lower()
            if confirm == 'y':
                for s in sessions:
                    await logout_session_file(s)
        else:
            print(f"{Fore.RED}[-] ভুল অপশন সিলেক্ট করেছেন!")

async def logout_session_file(session_name):
    filename = f"{session_name}.session"
    client = TelegramClient(session_name, API_ID, API_HASH)
    try:
        await client.connect()
        if await client.is_user_authorized():
            await client.log_out()
            print(f"{Fore.GREEN}[+] Telegram server থেকে সফলভাবে লগআউট করা হয়েছে: {session_name}")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Server-side logout করতে সমস্যা হয়েছে (অথবা আগে থেকেই লগআউট করা): {e}")
    finally:
        await client.disconnect()
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{Fore.GREEN}[+] Session ফাইলটি মুছে ফেলা হয়েছে: {filename}")

async def report_entity_with_client(session_name, target, selected_options, custom_message="", count=1, message_ids=None):
    client = TelegramClient(session_name, API_ID, API_HASH)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print(f"{Fore.YELLOW}[!] Session {session_name} ইজ নট অথরাইজড (লগইন নেই)। স্কিপ করা হচ্ছে।")
            return

        me = await client.get_me()
        user_label = me.first_name if me else session_name
        print(f"\n{Fore.CYAN}[*] Running report with account: {user_label} ({session_name})")

        entity = await client.get_input_entity(target)
        
        reason_map = {
            'spam': InputReportReasonSpam(),
            'violence': InputReportReasonViolence(),
            'pornography': InputReportReasonPornography(),
            'child_abuse': InputReportReasonChildAbuse(),
            'copyright': InputReportReasonCopyright(),
            'geo_irrelevant': InputReportReasonGeoIrrelevant(),
            'fake': InputReportReasonFake(),
            'illegal_drugs': InputReportReasonIllegalDrugs(),
            'personal_details': InputReportReasonPersonalDetails(),
            'other': InputReportReasonOther()
        }
        
        for i in range(1, count + 1):
            reason_key, sub_reason_text = random.choice(selected_options)
            selected_reason = reason_map.get(reason_key, InputReportReasonSpam())
            
            if sub_reason_text and custom_message:
                final_message = f"Category: {sub_reason_text}. Details: {custom_message}"
            elif sub_reason_text:
                final_message = f"Category: {sub_reason_text}. Violating Telegram Terms of Service."
            elif custom_message:
                final_message = custom_message
            else:
                final_message = "Violating Telegram Terms of Service."

            if message_ids:
                await client(ReportRequest(
                    peer=entity,
                    id=message_ids,
                    option=b'',
                    message=final_message
                ))
                print(f"{Fore.GREEN}[+] [{user_label}] [{i}/{count}] Submitted POST report -> Msg IDs: {message_ids} | Reason: {reason_key}")
            else:
                await client(ReportPeerRequest(
                    peer=entity,
                    reason=selected_reason,
                    message=final_message
                ))
                print(f"{Fore.GREEN}[+] [{user_label}] [{i}/{count}] Submitted PEER report -> Reason: {reason_key}")
                
            await asyncio.sleep(1.5)
            
    except Exception as e:
        print(f"{Fore.RED}[-] Failed to report using {session_name}. Error: {e}")
    finally:
        await client.disconnect()

def get_sub_reason(reason_choice):
    sub_reason_text = ""
    
    if reason_choice == '1': # Spam
        print(f"\n{Fore.CYAN}--- Spam এর নির্দিষ্ট টাইপ বেছে নিন ---")
        print(f"  [1] Impersonation")
        print(f"  [2] Deceptive or unrealistic financial claims")
        print(f"  [3] Malware, phishing")
        print(f"  [4] Fraudulent seller, product or service")
        print(f"  [5] Insults or false information")
        print(f"  [6] Promoting illegal content")
        print(f"  [7] Promoting other content")
        sub_choice = input(f"{Fore.YELLOW}সাব-অপশন সিলেক্ট করুন (1-7, ফাঁকা রাখতে Enter): {Fore.WHITE}").strip()
        sub_dict = {
            '1': 'Impersonation', '2': 'Deceptive or unrealistic financial claims',
            '3': 'Malware, phishing', '4': 'Fraudulent seller, product or service',
            '5': 'Insults or false information', '6': 'Promoting illegal content',
            '7': 'Promoting other content'
        }
        sub_reason_text = sub_dict.get(sub_choice, 'Spam')

    elif reason_choice == '2': # Violence
        print(f"\n{Fore.CYAN}--- Violence এর নির্দিষ্ট টাইপ বেছে নিন ---")
        print(f"  [1] Insults or false information")
        print(f"  [2] Graphic or disturbing content")
        print(f"  [3] Extreme violence, dismemberment")
        print(f"  [4] Hate speech or symbols")
        print(f"  [5] Calling for violence")
        print(f"  [6] Organized crime")
        print(f"  [7] Terrorism")
        print(f"  [8] Animal abuse")
        sub_choice = input(f"{Fore.YELLOW}সাব-অপশন সিলেক্ট করুন (1-8, ফাঁকা রাখতে Enter): {Fore.WHITE}").strip()
        sub_dict = {
            '1': 'Insults or false information', '2': 'Graphic or disturbing content',
            '3': 'Extreme violence, dismemberment', '4': 'Hate speech or symbols',
            '5': 'Calling for violence', '6': 'Organized crime',
            '7': 'Terrorism', '8': 'Animal abuse'
        }
        sub_reason_text = sub_dict.get(sub_choice, 'Violence')

    elif reason_choice == '3': # Pornography
        print(f"\n{Fore.CYAN}--- Pornography & Sexual Content এর টাইপ বেছে নিন ---")
        print(f"  [1] Child abuse")
        print(f"  [2] Illegal sexual services")
        print(f"  [3] Animal abuse")
        print(f"  [4] Non-consensual sexual imagery")
        print(f"  [5] Pornography")
        print(f"  [6] Other illegal sexual content")
        sub_choice = input(f"{Fore.YELLOW}সাব-অপশন সিলেক্ট করুন (1-6, ফাঁকা রাখতে Enter): {Fore.WHITE}").strip()
        sub_dict = {
            '1': 'Child abuse', '2': 'Illegal sexual services',
            '3': 'Animal abuse', '4': 'Non-consensual sexual imagery',
            '5': 'Pornography', '6': 'Other illegal sexual content'
        }
        sub_reason_text = sub_dict.get(sub_choice, 'Pornography')

    elif reason_choice == '4': # Child Abuse
        print(f"\n{Fore.CYAN}--- Child Abuse এর নির্দিষ্ট টাইপ বেছে নিন ---")
        print(f"  [1] Child sexual abuse")
        print(f"  [2] Child physical abuse")
        sub_choice = input(f"{Fore.YELLOW}সাব-অপশন সিলেক্ট করুন (1-2, ফাঁকা রাখতে Enter): {Fore.WHITE}").strip()
        sub_dict = {'1': 'Child sexual abuse', '2': 'Child physical abuse'}
        sub_reason_text = sub_dict.get(sub_choice, 'Child Abuse')

    elif reason_choice == '8': # Illegal Drugs / Goods
        print(f"\n{Fore.CYAN}--- Illegal Goods & Services এর টাইপ বেছে নিন ---")
        print(f"  [1] Weapons")
        print(f"  [2] Drugs")
        print(f"  [3] Fake documents")
        print(f"  [4] Counterfeit money")
        print(f"  [5] Hacking tools and malware")
        print(f"  [6] Counterfeit merchandise")
        print(f"  [7] Other goods and services")
        sub_choice = input(f"{Fore.YELLOW}সাব-অপশন সিলেক্ট করুন (1-7, ফাঁকা রাখতে Enter): {Fore.WHITE}").strip()
        sub_dict = {
            '1': 'Weapons', '2': 'Drugs', '3': 'Fake documents',
            '4': 'Counterfeit money', '5': 'Hacking tools and malware',
            '6': 'Counterfeit merchandise', '7': 'Other goods and services'
        }
        sub_reason_text = sub_dict.get(sub_choice, 'Illegal Goods and Services')

    elif reason_choice == '10': # Other
        print(f"\n{Fore.CYAN}--- Other এর নির্দিষ্ট টাইপ বেছে নিন ---")
        print(f"  [1] I don't like it")
        print(f"  [2] False information or defamation")
        print(f"  [3] Illegal adult content")
        print(f"  [4] Illegal goods and services")
        print(f"  [5] Something else")
        sub_choice = input(f"{Fore.YELLOW}সাব-অপশন সিলেক্ট করুন (1-5, ফাঁকা রাখতে Enter): {Fore.WHITE}").strip()
        sub_dict = {
            '1': "I don't like it", '2': 'False information or defamation',
            '3': 'Illegal adult content', '4': 'Illegal goods and services',
            '5': 'Something else'
        }
        sub_reason_text = sub_dict.get(sub_choice, 'Other')

    return sub_reason_text

def collect_reasons():
    reason_dict = {
        '1': 'spam', '2': 'violence', '3': 'pornography',
        '4': 'child_abuse', '5': 'copyright', '6': 'geo_irrelevant',
        '7': 'fake', '8': 'illegal_drugs', '9': 'personal_details', '10': 'other'
    }

    selected_options = []

    while True:
        print(f"\n{Fore.CYAN}রিপোর্টের কারণ বেছে নিন (বর্তমানে যুক্ত আছে: {len(selected_options)} টি রিজন):")
        print(f"  [1] Spam")
        print(f"  [2] Violence")
        print(f"  [3] Pornography")
        print(f"  [4] Child Abuse")
        print(f"  [5] Copyright")
        print(f"  [6] Geo Irrelevant")
        print(f"  [7] Fake Account/Channel")
        print(f"  [8] Illegal Goods and Services / Drugs")
        print(f"  [9] Personal Details (Doxxing)")
        print(f"  [10] Other")

        reason_choice = input(f"\n{Fore.YELLOW}অপশন নম্বর সিলেক্ট করুন (1-10): {Fore.WHITE}").strip()
        
        if reason_choice in reason_dict:
            reason_key = reason_dict[reason_choice]
            sub_reason_text = get_sub_reason(reason_choice)
            
            selected_options.append((reason_key, sub_reason_text))
            print(f"{Fore.GREEN}[+] রিজন যোগ করা হয়েছে: {reason_key} ({sub_reason_text if sub_reason_text else 'No Sub-reason'})")
            
            add_more = input(f"\n{Fore.YELLOW}আপনি কি আরও কোনো রিজন এড করতে চান? (y/n): {Fore.WHITE}").strip().lower()
            if add_more != 'y':
                break
        else:
            print(f"{Fore.RED}[-] সঠিক অপশন চাপুন!")

    if not selected_options:
        print(f"{Fore.RED}[-] কোনো রিজন সিলেক্ট করা হয়নি! ডিফল্ট Spam ধরা হলো।")
        selected_options.append(('spam', 'Spam'))

    return selected_options

async def start_reporting(is_post_report=False):
    sessions = get_all_sessions()
    if not sessions:
        print(f"{Fore.RED}[-] কোনো Telegram Account (.session ফাইল) পাওয়া যায়নি! আগে মেনু থেকে 3 সিলেক্ট করে একাউন্ট যুক্ত করুন।")
        return

    print(f"\n{Fore.GREEN}[*] মোট পাওয়া একাউন্ট (Sessions): {len(sessions)} টি -> {', '.join(sessions)}")

    target_input = input(f"\n{Fore.YELLOW}১. টার্গেট ইউজারনেম/চ্যানেল লিঙ্ক/পোস্ট লিঙ্ক দিন [মেইন মেনুতে ফিরতে '0' বা 'b' চাপুন]: {Fore.WHITE}").strip()
    if target_input in ['0', 'b', 'B']:
        return

    message_ids = []
    target_entity = target_input

    if "t.me/" in target_input:
        parts = target_input.strip('/').split('/')
        if parts[-1].isdigit():
            message_ids.append(int(parts[-1]))
            target_entity = parts[-2]
        else:
            target_entity = parts[-1]
    elif target_input.startswith("@"):
        target_entity = target_input.replace("@", "")

    if is_post_report and not message_ids:
        msg_id_input = input(f"{Fore.YELLOW}পোস্ট/মেসেজ ID দিন (একাধিক হলে কমা দিয়ে লিখুন, যেমন 10,11,12): {Fore.WHITE}").strip()
        if msg_id_input in ['0', 'b', 'B']:
            return
        try:
            message_ids = [int(x.strip()) for x in msg_id_input.split(',') if x.strip().isdigit()]
        except ValueError:
            print(f"{Fore.RED}[-] সঠিক পোস্ট ID দিন!")
            return

    selected_options = collect_reasons()

    count_input = input(f"\n{Fore.YELLOW}৩. প্রতিটি একাউন্ট থেকে কতবার রিপোর্ট পাঠাতে চান? (সংখ্যা লিখুন) [ব্যাকে যেতে 'b']: {Fore.WHITE}").strip()
    if count_input in ['b', 'B']:
        return
    
    try:
        report_count = int(count_input)
        if report_count == 0:
            return
    except ValueError:
        print(f"{Fore.RED}[-] ভুল সংখ্যা দিয়েছেন! ডিফল্ট হিসেবে ১ নির্ধারণ করা হলো।")
        report_count = 1
        
    description = input(f"\n{Fore.YELLOW}৪. কাস্টম বিবরণ/মেসেজ দিতে চাইলে লিখুন (ফাঁকা রাখতে Enter চাপুন): {Fore.WHITE}").strip()

    print(f"\n{Fore.GREEN}[*] Report Process Started -> Target: {target_entity} | Target Count per Account: {report_count} | Accounts: {len(sessions)}")
    print(f"{Fore.CYAN}----------------------------------------------------------------------")
    
    for session in sessions:
        await report_entity_with_client(
            session_name=session,
            target=target_entity,
            selected_options=selected_options,
            custom_message=description,
            count=report_count,
            message_ids=message_ids
        )

    print(f"\n{Fore.GREEN}[✔] সব একাউন্ট থেকে রিপোর্ট পাঠানোর কাজ সম্পন্ন হয়েছে!")

async def main():
    animate_banner()

    while True:
        print(f"\n{Fore.CYAN}মেইন মেনু থেকে একটি অপশন সিলেক্ট করুন:")
        print(f"  [1] Start Account/Channel Report")
        print(f"  [2] Start Post/Message Report")
        print(f"  [3] Add TG Account")
        print(f"  [4] Logout / Remove TG Account")
        print(f"  [5] Exit / Program Close")
        
        main_choice = input(f"\n{Fore.YELLOW}অপশন বেছে নিন (1/2/3/4/5): {Fore.WHITE}").strip()
        
        if main_choice == '1':
            await start_reporting(is_post_report=False)
        elif main_choice == '2':
            await start_reporting(is_post_report=True)
        elif main_choice == '3':
            await add_tg_account()
        elif main_choice == '4':
            await remove_tg_account()
        elif main_choice == '5':
            print(f"{Fore.RED}[*] প্রোগ্রাম বন্ধ করা হচ্ছে...")
            sys.exit()
        else:
            print(f"{Fore.RED}[-] ভুল অপশন সিলেক্ট করেছেন! সঠিক অপশন চাপুন।")

if __name__ == '__main__':
    asyncio.run(main())
