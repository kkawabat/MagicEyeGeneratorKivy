from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
Builder.load_file('file_system_dialogs.kv')


class LoadDialogPopup(Popup):
    def __init__(self, title, load_func):
        super(LoadDialogPopup).__init__(title=title, size_hint=(0.9, 0.9),
                                        content=LoadDialog(load=load_func, cancel=self.dismiss))


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def run_load(self, path, selection):
        # todo sanitize input
        self.load(path, selection)
        self.dismiss()


class SaveDialogPopup(Popup):
    def __init__(self, title, save_func):
        self.save = save_func
        super(SaveDialogPopup).__init__(title=title, size_hint=(0.9, 0.9),
                                        content=SaveDialog(save=save_func, cancel=self.dismiss))


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def run_save(self, path, text):
        # todo sanitize input
        self.save(path, text)
        self.dismiss()
