from urllib import parse, request

from kivy.app import App #We need to import the bits of kivy we need as we need them as importing everything would slow the app down unnecessarily
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget #this is a thing that you want the App to display
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
import urllib.request, json

GAME_ENDPOINT = "http://ships.kgz.sh/game"


class Lesson0(Widget): #this defines the instance of the widget.
    pass # pass is used to keep the class valid but allow it not to contain anything - At the moment our widget is not defined.

EMPTY = 0
MISS = 1
HIT =2


def state(rows, cols):
    a = []
    for i in range(rows):
        a.append([])
        for j in range(cols):
            a[i].append(EMPTY)
    return a

def submitMove(x,y):
    data = parse.urlencode({
        "x": x,
        "y:": y
    }
    ).encode()
    req = request.Request(GAME_ENDPOINT, data=data, method='GET')
    resp = request.urlopen(req)
    print(resp)


def genButton(state, x, y):
    if state == HIT:
        button = Button(text='HIT', width=50, background_color=[255, 0, 0, 255])
    elif state == MISS:
        button = Button(text='MISS', width=50, background_color=[255 ,255, 0, 255])
    else:
        button = Button(text='UNKNOWN', width=50,
                    background_color=[0, 255, 0, 255])
    button.bind(on_press=lambda _: submitMove(x,y))
    return button


class MyApp(App):


    def get_score(self):
        return "[size=200]Hits: {}, misses: {}[/size]".format(self.hits, self. misses)

    def refresh(self):
        self.hits = 0
        self.misses = 0
        cols = 10
        rows = 10
        with urllib.request.urlopen(
                GAME_ENDPOINT) as url:
            data = json.loads(url.read().decode())
            board = data["board"]
        for i in range(rows):
            for j in range(cols):
                state = board[i][j]
                if state == HIT:
                    self.hits +=1
                elif state == MISS:
                    self.misses += 1
                self.layout.add_widget(genButton(state=state, x=i, y=j))

    def build(self):
        cols = 10
        rows = 10
        box = BoxLayout(padding=10, orientation='vertical')
        self.score = Label(text='Score: 0', markup=True)
        self.layout = GridLayout(cols=cols, row_force_default=True,
                                 row_default_height=50)

        self.refresh()
        Clock.schedule_interval(self.update, 1)

        box.add_widget(self.layout)
        box.add_widget(self.score)

        return box

    def update(self, *args):
        widgets = []
        for child in self.layout.children:
            widgets.append(child)
        for child in widgets:
            self.layout.remove_widget(child)
        self.score.text = self.get_score()
        self.refresh()



if __name__ == '__main__': #Documentation suggests that each program file should be called main.py but I think that only matters if you're creating the final App to go onto a phone or tablet we're a long way off from that yet

    app = MyApp()
    MyApp().run() #This must match the name of your App