import pygame as pg # wrote as pg so that whenever we need to call a pygame func., we can js write pg
import json
from turret import Turret
from enemies import Enemy
from world import World
from button import Button
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg.init() # we are initializing the module here

#let's create our clock
clock = pg.time.Clock() #now we put this under the main loop of our game.

#now we need to open a window, so we assign it to a variable
screen = pg.display.set_mode((300+960,960)) #butonları ekleyebilmek için oyun ekranını büyüttük. 1260 yazmaya usendim
#unless we tell the code to keep the window open, running this code will only cause a momentary pop-up of our window.
#so we create a loop in order to keep our window open.
#then we change the name of our window
pg.display.set_caption("Tower Defense")

#game mi variables
placing_turrets = False #o esnada turret konumlandırıyor olup olmadığımıza bakan variable.
selected_turret = None


#load images
map_image =   pg.image.load("levels/level_map.png").convert_alpha() 
enemy_image = pg.image.load('assets/enemies/enemy_1.png').convert_alpha() #bunun amacı enemy oluşturduğumuz zaman ekrana vereceğimiz image'ı koda tanıtmak

#şimdi farklı seviyelerdeki turretların farklı gözükmesini sağlayacağız
turret_spritesheets = []
for x in range(1,5):
    #cursor spritesheetlerini indiriyorum
    turret_sheet = pg.image.load(f"assets/turrets/turret_{x}.png").convert_alpha()
    turret_spritesheets.append(turret_sheet) #böylece farklı seviye turret spritesheetlerin olduğu bi liste yaptık

cursor_turret = pg.image.load("assets/turrets/cursor_turret.png").convert_alpha() #bu kodla turret koyacağımız zamanki cursor image'ı programa ekledik

#düğmelerin görsellerini eklerken error vermemesi için tutorialdakinden biraz daha farklı bir kod kullanıcam burada
#error düzeltmeye çalışıyorum burada
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "assets", "buttons", "buy_turret.png")
other_image_path = os.path.join(script_dir, "assets", "buttons", "cancel.png")
third_image_path = os.path.join(script_dir, "assets", "buttons", "upgrade_turret.png")
buy_turret_image = pg.image.load(image_path).convert_alpha()
cancel_image = pg.image.load(other_image_path).convert_alpha()
#ŞİMDİ DE UPGRADE İÇİN BUTON AYARLAMAM LAZIMOOOOFFFFFF
upgrade_turret_image = pg.image.load(third_image_path).convert_alpha()


#load json data for level UwU
with open("levels/level.tmj") as file:
    world_data = json.load(file)

#create world ^-^
world = World(world_data , map_image)
world.process_data()

#esasında bu fonksiyon ile oyunumuzun tile game olmasını sağlıyoruz
#Turret class'ının özelliklerini de kullanarak turret'ların istediğimiz her yere değil her 64 pixele bir koyulmasını sağlıyoruz
#önce 64'e bölüp sonra da kalanını alıp 64'le çarpınca küsuratları gidiyor bu sayede her 64 pixelde bir oluyor
def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // 64
    mouse_tile_y = mouse_pos[1] // 64
    mouse_tile_num = (mouse_tile_y * 15) + mouse_tile_x #burada böyle bir şekilde yazmamızın sebebi JSON formatı böyle koordinat kaydediyormuş
    if world.map_tiles[mouse_tile_num] == 25: #eğer kullanacağımız tile sadece çimenin olduğu bir tile'sa bir sonraki check'e geçeriz
        #burada turret koyduğumuz yer boş mu onu kontrol ediyor boşsa koyuyor
        space_is_free = True
        for turret in turret_group:
             if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                  space_is_free = False
        if space_is_free == True: #artık turret için koyduğumuz resim argümanı turret spritesheet listesinin kendisi olmalı
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y) #burada new_turret dedim çok fazla turret'lı değişken vardı çünkü
            turret_group.add(new_turret)

def select_turret(mouse_pos): #şimdi bu function ile bir turret'a tıklayınca menzilini gösteriyor artık
    mouse_tile_x = mouse_pos[0] // 64
    mouse_tile_y = mouse_pos[1] // 64
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_section(): #bununla da o turret tıklamasını geri alıyoruz
    for turret in turret_group:
        turret.selected = False

