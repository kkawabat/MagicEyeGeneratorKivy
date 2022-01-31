import os
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout

from magic_eye_generator.sis_degenerator import degen_sis
from magic_eye_generator.sis_generator import gen_sis
from magic_eye_generator.ui.widgets.file_system_dialogs import LoadDialogPopup, SaveDialogPopup

Builder.load_file(r'ui\widgets\magic_eye_widget.kv')
data_dir = Path(__file__).parents[3].joinpath('data')


class MagicEyeWidget(BoxLayout):
    depth_val = NumericProperty(.5)
    num_strips = NumericProperty(10)
    strip_width = NumericProperty(100)

    def __init__(self, **kwargs):
        super(MagicEyeWidget, self).__init__(**kwargs)
        self._popup = None
        self.depth_map_source = None
        self.texture_map_source = None
        self.magic_eye_image = None

    def load_depth_map(self, *args):
        def load(path, filename):
            self.depth_map_source = os.path.join(path, filename[0])
            self.ids.img_viewer.source = self.depth_map_source
        LoadDialogPopup(title='load depth map', load_func=load, default_dir=str(data_dir.joinpath('depth_map'))).open()

    def load_texture_map(self, *args):
        def load(path, filename):
            self.texture_map_source = os.path.join(path, filename[0])
            self.ids.img_viewer.source = self.texture_map_source
        LoadDialogPopup(title='load texture map', load_func=load, default_dir=str(data_dir.joinpath('texture'))).open()

    def view_magic_eye_image(self, *args):
        self.magic_eye_image = self.gen_magic_eye()
        if isinstance(self.magic_eye_image, str):
            self.ids.img_viewer.source = self.magic_eye_image
        else:
            self.ids.img_viewer.texture = self.magic_eye_image.texture

    def gen_magic_eye(self):
        canvas_img = gen_sis(self.depth_map_source, self.texture_map_source,
                             self.depth_val, self.num_strips, self.strip_width)
        data = BytesIO()
        if isinstance(canvas_img, Image.Image):
            canvas_img.save(data, format='png')
            data.seek(0)
            return CoreImage(data, ext='png')
        else:
            # very hacky way of getting image to display (save it as a temporary image to be used as a source)
            # because I couldn't figure out how to load gif as image in memory
            # canvas_img[0].save(data, format='gif', append_images=canvas_img[1:],
            #                    save_all=True, duration=100, loop=0, optimize=False, )
            # data.seek(0)
            # a = CoreImage(data, ext='gif')
            # a.anim_reset(True)
            canvas_img[0].save('tmp.gif', format='gif', append_images=canvas_img[1:],
                               save_all=True, duration=100, loop=0, optimize=False,)
            return 'tmp.gif'

    def decode_magic_eye_image(self, *args):

        def load(path, filename):
            magic_eye_image_source = os.path.join(path, filename[0])
            self.ids.img_viewer.source = magic_eye_image_source

            decoded_img = degen_sis(magic_eye_image_source)
            data = BytesIO()
            decoded_img.save(data, format='png')
            data.seek(0)
            decoded_img_cor = CoreImage(data, ext='png')
            self.ids.img_viewer.texture = decoded_img_cor.texture

        LoadDialogPopup(title='load magic eye', load_func=load, default_dir=str(data_dir.joinpath('magic_eye_results'))).open()

    def save_magic_eye_image(self, *args):
        def save(path, filename):
            self.magic_eye_image.save(os.path.join(path, filename))

        SaveDialogPopup(title='save magic eye image', save_func=save,
                        default_dir=str(data_dir.joinpath('magic_eye_results'))).open()

    def update_depth(self, slider, touch):
        if self.depth_val != slider.value:
            self.depth_val = slider.value
            # self.view_magic_eye_image()

    def update_num_strips(self, slider, touch):
        if self.num_strips != slider.value:
            self.num_strips = slider.value
            # self.view_magic_eye_image()

    def update_strip_width(self, slider, touch):
        if self.strip_width != slider.value:
            self.strip_width = slider.value
            # self.view_magic_eye_image()
