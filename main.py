import os
import audio_metadata
from kivy.core.audio import SoundLoader

from kivymd.app import MDApp, ThemeManager
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.imagelist import SmartTile
from kivymd.uix.slider import MDSlider
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label




class Player():

    def __init__(self):
        self._isplaying = False

        self._player = SoundLoader()

        self._curent_music = None
        self._playing_path = None

    def play(self, url):
        if self._curent_music:
            self._player.stop()
        try:
            self._player.load(str(url))
            self._player.play()
            self._isplaying = True
        except Exception as e:
            self._isplaying = False

    def pause(self):
        if self._curent_music:
            self._player.pause()

    def stop(self):
        if self._curent_music:
            self._player.stop()
            self._player.unload(self._playing_path)
            self._isplaying = False

    def seek(self, position):
        try:
            self._player.seek()
        except:
            pass


class PlayingPage(BoxLayout):

    def __init__(self ):
        super().__init__()
        self.pointer= 0
        self.state_ = {"isPlaying": True,
                       "title": "Test Title", "artist": "J. Cole","lenght":100.0}
        self.orientation = "vertical"
        self.toolbar = MDToolbar(title="Now Playing")
        self.toolbar.left_action_items = [["arrow-left", self.back]]
        self.add_widget(self.toolbar)
        self.upper_container = BoxLayout()
        self.upper_container.orientation = "vertical"
        self.title = MDLabel(text=self.state_['title'] +'\n'+self.state_['artist'], halign="center",font_style="H5")
        self.upper_container.add_widget(self.title)
        self.lower_container = BoxLayout()
        self.lower_container.orientation = "horizontal"
        self.lower_container.halign="center"
        self.lower_container.size_hint_max_y=0.2
        self.slider_time_line = BoxLayout()
        self.slider_time_line.orientation = "horizontal"
        self.play_btn = MDIconButton(icon="pause")
        self.play_btn.on_press = self.pause_
        self.next_Btn = MDIconButton(icon="skip-forward")
        self.slider = MDSlider(min=0 , max=self.state_['lenght'])
        self.prev_Btn = MDIconButton(icon="skip-backward")
        self.lower_container.add_widget(self.prev_Btn)
        self.lower_container.add_widget(self.play_btn)
        self.lower_container.add_widget(self.next_Btn)
        self.slider_time_line.add_widget(self.slider)
        self.add_widget(self.upper_container)
        self.add_widget(self.slider_time_line)
        self.add_widget(self.lower_container)

    def init_config(self,title,artist,lenght):
        if not artist:
            artist=""
        self.title.text = str(title )+ "\n" + str(artist)
        self.slider.max = lenght

    def pause_(self):
        self.state_['isPlaying'] = not self.state_['isPlaying']
        self.slider.max = self.state_['lenght']
        if self.state_['isPlaying']:
            self.play_btn.icon = "pause"
            app.playing.play()
        else:
            self.play_btn.icon = "play"
            app.playing.stop()

    def back(self, instance):
        app.screen_manager.current = "listpage"


class SettingsPage(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = "vertical"
        self.toolbar = MDToolbar(title="Setting")
        self.toolbar.left_action_items = [["arrow-left", self.back]]
        self.add_widget(self.toolbar)
        self.container = BoxLayout()
        label = MDLabel(text="", halign="center")
        self.container.add_widget(label)
        self.add_widget(self.container)

    def back(self, instance):
        app.screen_manager.current = "listpage"


class ListPage(BoxLayout):
    def __init__(self):
        super().__init__()
        self.row = 2
        self.music_list = get_all_music('C:\\Users\\roseBlack\\Music')
        self.orientation = "vertical"
        self.toolbar = MDToolbar(title="Music Player")
        self.toolbar.right_action_items = [
            ["database-settings", lambda x: self.goto_setting()]]
        self.add_widget(self.toolbar)
        scroll_list = ScrollView()
        dml = MDList()
        self.counter = 0
        for music in self.music_list:
            meta = music['meta']
            path = music['path']
            self.dl = (TwoLineListItem(
                text=meta['title'] or "Unkown", secondary_text=meta['artist'] or 'Unkown', id=str(self.counter)))
            self.dl.bind(on_press=self.to_playing)
            dml.add_widget(self.dl)
            self.counter += 1
        scroll_list.add_widget(dml)
        self.add_widget(scroll_list)

    def to_playing(self, isinstance):
        current = self.music_list[int(isinstance.id)] ;
        app.play(self.music_list[int(isinstance.id)]['path'])
        app.screen_manager.current = "playingpage"
        app.playingpage.init_config(current['meta']['title'],current['meta']['artist'],app.playing.length)
        

    def goto_setting(self):
        app.screen_manager.current = "settingspage"


class MusicApp(MDApp):
    def __init__(self):
        super().__init__()
        self._player = SoundLoader()
        self._isplaying = False
        self.playing = None

    def get_length(self):
        if self.playing:
            return self.playing.length
        else:
            return 0

    def play(self, isinstance):
        if self.playing:
            self.playing.unload()
        self.playing = self._player.load(str(isinstance))
        self.playing.play()
        self._isplaying = True

    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Indigo"
        self.screen_manager = ScreenManager()
        self.listpage = ListPage()
        self.playingpage = PlayingPage()
        self.settinsgpage = SettingsPage()

        screen = Screen(name="listpage")
        screen.add_widget(self.listpage)
        self.screen_manager.add_widget(screen)

        screen = Screen(name="playingpage")
        screen.add_widget(self.playingpage)
        self.screen_manager.add_widget(screen)

        screen = Screen(name="settingspage")
        screen.add_widget(self.settinsgpage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


def get_all_music(path):
    print(path)
    music_list = []
    for root, dirnames, filenames in os.walk(path):
        for nm in filenames:
            if os.path.splitext(nm)[1] == ".mp3":
                music_list.append({"path": str(os.path.join(
                    root, nm)), "meta": get_meta(str(os.path.join(root, nm)))})
    return music_list


def get_meta(music):
    metadata = audio_metadata.load(music)
    duration = None
    artist = None
    title = None
    try:
        artist = str(metadata['tags']['artist'][0])
    except:
        pass
    try:
        title = str(metadata['tags']['title'][0])
    except:
        pass
    try:
        duration = str(metadata['streaminfo']['duration'])
    except:
        pass
    return {"artist": artist, "duration": duration, "title": title}


if __name__ == "__main__":
    app = MusicApp()
    app.run()
