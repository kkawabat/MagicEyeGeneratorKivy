import os
from pathlib import Path
import numpy as np
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from PIL import Image
from io import BytesIO

from magic_eye_generator.sis_generator import gen_sis
from magic_eye_generator.ui.widgets.file_system_dialogs import LoadDialogPopup, SaveDialogPopup

Builder.load_file(r'ui\widgets\magic_eye_widget.kv')
data_dir = Path(__file__).parents[3].joinpath('data')


class MagicEyeWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(MagicEyeWidget, self).__init__(**kwargs)
        self._popup = None
        self.depth_val = 0
        self.num_strips = 10
        self.texture_fixed_width = 100
        self.main_image_obj = KivyImage()
        self.depth_map_source = None
        self.texture_map_source = None
        self.magic_eye_image = None

    def load_depth_map(self, *args):
        def load(path, filename):
            self.depth_map_source = os.path.join(path, filename[0])
            self.view_depth_map()
        LoadDialogPopup(title='load depth map', load_func=load, default_dir=str(data_dir.joinpath('depth_map'))).open()

    def view_depth_map(self, *args):
        self.ids.img_viewer.source = self.depth_map_source

    def load_texture_map(self, *args):
        def load(path, filename):
            self.texture_map_source = os.path.join(path, filename[0])
            self.view_texture_map()
        LoadDialogPopup(title='load texture map', load_func=load, default_dir=str(data_dir.joinpath('texture'))).open()

    def view_texture_map(self, *args):
        self.ids.img_viewer.source = self.texture_map_source

    def view_magic_eye_image(self, *args):
        self.magic_eye_image = self.gen_magic_eye()
        self.ids.img_viewer.texture = self.magic_eye_image.texture

    def gen_magic_eye(self):
        # todo generate magic eye
        canvas_img = gen_sis(self.depth_map_source, self.texture_map_source,
                             self.depth_val, self.num_strips, self.texture_fixed_width)
        data = BytesIO()
        Image.fromarray(canvas_img.astype(np.uint8), mode="RGBA").save(data, format='png')
        data.seek(0)
        return CoreImage(data, ext='png')

    def save_magic_eye_image(self, *args):
        def save(path, filename):
            self.magic_eye_image.save(os.path.join(path, filename[0]))

        SaveDialogPopup(title='save magic eye image', save_func=save,
                        default_dir=str(data_dir.joinpath('magic_eye_results'))).open()

    def update_depth(self, depth_value):
        print(f"updated depth to {depth_value}")
        self.depth_val = depth_value

    def update_num_strips(self, num_strips):
        print(f"updated # strips to {num_strips}")
        self.num_strips = num_strips
