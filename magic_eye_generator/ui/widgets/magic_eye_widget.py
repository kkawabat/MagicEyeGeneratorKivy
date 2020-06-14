from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file(r'ui\widgets\magic_eye_widget.kv')


class MagicEyeWidget(BoxLayout):
    magic_eye_img_source = StringProperty('texture_example_image.png')

    def __init__(self, **kwargs):
        super(MagicEyeWidget, self).__init__(**kwargs)

    def load_image(self):
        pass

    def view_image(self):
        pass

    def load_texture_map(self):
        pass

    def view_texture_map(self):
        pass

    def view_magic_eye_image(self):
        pass

    def save_magic_eye_image(self):
        pass

    def update_depth(self, depth_value):
        print(f"updated depth to {depth_value}")

    def update_num_strips(self, num_strips):
        print(f"updated # strips to {num_strips}")