from mainFrame import MainFrame
from tkinter import Tk

def main():
    root = Tk()
    root.wm_title("KP-KI-KD-HIZ'ın Arduinoya Gönderilmesi")
    app = MainFrame(root)
    app.mainloop()

if __name__=="__main__":
    main()
