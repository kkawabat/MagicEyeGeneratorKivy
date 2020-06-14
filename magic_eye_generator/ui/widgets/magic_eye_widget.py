import os

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from magic_eye_generator.ui.widgets.file_system_dialogs import LoadDialogPopup, SaveDialogPopup

Builder.load_file(r'ui\widgets\magic_eye_widget.kv')


class MagicEyeWidget(BoxLayout):
    img_source = StringProperty('texture_example_image.png')

    def __init__(self, **kwargs):
        super(MagicEyeWidget, self).__init__(**kwargs)
        self._popup = None
        self.depth_map_source = None
        self.texture_map_source = None
        self.magic_eye_source = None

    def load_depth_map(self):
        def load(path, filename):
            self.depth_map_source = os.path.join(path, filename[0])

        LoadDialogPopup(title='load depth map', load_func=load).open()

    def view_depth_map(self):
        self.img_source = self.depth_map_source

    def load_texture_map(self):
        def load(path, filename):
            self.texture_map_path = os.path.join(path, filename[0])

        LoadDialogPopup(title='load texture map', load_func=load).open()

    def view_texture_map(self):
        self.img_source = self.texture_map_source

    def view_magic_eye_image(self):
        self.gen_magic_eye()
        self.img_source = self.magic_eye_image_io.name

    def gen_magic_eye(self):
        # todo generate magic eye
        pass

    def save_magic_eye_image(self):
        def save(path, filename):
            # todo save magic_eye to file
            os.path.join(path, filename[0])

        SaveDialogPopup(title='save magic eye image', save_func=save).open()

    def update_depth(self, depth_value):
        print(f"updated depth to {depth_value}")

    def update_num_strips(self, num_strips):
        print(f"updated # strips to {num_strips}")
