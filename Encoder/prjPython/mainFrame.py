#GUI için gerekli olan kütüphaneleri import ettim
from tkinter import Frame, Label, Button, Scale, StringVar
import serial
import time
import threading

#GUI arayüzü oluşturdum
class MainFrame(Frame):

    def __init__(self, master=None):
        #GUI ekranı oluşturdum
        super().__init__(master, width=420, height=270)
        self.master = master
        self.master.protocol('WM_DELETE_WINDOW', self.askQuit)
        self.pack()
        self.hilo1 = threading.Thread(target=self.getSensorValues, daemon=True)
        #seri portu başlattım
        self.arduino = serial.Serial("COM1", 9600, timeout=1.0)
        time.sleep(1)
        #kullanıcıdan alınacak değerleri aldım
        self.value_kp = StringVar()
        self.value_ki = StringVar()
        self.value_kd = StringVar()
        self.value_vel = StringVar()
        self.create_widgets()
        self.isRun = True
        self.hilo1.start()

    def askQuit(self):
        self.isRun = False
        #ekran kapatıldığında tüm değerleri 0 yaparak seri ekrana gönderdim
        self.arduino.write('KP:0'.encode('ascii'))
        self.arduino.write('KI:0'.encode('ascii'))
        self.arduino.write('KD:0'.encode('ascii'))
        time.sleep(1.1)
        self.arduino.write('VEL:0'.encode('ascii'))
        self.arduino.close()
        self.hilo1.join(0.1)
        self.master.quit()
        self.master.destroy()
        print("Kapandı")

    def getSensorValues(self):
        while self.isRun:
            cad = self.arduino.readline().decode('ascii').strip()

    def KPgonder(self):
        #kullanıcıdan alınan kp degerini seri ile gönderme işlemi
        cad = "KP:" + self.value_kp.get()
        self.arduino.write(cad.encode('ascii'))
        print(cad)

    def KIgonder(self):
        # kullanıcıdan alınan ki degerini seri ile gönderme işlemi
        cad = "KI:" + self.value_ki.get()
        self.arduino.write(cad.encode('ascii'))
        print(cad)

    def KDgonder(self):
        # kullanıcıdan alınan kd degerini seri ile gönderme işlemi
        cad = "KD:" + self.value_kd.get()
        self.arduino.write(cad.encode('ascii'))
        print(cad)

    def VELgonder(self):
        # kullanıcıdan alınan hız degerini seri ile gönderme işlemi
        cad = "VEL:" + self.value_vel.get()
        self.arduino.write(cad.encode('ascii'))
        print(cad)

    def create_widgets(self):
        #GUI için gerekli arayüz oluşturma kısmı burada gerçekleştiriliyor
        Label(self, text="KP: ").place(x=50, y=20)
        Scale(self, from_=0, to=250, orient='horizontal', tickinterval=250,
              length=220, variable=self.value_kp).place(x=90, y=0)
        Button(self, text="Gönder", command=self.KPgonder).place(x=330, y=20)

        Label(self, text="KI: ").place(x=50, y=90)
        Scale(self, from_=0, to=250, orient='horizontal', tickinterval=250,
              length=220, variable=self.value_ki).place(x=90, y=70)
        Button(self, text="Gönder", command=self.KIgonder).place(x=330, y=90)

        Label(self, text="KD: ").place(x=50, y=160)
        Scale(self, from_=0, to=250, orient='horizontal', tickinterval=250,
              length=220, variable=self.value_kd).place(x=90, y=140)
        Button(self, text="Gönder", command=self.KDgonder).place(x=330, y=160)

        Label(self, text="HIZ: ").place(x=50, y=225)
        Scale(self, from_=0, to=250, orient='horizontal', tickinterval=250,
              length=220, variable=self.value_vel).place(x=90, y=210)
        Button(self, text="Gönder", command=self.VELgonder).place(x=330, y=225)




