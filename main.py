import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime

veritabani = sqlite3.connect('sinavlar.db')
db = veritabani.cursor()

db.execute('''
CREATE TABLE IF NOT EXISTS sinavlar (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           ders TEXT,
           tarih TEXT,
           vize INTEGER,
           final INTEGER,
           butunleme INTEGER
           )         
           ''')
veritabani.commit()

ana_pencere = tk.Tk()
ana_pencere.title("Sınav Takip Programı")
ana_pencere.geometry("1000x700")

def tarih_formatla(tarih_metni):
    for format in ("%Y-%m-%d", "%m/%d/%y"):
        try:
            return datetime.strptime(tarih_metni, format).date()
        except:
            continue
sekme_panel = ttk.Notebook(ana_pencere)
sekme_panel.pack(fill="both", expand=True)

takip_sekmesi = ttk.Frame(sekme_panel)
sekme_panel.add(takip_sekmesi, text="Sınav Takip")

takvim = Calendar(takip_sekmesi, selectmode='day', date_pattern="yyyy-mm-dd")
takvim.pack(pady=10)

form_cercevesi = ttk.LabelFrame(takip_sekmesi, text="Sınav Bilgileri")
form_cercevesi.pack(pady=10, padx=10, fill="x")

ttk.Label(form_cercevesi,text="Ders:").grid(row=1,column=0,padx=10, pady=5 )
ders_alani = ttk.Entry(form_cercevesi)
ders_alani.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(form_cercevesi, text="Vize:").grid(row=1, column=0,padx=10, pady=5)
vize_alani = ttk.Entry(form_cercevesi)
vize_alani.grid(row=1, column=1, padx=10, pady=5)
 
ttk.Label(form_cercevesi,text="Final").grid(row=1, column=0, padx=10, pady=5)
final_alani = ttk.Entry(form_cercevesi)
final_alani.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(form_cercevesi, text="Büt/Proje").grid(row=1,column=0,padx=10, pady=5)
butunleme_alani = ttk.Entry(form_cercevesi)
butunleme_alani.grid(row=3, column=1, padx=10, pady=5)

def sinavlari_goster():
    for kayit in tablo.get_children():
        tablo.delete(kayit)
    db.execute("SELECT * FROM sinavlar")
    for satir in db.fetchall():
        tablo.insert("", "end", values=satir)

def sinav_ekle():
    ders = ders_alani.get()
    tarih = takvim.get_date()
    vize = vize_alani.get() or None
    final = final_alani.get() or None
    butunleme = butunleme_alani.get() or None

    if not ders:
        messagebox.showwarning("Uyarı", "Ders alanını doldurunuz")
    db.execute("INSERT INTO sinavlar (ders, tarih, vize, final, butunleme) VALUES (?, ?, ?, ?, ?)",(ders, tarih, vize, final, butunleme))
    veritabani.commit()
    sinavlari_goster()
    sinav_takvimi_goster()

def sinav_sil():
    secili = tablo.selection()
    if secili:
        kayit_id = tablo.item(secili)['values'][0]
        db.execute("DELETE FROM sinavlar WHERE id=?",(kayit_id,))
        veritabani.commit()
        sinavlari_goster()
        sinav_takvimi_goster()
def sinav_guncelle():
    secili = tablo.selection()
    if secili:
        kayit_id = tablo.item(secili)['values'][0]
        db.execute("UPDATE sinavlar SET ders=?, tarih=?, vize=?, final=?, butunleme=? WHERE id=?", (ders_alani.get(), takvim.get_date(), vize_alani.get(), final_alani.get(), butunleme_alani.get(), kayit_id))
        veritabani.commit()
        sinavlari_goster()
        sinav_takvimi_goster()
def kayit_sec(event):
    secili = tablo.selection()
    if secili:
        kayit = tablo.item(secili)['values']
        ders_alani.delete(0, tk.END)
        ders_alani.insert(0, kayit[1])
        takvim.set_date(kayit[2])
        vize_alani.delete(0, tk.END)
        vize_alani.insert(0, kayit[3])
        final_alani.delete(0, tk.END)
        final_alani.insert(0, kayit[4])
        butunleme_alani.delete(0, tk.END)
        butunleme_alani.insert(0, kayit[5])

buton_cercevesi = ttk.Frame(takip_sekmesi)
buton_cercevesi.pack(pady=10)

ttk.Button(buton_cercevesi, text="Ekle", command=sinav_ekle).pack(side="left", padx=5)
ttk.Button(buton_cercevesi, text="Güncelle", command=sinav_guncelle).pack(side="left", padx=5)
ttk.Button(buton_cercevesi, text="Sil",command=sinav_sil).pack(side="left", padx=5)
tablo = ttk.Treeview(takip_sekmesi, columns=("ID", "Ders","Tarih", "Vize", "Final", "Bütünleme"), show="headings")
for kolon in ("ID", "Ders", "Tarih", "Vize", "Final", "Bütünleme"):
    tablo.heading(kolon, text=kolon)
    if kolon == "Ders":
        tablo.column(kolon, width=200)
    elif kolon == "ID":
        tablo.column(kolon, width=50)
    else:
        tablo.column(kolon, width=100)
tablo.pack(fill="both", expand=True)

tablo.bind("<Double-1>", lambda e: kayit_sec(e))
sinavlari_goster()

takvim_sekmesi = ttk.Frame(sekme_panel)
sekme_panel.add(takvim_sekmesi, text="Takvim")

sinav_takvimi = Calendar(takvim_sekmesi, selectormode='day', date_pattern='yyyy-mm-dd')
sinav_takvimi.pack(fill="both", expand=True, pady=10)

def sinav_takvimi_goster():
    sinav_takvimi.calevent_remove('all')
    db.execute("SELECT tarih, ders FROM sinavlar")
    for tarih, ders in db.fetchall():
        tarih_obj = tarih_formatla(tarih)
        sinav_takvimi.calevent_create(tarih_obj, ders, 'sinav')
    sinav_takvimi.tag_config('sinav', background='red', foreground='white')
sinav_takvimi.bind("<<CalendarSelected>>", lambda e:messagebox.showinfo("Sinavlar","\n".join(d[0] for d in db.execute("SELECT ders FROM sinavlar WHERE tarih=?", (sinav_takvimi.get_date(),)))))
sinavlari_goster()
sinav_takvimi_goster()

ana_pencere.mainloop()