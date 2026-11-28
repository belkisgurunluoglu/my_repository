import pygame as pg
from pygame.math import Vector2 #bu modülü, enemy'mizin çizgileri takip etmesini yazmayı kolaylaştırmak için importladık.
import math # bu modülü enemy'i rotatelemek için importladık. 
class Enemy(pg.sprite.Sprite): #burada enemy class'ımızı tanımlıyoruz, ayrıca enemy'lerin sprite sayılması için pygame'in sprite class'ından inheritance da aldık
    def __init__(self, enemy_type, waypoints, images): #normalde pos variable'ı bekliyordu bu class, waypoints kullanabilmek için içini güncelledik.
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0]) #waypoints'i pos variable'ımızı extractlemek için kullanıyoruz.
        #en baştaki initial position'umuzu, waypoints listesinin ilk elemanı yaptık ki hareketine çizginin başından başlasın.
        self.target_waypoint = 1 #hedef waypoint'imizin waypoints listesi içerisindeki indexi olacak bu sayı :D
        self.health = 10
        self.speed = 2 #ileride farklı enemy türleri için farklı farklı hızlar yapacağımız bir speed variable'ı ekledik.
        self.angle = 0 
        self.original_image = images.get(enemy_type) #aynı görseli tekrar tekrar rotateleyince görüntü kalitesi düşmesin diye tanımladık bunu.
        self.image = pg.transform.rotate(self.original_image , self.angle) #image'i o anki angle'a göre rotatelemiş olduk.
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 

    def move(self): #burada enemy'nin hareket etmesini sağlayan method var, x ekseninde tick başına 1 piksel ilerliyor bu sayede #ARTIK YOK DFJKGNLSKDJFNLSD
        if self.target_waypoint < len(self.waypoints): #yolum bitmedi normal devam ediyorsam
            self.target = Vector2(self.waypoints[self.target_waypoint])  
            self.movement = self.target - self.pos 
        else: #eğer yolun sonuna geldiysek
            self.kill() #sprite'ı silmeye yarayan bir method bu. yolun sonuna gelince artık oyunun kendisi error verip kapanmıyor, enemy yok oluyor sadece.
        dist = self.movement.length() #valueerror veriyordu başta, onu engelleyecek bir şeyler yaptık.
        #check if remaining distance is greater than enemy speed
        if dist >= self.speed: #bu normalde olması gereken koşulumuz. dolayısıyla normal hareketimizi bunun içine attık.
            self.pos += self.movement.normalize() * self.speed #adım büyüklüğünü speed'le çarptık ki o hızda gitsin.
        else:
            if dist != 0:
                #eğer bu if satırını eklemeseydik bu sefer de ikinci kez yolun sonuna geldiğimizde valueerror yiyecektik.
                self.pos += self.movement.normalize() * dist #eğer adımdan az kaldıysa direkt distance'ın kendisi kadar gideceği şekilde kodladık.
            self.target_waypoint += 1 #çizgi sonuna gelmiş enemy'mizin targetini diğer waypoint yapıyoruz.
        #artık enemy ekranın bir ucundan diğerine gitmeyeceği için x += 1 kısmını sildik. sorry Egemen :D 
    def update(self): #burada update diye bir method ekledim, hareket methodunu çağırmak için kullanılıyor
        self.move()
        self.rotate() #artık update'i çağırdığımızda rotate'i de çağırmış olacağız.
    def rotate(self):
        #calculate the distance, sonra bu değerleri açı hesabı için kullanıyoruz
        dist = self.target - self.pos
        #use the distance to calculate angle. TRİGONOMETRİK BİR ŞEYLER YAPACAĞIZ ŞİMDİ BURADA, GEBERMELİK.
        self.angle = math.degrees(math.atan2(-dist[1], dist[0])) #sırasıyla y ve x mesafe değerlerini verip açı hesaplattık, radyanı dereceye çevirdik
        #rotate image and update rectangle
        self.image = pg.transform.rotate(self.original_image , self.angle) #og image'imizi angle'a göre rotatelenmiş halini self.image'e eşitledik.
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 

    
        
        
        
        
   

