import pygame as pg
#şimdi artık tuşlarımızı hem tek kez tıklanabilir hem basılı tutulabilir farklı farklı tuşlar
#olarak yazmak istiyoruz. 
#ilk başta single click yapıcaz hepsini (şu anda biraz daha garip bir şey. maindeki print testini çalıştırınca sonsuza kadar çalışıyordu)
#sonra basılı tutarak tıklama özelliğini de eklicez.

#fgjfjgfhj
class Button():
  def __init__(self, x, y, image, single_click):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y) #kullandığımız x ve y verilerini buttonun sol üst köşesi olarak belirledik. bu yüzden ismini böyle koyduk
    self.clicked = False #oluşturduğumuz tıklanmış olma değişkeni, tuş oluşturulduğu andan itibaren false.
    #bu sanırım action'dan şöyle farklı, action tıklanma karşılığında harekete geçiyor olma durumu. buysa direkt tıklanıp tıklanmamanın kendisi.
    self.single_click = single_click
    #tek tıkla mı basılı tutmayla mı çalıştığına dair bir bool. butonun kendisine ait bir özellik olduğu için bunu bir argüman olarak eklemek lazım.

  def draw(self, surface):
    #şimdi tuşlarımızı tıklanabilir kılmaya geldi sıra. bunuun için tuşa tıklanma durumuna bakan bir değişken oluşturuyoruz.
    action = False
    #there are a few steps to working with buttons
    #get mouse position
    pos = pg.mouse.get_pos()
    
    #check mouseover and clicked conditions (he said that the button was a rectangle, so we could simply check for collision.)
    if self.rect.collidepoint(pos): #she was coding something :pp. bu, mouse'un buttonun üzerinde geziniyor olma durumunu kontrol ediyor.
      if pg.mouse.get_pressed()[0] == 1 and self.clicked == False : #0'ın olayı sadece sol tıklama kabul etmek. 
        #burada ayrıca tıklamanın bir kez gerçekleşip gerçekleşmediğine bakıyoruz.
        action = True #artık bu koşulumuz sağlandığında defaultta false olan değişkenimiz true oluyor.
        #if button is a single click type, then set clicked to True
        if self.single_click:
          self.clicked = True #tıklayınca clicked'i de true yapmış oluyoruz böylece. bu değişkenimiz tıklanınca olacak olayın sonsuza kadar olmamasını sağlayacak.
    #ama şimdi de birden fazla kez tıklasak da sadece bir sefer sonuç alabiliyoruz, çünkü self.clicked geri 0 olmuyor. onu düzeltelim.
    if pg.mouse.get_pressed()[0] == 0:
      self.clicked = False #artık tek tıklamalık tuşlarımız tamamen hazır!
    #draw button on screen. crazy i know
    surface.blit(self.image, self.rect) #ekrana çizdirecek metodu oluşturduk.
    return action #variable'ımızı çağırdık.

 
    
