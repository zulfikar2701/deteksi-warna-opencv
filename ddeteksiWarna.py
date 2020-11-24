import pandas as panda
import argparse
from cv2 import cv2

# membuat argumen dengan argparse di command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Lokasi Gambar")
argp = vars(ap.parse_args())
img_lok = argp['image']

# membaca gambar dengan library openCV
img = cv2.imread(img_lok)

# mencari dimensi gambar
dimensi = img.shape
panjang = img.shape[0]
lebar = img.shape[1]
luas = panjang*lebar

# mendeklarasi variabel global
clicked = False
r = g = b = xpos = ypos = 8

# membuka file csv dengan pandas & ngasih nama di setiap kolom
# membuat array untuk warna-warna
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = panda.read_csv('color.csv', names=index, header=None)

# fungsi untuk mendapatkan warna dari gambar yang tepat
def getColorName(R, G, B):
    minimum = float('inf')
    namawarna = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        #d adalah distance = jarak
        if d <=  minimum:
            minimum = d
            namawarna = csv.loc[i, "color_name"]
    return namawarna

#fungsi untuk mendapatkan koordinat x,y dari double klik dari mouse
def draw_function(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
# membuat agar window yang muncul tidak lebih dari 662000 piksel
# karena jika gambar terlalu besar maka gambar akan keluar dari layar
if lebar<=662000:
    cv2.namedWindow('image')
else:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# untuk memanggil kembali function draw_function
cv2.setMouseCallback('image', draw_function)

#loop untuk menunjukan gambar sesuai lokasi (path) menggunakan openCV
while(1):
    cv2.imshow("image", img)
    if clicked:
        recEnd = (round(lebar*.735),round(panjang*.1))
        textStart = (round(lebar*.05), round(panjang*.08))
        cv2.rectangle(img, (20,20), recEnd, (b, g, r), -1)
        #akan menampilkan jenis warna yang ditunjuk oleh mouse digambar dengan nilai RGB-nya
        text = getColorName(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        if (r+g+b>=600):
            #untuk menampilkan tulisan, jika warna piksel yang ditunjuk merupakan warna terang r+g+b >= 600 maka kita pastikan tulisan dapat dibaca
            cv2.putText(img, text, textStart, cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1, cv2.LINE_AA)
            #ukuran font akan = 1, warna yang ditampilkan akan menjadi hitam (0,0,0) dan font HERSHEY PLAIN
        else:
            cv2.putText(img, text, textStart, cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, cv2.LINE_AA)
        clicked = False

    # keluar dari loop jika user mengklik tombol ESC dan akan keluar dari program

# cv2.waitkey artinya loop akan berakhir jika tombol ESC (kode 27) di klik
    if cv2.waitKey(20) & 0xff == 27:
        break
cv2.destroyWindow()
