import pygame as pg
import math

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)
        self.range = 200 #turret'ın menzili bu da
        self.cooldown = 1500 #turret animasyonu için cooldown ekliyorum
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        self.tile_x = tile_x
        self.tile_y = tile_y
        #calculates the center coordinates
        self.x = (self.tile_x * 64) + 32
        self.y = (self.tile_y * 64) + 32

        #animasyonun büyüsü burada oluyor
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #eski image kısmını yeniledim
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        #EVET TURRET'I HAREKET ETTİRİYORUM ARTIK MUHEHEHEHE >:3
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #transparent bir daire ekleyeceğiz menzilimizi göstermek için
        self.range_image = pg.Surface((self.range * 2, self.range *2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self):
        #sprite sheet'ten frameleri çıkartan komut bloğu
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(8):
            temp_image = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_image)
        return animation_list

    def update(self, enemy_group):
        #artık sadece range'te enemy varsa ateş etsin istiyorum
        if self.target:
            self.play_animation()
        else:
            #cooldown bittiği zaman yeni hedef arasın
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        #find enemies to **seek and destroy** (arkada bu çalıyor yazmam lazımdı)
        x_dist = 0
        y_dist = 0
        #düşmanların uzaklığını bulup en yakındakine saldıracağız
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = (x_dist ** 2 + y_dist ** 2) ** 0.5
            if dist <= self.range:
                self.target = enemy
                print("enemy found")
                self.angle = math.degrees(math.atan2(-y_dist, x_dist)) #math komutlarının iğrençlik ya, ama artık her ateş ettiğinde nişan alıp ateş ediyor


    def play_animation(self):
        #updating image
        self.original_image = self.animation_list[self.frame_index]
        #son resim güncellemesinden sonra yeteri kadar zaman geçmiş mi bakıyor
        if pg.time.get_ticks() - self.update_time > 15:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index == 8: #animasyon bittiği zaman error veriyor o yüzden bu komutla tekrar başa sarıyorum
                self.frame_index = 0 #hoca sonsuz döngüde >~<
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect) #bu satır olmazsa turret yerine sadece circle çiziyor eklemek zorundayız yani
        if self.selected == True:
            surface.blit(self.range_image, self.range_rect)
            #yukarıda bahsettiğimiz circle'ı çizen method