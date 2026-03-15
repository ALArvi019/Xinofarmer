
from movePlayer import moveplayer
from sendTextToBot import SendTextToBot
import time



for i in list(range(4))[::-1]:
     print(i+1)
     time.sleep(1)

send_text_to_bot = SendTextToBot()

Moveplayer = moveplayer("LDPlayer", None, "path\\to\\immortal_xinofarmer\\inc\\img", "en", send_text_to_bot, True)

Moveplayer.move_circle_8_directions(3.5)