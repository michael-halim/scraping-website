# import re
# # a = 'Sofa minimalis, kokoh dan berkualitas, Jenna Sofa.  Sempurna untuk menikmati waktu bersama keluarga.  Dikirim knockdown, butuh perakitan sederhana. P 140 cm L 66 cm T 82 cm  Bahan  rangka kayu pinus, busa rebounded, kain.'
# a = 'Ellis 4 Drawers, solusi penyimpanan dengan empat laci.  Cocok untuk dijadikan penyimpanan di semua ruangan, kamar tidur, nursery ataupun ruang keluarga.  Dikirim jadi, hanya tinggal pasang kaki. Panjang 80 cm Kedalaman 48 cm Tinggi 92,5 cm Warna Ivory (putih gading  Bahan kayu solid, mdf, laci kayu'
# b = """
# Rak penyimpanan berbentuk high chest dengan gaya American Country.  Cocok digunakan untuk menyimpan 
# segala keperluan hunian Anda! Dibuat dengan rangka kayu mahoni, papan mdf dan finishing cat duco berkualitas.  Kualitas ekspor akan menjamin kepuasan 
# Anda.  Dikirim jadi, tanpa perakitan. Panjang 76 Kedalaman 40 Tinggi 120 
# """
# b = """
# Dengan Deluxe Pillow Top Layer dan Kain Rajutan Luar Biasa, Sapphire Dream adalah kasur terbaik untuk ketenangan sempurna. Memberikan dukungan dan kenyamanan yang cukup, Sapphire Mimpi penciptaan kembali yang menakjubkan dari tidur yang nyenyak. Tingkat kenyamanan: Medium Tinggi matras: 27 cm Produk ini adalah matras / kasur saja. Headboard dan divan tidak termasuk. Hanya untuk pelanggan di Bandung dan Jabodetabek.
# """
# Cari Dimensi P L T
# res = re.search(r'\bP(?:anjang)?\s([\d-]+)\s(cm|m|)?(?:\s)?(?:L|Kedalaman)?\s([\d-]+)\s(cm|m)?(?:\s)?T(?:inggi)?\s([\d-]+)\s(cm|m)?\b',b)
# res = re.search(r'\b(?:[dD]ibuat|[bB]ahan)[^.]+\b',b)


# Cari Material / Bahan
# res = re.search(r'\b([dD]ibuat|[bB]ahan)[^.]+\b',b)
# print(res.group(0))
# print(res.group(1))


# print(res.group(1))
# print(res.group(2))
# print(res.group(3))
# print(res.group(4))
# print(res.group(5))
# print(res.group(6))
import os
from dotenv import load_dotenv

load_dotenv()
print(os.environ.get('DEVELOPMENT_MODE'))
if os.environ.get('DEVELOPMENT_MODE') == 'True':
    print('True')
else:
    print('False')