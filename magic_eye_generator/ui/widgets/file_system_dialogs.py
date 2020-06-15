from pathlib import Path

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

Builder.load_file(str(Path(__file__.replace('.py', '.kv'))))
data_dir = Path(__file__).parents[3].joinpath('data')


class LoadDialogPopup(Popup):
    def __init__(self, title, load_func, default_dir=None):
        super().__init__(title=title, size_hint=(0.9, 0.9), auto_dismiss=False,
                         content=LoadDialog(load=load_func, cancel=self.dismiss, default_dir=default_dir))


class LoadDialog(FloatLayout):
    default_dir = StringProperty(str(data_dir))
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, default_dir=None, **kwargs):
        super().__init__(**kwargs)
        self.default_dir = default_dir

    def run_load(self, path, selection):
        # todo sanitize input
        self.load(path, selection)
        self.cancel()

    @staticmethod
    def file_filter(directory, filename):
        return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))


class SaveDialogPopup(Popup):
    def __init__(self, title, save_func, default_dir):
        self.save = save_func
        super().__init__(title=title, size_hint=(0.9, 0.9), auto_dismiss=False,
                         content=SaveDialog(save=save_func, cancel=self.dismiss, default_dir=default_dir))


class SaveDialog(FloatLayout):
    default_dir = StringProperty(str(data_dir))
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, default_dir=None, **kwargs):
        super().__init__(**kwargs)
        self.default_dir = default_dir

    def run_save(self, path, text):
        # todo sanitize input
        self.save(path, text)
        self.cancel()
