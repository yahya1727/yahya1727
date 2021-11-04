from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.picker import MDTimePicker, MDThemePicker, SelectorLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.uix.snackbar import Snackbar
from kivy.core.audio import Sound, SoundLoader
from time import strftime, time
from datetime import datetime
from kivy.clock import Clock

going_time = datetime.now().strftime("%H:%M:%S")

app_ui = '''
FloatLayout:

    MDBottomNavigation:

        MDBottomNavigationItem:
            id: timer_scr
            name: "screen 1"
            text: "Timer"
            icon: "clock-time-four"
            MDToolbar:
                title: "Timer"
                pos_hint: {"top":1}
            MDLabel:
                id: timers
                text: "00:00:00"
                font_size:40
                pos_hint: {"center_x":0.8,"center_y":0.7}
                bold: True
            MDRaisedButton:
                id: stop_btn
                text: "STOP"
                sont_size: 24
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                disabled: True
                on_press: app.stopMusic()
            MDIconButton:
                icon: "plus"
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                user_font_size: "50sp"
                pos_hint: {'center_x': .9, 'center_y': 0.1}
                on_release: app.show_time_picker()

        MDBottomNavigationItem:
            name: "screen 2"
            text: "Settings"
            icon: "cog"
            MDToolbar:
                title: "Settings"
                pos_hint: {"top":1}
            ScrollView:
                size_hint_y: 0.90

                MDList:

                    OneLineListItem:
                        text: "Change Theme And Appearance"
                        on_press: app.show_theme_picker() 
'''

class TimerApp(MDApp):
    def build(self):
        return Builder.load_string(app_ui)

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.schedule)
        time_dialog.open()

    def schedule(self, *args):
        Clock.schedule_once(self.alarm, 1)
        Snackbar(text="Timer Scheduled! (Don't Close The App!)").open()

    def alarm(self, *args):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if self.root.ids.timers.text == current_time:
                self.startMusic()
                break

    def stopMusic(self, *args):
        self.tone.stop()
        self.root.ids.timers.text = "00:00:00"
        self.root.ids.stop_btn.disabled = True

    def startMusic(self, *args):
        self.tone = SoundLoader.load("alarm1.wav")
        self.root.ids.stop_btn.disabled = False
        self.tone.loop = True
        self.tone.play()

    def get_time(self, instance, time):
        self.alarmtime = time
        self.root.ids.timers.text = str(self.alarmtime)

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def show_confirmation_dialog(self):
        close_btn = MDFlatButton(
            text="Close",
            on_release=self.close_dialog
        )
        self.dialog = MDDialog(
            title="Change Alarm Sound",
            text="This feature is still in progress!",
            buttons=[close_btn]
        )
        self.dialog.open()

    def close_dialog(self, event):
        self.dialog.dismiss()


if __name__ == "__main__":
    app = TimerApp()
    app.run()
