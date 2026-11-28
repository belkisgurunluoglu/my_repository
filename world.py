import pygame as pg 
from enemy_data import ENEMY_SPAWN_DATA

class World():
  def __init__(self, data, map_image):
    self.level = 1
    self.map_tiles = []
    self.waypoints = []
    self.level_data = data
    self.image = map_image
    self.enemy_list = []
    self.spawned_enemies = 0
    

  def process_data(self):
    #datayı inceleyecek olan method
    for layer in self.level_data["layers"]:
      if layer["name"] == "Desen Katman\u0131 1": #burada tareti koyacağımız tile'ın property'lerini alıyoruz, json dosyamızda 64x64'lük alandaki her pixel'i yeşil olan tile'lar 25 değeri alıyordu, tareti onlara yapacağız
        self.map_tiles = layer["data"] #burada da o tile değerlerini kaydettik ileride check'lerde kullanmak için
      elif layer["name"] == "waypoints":
        for obj in layer["objects"]:
          waypoint_data = obj["polyline"]
          self.process_waypoints(waypoint_data)

  def process_waypoints(self, data):
    #iterate through waypoints to extract coordinates
    for point in data:
      temp_x = point.get("x")
      temp_y = point.get("y")
      self.waypoints.append((temp_x + 960 - 128, temp_y))
      
  def process_enemies(self):
    enemies = ENEMY_SPAWN_DATA[self.level - 1]
    for enemy_type in enemies:
      enemies_to_spawn = enemies[enemy_type]
      print(enemies_to_spawn)
    
  def draw(self, surface):
    surface.blit(self.image, (0,0))
