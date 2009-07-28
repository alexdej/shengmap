require 'rubygems'
require 'RMagick'


map = Magick::ImageList.new("map/base.png")
fj = Magick::ImageList.new("map/FJ.png")

#white_bg = Magick::Image.new(img.columns, img.rows)
map = map.composite(fj, 0, 0, Magick::OverCompositeOp)
#img = white_bg.composite(mid, 50, 15, Magick::OverCompositeOp)

#img.write('after.jpg')
map.write('map.jpg')
