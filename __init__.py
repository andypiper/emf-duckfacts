import wifi
import urequests, ujson

import vga2_8x16 as font

from tidal import *
from app import TextApp


class DuckFact(TextApp):
    TITLE = "Duck Fact"
    BG = BLACK
    FG = WHITE

    duck = {}

    def on_activate(self):
        super().on_activate()
        self.rotate()

        self.window.println("Connecting to wifi...")
        self.window.println()
        self.window.println("if this fails, keep trying")
        self.window.println()

        wifi_attempts = 0
        while not wifi.status():
            wifi.stop()
            wifi_attempts += 1
            self.window.println("attempt {}".format(wifi_attempts))
            wifi.connect()
            wifi.wait()

        if wifi.status():
            self.window.println("loading DUCK FACT...")
            fact_json = urequests.get("https://03vpefsitf.execute-api.eu-west-1.amazonaws.com/prod/")
            self.duck = ujson.loads(fact_json.content)
            self.window.println("loaded!")
            wifi.disconnect()

        self.quack()

    def on_start(self):
        super().on_start()

    def quack(self):
        self.window.redraw()
        x = 2
        y = 13
        self.window.display.text(font, self.duck["fact"], x, y, WHITE, BLACK)
        y += font.HEIGHT+1
        self.window.display.text(font, "", x, y, WHITE, BLACK)


main = DuckFact