#burada group üretiyoruz enemyler ve turretler için
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#şimdi oyunumuzun içerisinde oluşturuyoruz button'ları ^v^
turret_button = Button(960+30, 120, buy_turret_image, True) #bu kısım tutorialdan birazcik farklı, direkt png
cancel_button = Button(960+50, 180, cancel_image, True) #dosyasının adını verince kodumuz nedense tanımıyor çünkü </3
upgrade_button = Button(960+30, 240, upgrade_turret_image, True) #saat sabahın ALTISI
#class'ımıza tek tıklanabilme argümanı eklemiştik. instance'larımızı da güncelledik.



#şimdi artık enemy'lerimizin oluşturduğumuz waypoint'leri takip etmelerini sağlamamız lazım.
enemy = Enemy(world.waypoints, enemy_image) #manuel olarak yazdığımız koordinatı waypoint'le değiştiriyoruz bunun için.
enemy_group.add(enemy)

print(enemy)

run = True
while run:  #as long as the run variable is true, the code will keep executing itself in a loop. brief moment --> forever
    clock.tick(60)
    #burada enemy update kısmını üste aldı ama çok da fark etmiyor imo. 
    #im from tel aviv and this is my kod düzeni
    
    #burada arkaplan rengi ekledim, bir de bu olmazsa karakter hareket ettikçe eski halleri ekranı kaplıyor >~<
    screen.fill("goldenrod4")

    #draw level
    world.draw(screen)

    #şimdiiii buttonları ekrana çizebiliriz 
    #button'larımızın draw method'larının içerisine sonunda returnlediğimiz boolean bir değişken eklediğimiz için
    #artık bu değişkenin varlığını kontrol eden if blokları içerisinde de kullanabiliyoruz draw methodlarımızı.
    #yani sanırım hem butonu ekrana çiziyor hem de kendi içerisinde butona tıklanıp tıklanmadığına bakıyor ve ona göre bir value döndürüyor artık bu method.
    #biz de bunu kullanabiliyoruz. hayat gülünce fr çok güzel
    if turret_button.draw(screen): #hallettim sorun yok.
        placing_turrets = True #artık printlemiyoruz turret yerleştirme değişkenini true yapıyoruz.
    #if placing turrets, then show cancel button as well. cancel yalnızca turret placelemeye çalışırken belirmesi gereken bir buton.
    if placing_turrets == True:
        #cursor'da turret gözüksün diye bu
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= 960:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
            placing_turrets = False #artık printlemiyoruz, değişkenimizi false yapıyoruz.
    #sondaki printler butona basma durumumuza göre programa bir şeyler yaptırma işini becerdik mi kontrol etmek için. doğru çalışırsa terminale basmalı
    #şimdi. upgrade butonu ancak bir turret seçildiyse ekrana gelmeli
    if selected_turret:
        #if selected turret can be upgraded then show the upgrade button
        if selected_turret.upgrade_level < 4:
            if upgrade_button.draw(screen): #bir input alabilmek için if bloğu koyuyoruz ig-
                selected_turret.upgrade()

    #enemy'nin takip edeceği yolu artık ekrana çizmemiz gerekmediği için sildim :pp

    #artık bütün düşmanları hareket ettirecek method ile hareketi sağlayabiliriz ^_^
    enemy_group.update()
    turret_group.update(enemy_group)
    for turret in turret_group: #yenilenmiş turret çizme komutu (bunu silmeyin range çalışmıyor NEDEN ÇALIŞMIYOR BİLMİYORUM SİLMEYİN İŞTE (╥﹏╥))
        turret.draw(screen)

    if selected_turret:
        selected_turret.selected = True
    
    #enemyleri ekrana yansıtıyoruz burada artık :3
    enemy_group.draw(screen)
    turret_group.draw(screen)
    
    # to keep the loop from being stuck in forever, we use an event handler.
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False #now, whenever we press x the window can be closed. it won't stay open forever and ever. 

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #turret koyduğumuz yer oyun ekranının içinde mi onu kontrol ediyor, içindeyse turret yerleştiriyor ^w^
            if mouse_pos[0]<960 and mouse_pos[1]<960:
                    #seçilen turret'tan çıkıyoruz
                    selected_turret = None
                    clear_section()
                    if placing_turrets == True: #bunun sayesinde artık place turret tuşuna basmadan turret yerleştiremiyoruz
                        create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)
            

    pg.display.flip() #güncellemeleri ekranda gösteriyoruz  
    
pg.quit() #bunu neden yaptığımızı anlamadım, bu satırı yazmadan önce de pencere açılıyordu ve kapat deyince kapanıyordu? :PP

#next thing we need to do is limiting the framerate, meaning it should run at 
#the same speed no matter how powerful the computer is. so we go under the first init to create a clock.
