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
        self.window.println("I'll keep trying!")
        self.window.println()

        wifi_attempts = 0
        while not wifi.status():
            # wifi.stop()
            wifi_attempts += 1
            self.window.println("Attempt {}".format(wifi_attempts))
            wifi.connect()
            wifi.wait()

        if wifi.status():
            self.window.println()
            self.window.println("Getting you a DUCK FACT...")
            fact_json = urequests.get("https://03vpefsitf.execute-api.eu-west-1.amazonaws.com/prod/")
            self.window.println("found one...")
            self.duck = ujson.loads(fact_json.content)
            wifi.disconnect()

        self.quack()

    def on_start(self):
        super().on_start()

    def quack(self):
        self.window.redraw()
        x = 2
        y = 13

        message = self.duck["fact"]

        for line in self.window.flow_lines(message):
            self.window.display.text(font, line, x, y, WHITE, BLACK)
            y += font.HEIGHT+1

        y += font.HEIGHT+1
        self.window.display.text(font, "QUACK!", x, y, WHITE, BLACK)


main = DuckFact
