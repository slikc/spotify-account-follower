import string, random, requests, time, json, ctypes
from colorama import init, Fore, Back, Style
requests.packages.urllib3.disable_warnings()

counter = 0
def main():
    global counter
    email = ("").join(random.choices(string.ascii_letters + string.digits, k = 8)) + "@gmail.com"
    password = ("").join(random.choices(string.ascii_letters + string.digits, k = 8))
    data = f"birth_day=1&birth_month=01&birth_year=1970&collect_personal_info=undefined&creation_flow=&creation_point=https://www.spotify.com/uk/&displayname=github.com/slikc&email={email}&gender=neutral&iagree=1&key=a1e486e2729f46d6bb368d6b2bcda326&password={password}&password_repeat={password}&platform=www&referrer=&send-email=1&thirdpartyemail=0&fb=0"
    session = requests.Session()
    headers = {
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://www.spotify.com/",
                "accept-language": "en-US,en;q=0.9",
    }
    create = session.post("https://spclient.wg.spotify.com/signup/public/v1/account/", data=data, headers=headers, verify=False)
    if create.status_code == 200:
        if "login_token" in create.text:
            print(f"{Fore.GREEN}[+]{Fore.RESET} GOT LOGIN TOKEN")
            logtoken = create.json()["login_token"]
            print(f"{Fore.GREEN}[+]{Fore.RESET} CREATED ACCOUNT: " + email + ":" + password)


    r = session.get("https://www.spotify.com/uk/signup/?forward_url=https://accounts.spotify.com/en/status&sp_t_counter=1", verify=False)
    #get the csrf token from the text "csrfToken":"<token>" by splitting the text
    csrf = r.text.split('"csrfToken":"')[1].split('"')[0]
    if csrf == "":
        print(f"{Fore.RED}[-]{Fore.RESET} FAILED TO GET CSRF TOKEN")
        exit()
    def get_token(login_token):
        headers = {
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRF-Token": csrf,
                "Host": "www.spotify.com"
                }
        session.post("https://www.spotify.com/api/signup/authenticate", headers=headers, data="splot=" + login_token, verify=False)
        headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "accept-language": "en",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "spotify-app-version": "1.1.52.204.ge43bc405",
                "app-platform": "WebPlayer",
                "Host": "open.spotify.com",
                "Referer": "https://open.spotify.com/"
            }
        try:
            r = session.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player", headers = headers, verify=False)
            return r.json()["accessToken"]
        except:
            return None

    auth_token = get_token(logtoken)
    #open the json config file
    with open("config.json", "r") as f:
        config = json.load(f)
        idd = config["id"]
    headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "accept-language": "en",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "app-platform": "WebPlayer",
                "Referer": "https://open.spotify.com/",
                "spotify-app-version": "1.1.52.204.ge43bc405",
                "authorization": "Bearer {}".format(auth_token),
            }
    followuser = session.put("https://api.spotify.com/v1/me/following?type=user&ids="+ idd, headers=headers, verify=False)
    accountstats = requests.get(f"https://spclient.wg.spotify.com/user-profile-view/v3/profile/{idd}?playlist_limit=0&artist_limit=0&episode_limit=0&market=from_token", headers=headers, verify=False).json()
    accountstats = accountstats["followers_count"]
    print(f"{Fore.BLUE}[INFO]{Fore.RESET} {Fore.CYAN}Current User Follows: {accountstats}")
    if followuser.status_code == 204:
        print(f"{Fore.GREEN}[+]{Fore.RESET} FOLLOWED USER")
        counter += 1

    else:
        print(f"{Fore.RED}[-]{Fore.RESET} FAILED TO FOLLOW USER")

if __name__ == "__main__":
    main()
