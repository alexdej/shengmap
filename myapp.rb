require 'rubygems'
require 'sinatra'
require 'RMagick'

get '/' do
  # TODO: want to have a help page here but for now just redirect to the map
  redirect '/map'
end
get '/map' do
  content_type 'image/png'
  headers['Cache-Control'] = 'public, max-age=86400' # one day
  map = Magick::ImageList.new("map/base.png")
  for sheng in params
    if File.exists?("map/#{sheng}.png")
      shengmap = Magick::ImageList.new("map/#{sheng}.png")
      map = map.composite(shengmap, 0, 0, Magick::OverCompositeOp)
    end
  end
  w = params[:w].to_i()
  w = map.columns if w <= 0
  h = params[:h].to_i()
  h = map.rows if h <= 0
  
  if w != map.columns || h != map.rows
    map = map.resize(w, h)
  end
  map.to_blob
end


