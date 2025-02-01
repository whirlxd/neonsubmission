import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import requests
import urllib.parse
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
group_root = displayio.Group()
group_text = displayio.Group()
API_KEY = #replace with your free  api key from dashboard of brawl stars api
def get_brawl_stars_stats(player_tag):
    url = f"https://api.brawlstars.com/v1/players/{player_tag}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {
            "error": "Request failed",
            "status_code": response.status_code,
            "reason": response.reason,
            "text": response.text
        }

    data = response.json()

    try:
        trophies = data.get("trophies", "N/A")
        wins = data.get("wins", 0)
        losses = data.get("losses", 1)
        kd_ratio = data.get("soloVictories", 0) / max(1, data.get("duoVictories", 1))
        win_rate = round((wins / (wins + losses)) * 100, 2)

        return {
      trophies,win_rate,kd_ratio
        }
    except KeyError:
        return {"error": "Could not extract stats"}




stats =get_brawl_stars_stats(urllib.parse.quote("username"))
statlist = list(stats)
trophies = statlist[0]
winrate = statlist[1]
kd = round(statlist[2)])

text_4 = adafruit_display_text.label.Label(
     terminalio.FONT,
    color=0x59d704,
    text=f"trophies {trophies}")
text_4.x = 1
text_4.y = 5
group_text.append(text_4)
text_5 = adafruit_display_text.label.Label(
     terminalio.FONT,
    color=0x490af5,
    text=f"winrate {winrate}")
text_5.x = 0
text_5.y = 15
group_text.append(text_5)
text_6 = adafruit_display_text.label.Label(
     terminalio.FONT,
    color=0xc00c0c,
    text=f"kda {kd}")
text_6.x = 1
text_6.y = 24
group_text.append(text_6)
group_root.append(group_text)
display.root_group = group_root
display.refresh(minimum_frames_per_second=0)
