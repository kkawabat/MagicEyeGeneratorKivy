## MagicEyeGenerator
This project generates [magic eye](https://www.youtube.com/watch?v=v8O8Em_RPNg) illusion pictures with custom images and textures.  
 
![](doc/squirrel_magic_eye1.png)

### usage

#### geneerate magic eye image
 
`python main.py` to load the kivy app  
- choose your depth map image (default files in data/depth_map folder)  
- choose your texture image (default files in data/texture folder) 
- run "generate magic eye" to generate image in memory
- change slider to adjust parameters if the illusion looks wonky
- save image to file   

![demo.gif](doc/demo.gif)  
output image zoomed  
![demo.gif](doc/squirrel_magic_eye.png)

This app also support animated gif depth map (experimental)  

#### extract hidden image from magic eye image (experimental)
You can also extract hidden image from magic eye image (see sis_degenerator.py)  

![demo.gif](doc/extracted_squirrel_hidden_image.PNG)



### installation
requires:  
Kivy (2.0.0rc2)  
numpy  
pillow

`python setup.py install`


### resources
#### stereogram resource
https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-41-real-time-stereograms

#### app related resources
https://kivy.org/doc/stable/examples/gen__canvas__texture__py.html

https://stackoverflow.com/a/52340135/4231985


#### aknowledgement
This app is dedicated to long time mentor and friend @visarberisha who suffers from debilitating inability to see magic eye illusions 