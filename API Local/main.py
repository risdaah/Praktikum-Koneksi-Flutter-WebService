# from typing import Union # Impor tipe Union dari modul typing
# from fastapi import FastAPI # Impor kelas FastAPI dari modul fastapi

# app = FastAPI() # Membuat objek FastAPI

from typing import Union
from fastapi import FastAPI,Response,Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import sqlite3

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/") # Menetapkan `read_root()` sebagai handler respon GET untuk URL root
def read_root():
    return {"Hello": "World"} # Output respons nya

@app.get("/mahasiswa/{nim}") # Definisikan endpoint dengan URL "/mahasiswa/{nim}"
def ambil_mhs(nim:str): # Definisikan fungsi ambil_mhs dengan parameter nim
    return {"nama": "Budi Martami"} # Output objek dengan atribut "nama" yang berisi "Budi Martami"

@app.get("/mahasiswa2/") # Definisikan endpoint dengan URL "/mahasiswa2/"
def ambil_mhs2(nim:str): # Definisikan fungsi ambil_mhs dengan parameter nim
    return {"nama": "Budi Martami 2"} # Output objek dengan atribut "nama" yang berisi "Budi Martami 2"

@app.get("/daftar_mhs/")  # Definisikan endpoint dengan URL "/daftar_mhs/"
def daftar_mhs(id_prov: str, angkatan: str):  # Definisikan fungsi daftar_mhs dengan parameter id_prov dan angkatan
    return { # output dari request
        "query": " idprov: {}  ; angkatan: {} ".format(id_prov, angkatan),
        "data": [
            {"nim": "1234"},
            {"nim": "1235"}
        ]
    }
    
import sqlite3 # mengimport modul sqlite3
    
# Panggil Sekali Saja
@app.get("/init/")  # Definisikan endpoint dengan URL "/init/"
def init_db():
    try:
        DB_NAME = "upi.db"
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        
        # Membuat tabel "mahasiswa"
        create_table = """
        CREATE TABLE mahasiswa (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT NOT NULL,
            nama TEXT NOT NULL,
            id_prov TEXT NOT NULL,
            angkatan TEXT NOT NULL,
            tinggi_badan INTEGER
        )
        """
        cur.execute(create_table)
        con.commit()
        
    except:
        return {"status": "Terjadi error"}  # Output pesan status error
  
    finally:
        con.close()  # Menutup koneksi ke database

    return {"status": "OK, database dan tabel berhasil dibuat"}  # Output pesan status OK

# tambah_mhs versi 2
from typing import Optional  # Import tipe 'Optional' untuk properti opsional
from pydantic import BaseModel  # Import kelas 'BaseModel' untuk skema validasi data
from fastapi import FastAPI, Response, Request  # Import kelas FastAPI, Response, dan Request
import sqlite3  # Import modul sqlite3 untuk interaksi dengan database SQLite

class Mhs(BaseModel):
    nim: str  # Properti nim dengan tipe data string
    nama: str  # Properti nama dengan tipe data string
    id_prov: str  # Properti id_prov dengan tipe data string
    angkatan: str  # Properti angkatan dengan tipe data string
    tinggi_badan: Optional[int] = None  # Properti tinggi_badan dengan tipe data opsional integer, nilai defaultnya adalah None


app = FastAPI()  # Inisialisasi objek FastAPI

from fastapi import HTTPException

@app.post("/tambah_mhs/", response_model=Mhs, status_code=201)
def tambah_mhs(m: Mhs, response: Response, request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=201)
    
    try:
        # Proses tambah mahasiswa
        DB_NAME = "upi.db"  # Nama database SQLite
        con = sqlite3.connect(DB_NAME)  # Membuat koneksi ke database
        cur = con.cursor()  # Membuat objek cursor untuk menjalankan perintah SQL

        # hanya untuk test, rawal sql injection, gunakan spt SQLAlchemy
        cur.execute(
            """INSERT INTO mahasiswa (nim,nama,id_prov,angkatan,tinggi_badan) VALUES ("{}","{}","{}","{}",{})""".format(
                m.nim, m.nama, m.id_prov, m.angkatan, m.tinggi_badan
            )
        )

        con.commit()  # Melakukan commit perubahan ke database
    except Exception as e:
        # print("Error:", str(e))
        # return {"status": "Terjadi error"}
        
        raise HTTPException(status_code=500, detail="Terjadi error: {}".format(str(e)))
    finally:
        con.close()  # Menutup koneksi ke database

    response.headers["Location"] = "/mahasiswa/{}".format(m.nim)  # Mengatur header 'Location' pada respons
    print(m.nim)  # Menampilkan nim mahasiswa ke konsol
    print(m.nama)  # Menampilkan nama mahasiswa ke konsol
    print(m.angkatan)  # Menampilkan angkatan mahasiswa ke konsol

    return m  # Mengembalikan objek m sebagai respons
        


# tambah_mhs versi 3
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Response, Request
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

class Mhs(BaseModel):
    nim: str
    nama: str
    id_prov: str
    angkatan: str
    tinggi_badan: Optional[int] = None

app = FastAPI()

# Menambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import HTTPException

@app.post("/tambah_mhs/", response_model=Mhs, status_code=201)
def tambah_mhs(m: Mhs, response: Response, request: Request):
    try:
        DB_NAME = "upi.db"
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()

        cur.execute(
            """INSERT INTO mahasiswa (nim,nama,id_prov,angkatan,tinggi_badan) VALUES ("{}","{}","{}","{}",{})""".format(
                m.nim, m.nama, m.id_prov, m.angkatan, m.tinggi_badan
            )
        )

        con.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Terjadi error: {}".format(str(e)))
    finally:
        con.close()

    response.headers["Location"] = "/mahasiswa/{}".format(m.nim)
    print(m.nim)
    print(m.nama)
    print(m.angkatan)

    return m



# panggil semua data mahasiswa
@app.get("/tampilkan_semua_mhs/")
def tampil_semua_mhs():
    try:
        DB_NAME = "upi.db"  # Nama database SQLite
        con = sqlite3.connect(DB_NAME)  # Membuat koneksi ke database
        cur = con.cursor()  # Membuat objek cursor untuk menjalankan perintah SQL
        recs = []
        for row in cur.execute("SELECT * FROM mahasiswa"):  # Menjalankan query untuk mengambil semua data mahasiswa
            recs.append(row)  # Menambahkan setiap baris hasil query ke dalam daftar 'recs'
    except Exception as e:  # Menangkap dan menangani kesalahan
        print("Error:", str(e))
        return {"status": "Terjadi error"}
    finally:
        con.close()  # Menutup koneksi ke database

    return {"data": recs}  # Mengembalikan data mahasiswa dalam bentuk respons

#FASTAPI PUT
from fastapi import FastAPI, Response, Request, HTTPException
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

# Menambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.put("/update_mhs_put/{nim}", response_model=Mhs)
def update_mhs_put(response: Response, nim: str, m: Mhs):
    # Definisikan route dan handler untuk metode PUT pada endpoint /update_mhs_put/{nim}
    # Endpoint ini digunakan untuk memperbarui data mahasiswa berdasarkan nim
    
    try:
        DB_NAME = "upi.db"
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim,))  # Melakukan query SELECT untuk mendapatkan data mahasiswa dengan nim yang sesuai
        existing_item = cur.fetchone()  # Mengambil hasil query sebagai tuple
    except Exception as e:
        raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e)))  # outpu jika terjadi kesalahan saat terhubung ke database
    
    if existing_item:  # Jika data mahasiswa dengan nim yang diberikan ditemukan
        cur.execute("UPDATE mahasiswa SET nama = ?, id_prov = ?, angkatan = ?, tinggi_badan = ? WHERE nim = ?", (m.nama, m.id_prov, m.angkatan, m.tinggi_badan, nim))  
        # Melakukan query UPDATE untuk memperbarui data mahasiswa
        con.commit()  # Melakukan commit untuk menyimpan perubahan ke database
        response.headers["location"] = "/mahasiswa/{}".format(m.nim)  # Mengatur header respons HTTP "location" untuk menunjukkan lokasi yang diperbarui
    else:  # Jika data mahasiswa dengan nim yang diberikan tidak ditemukan
        raise HTTPException(status_code=404, detail="Item Not Found")  # Output jika HTTP 404 - Item not found
    
    con.close()  # Menutup koneksi ke database
    return m  # Mengembalikan objek m sebagai respons dari handler


# FASTAPI PATCH
# khusus untuk patch, jadi boleh tidak ada
# menggunakan "kosong" dan -9999 supaya bisa membedakan apakah tidak diupdate ("kosong") atau ingin diupdate dengan None atau 0
from fastapi.middleware.cors import CORSMiddleware

class MhsPatch(BaseModel):
    nama: str | None = "kosong"  # Inisialisasi atribut 'nama' dengan nilai default "kosong"
    id_prov: str | None = "kosong"  # Inisialisasi atribut 'id_prov' dengan nilai default "kosong"
    angkatan: str | None = "kosong"  # Inisialisasi atribut 'angkatan' dengan nilai default "kosong"
    tinggi_badan: Optional[int] | None = -9999  # Inisialisasi atribut 'tinggi_badan' dengan nilai default -9999
    
# Menambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.patch("/update_mhs_patch/{nim}", response_model=MhsPatch)
def update_mhs_patch(response: Response, nim: str, m: MhsPatch):
    try:
        print(str(m))  # Mencetak objek 'm' ke dalam string untuk keperluan debugging
        DB_NAME = "upi.db"
        con = sqlite3.connect(DB_NAME)  # Membuka koneksi ke database
        cur = con.cursor()  # Membuat objek cursor untuk mengeksekusi perintah SQL
        cur.execute("select * from mahasiswa where nim = ?", (nim,))  # Melakukan query untuk mengambil data mahasiswa berdasarkan nim
        existing_item = cur.fetchone()  # Mengambil hasil query sebagai tuple dan menyimpannya dalam variabel 'existing_item'
    except Exception as e:
        raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e)))  
        # Melemparkan exception dengan status code 500 jika terjadi kesalahan dalam koneksi ke database
            
    if existing_item:  # Jika data mahasiswa ditemukan
        sqlstr = "update mahasiswa set "  # String SQL untuk melakukan update data

        # Memeriksa dan membangun perintah update untuk setiap atribut dalam objek 'm'
        if m.nama != "kosong":  # Jika nilai atribut 'nama' bukan "kosong"
            if m.nama != None:  # Jika nilai atribut 'nama' bukan None
                sqlstr = sqlstr + " nama = '{}' ,".format(m.nama)  # Menambahkan frasa update untuk atribut 'nama' dengan nilai yang sesuai
            else:
                sqlstr = sqlstr + " nama = null ,"  # Menambahkan frasa update untuk atribut 'nama' dengan nilai null jika nilai atribut 'nama' adalah None
        
        if m.angkatan != "kosong":  # Memeriksa nilai atribut 'angkatan' dengan logika yang serupa
            if m.angkatan != None:
                sqlstr = sqlstr + " angkatan = '{}' ,".format(m.angkatan)
            else:
                sqlstr = sqlstr + " angkatan = null ,"
        
        if m.id_prov != "kosong":  # Memeriksa nilai atribut 'id_prov' dengan logika yang serupa
            if m.id_prov != None:
                sqlstr = sqlstr + " id_prov = '{}' ,".format(m.id_prov)
            else:
                sqlstr = sqlstr + " id_prov = null, "
        
        if m.tinggi_badan != -9999:  # Memeriksa nilai atribut 'tinggi_badan' dengan logika yang serupa
            if m.tinggi_badan != None:
                sqlstr = sqlstr + " tinggi_badan = {} ,".format(m.tinggi_badan)
            else:
                sqlstr = sqlstr + " tinggi_badan = null ,"
        # Menghapus koma terakhir dari 'sqlstr' dan menambahkan WHERE untuk menentukan baris yang akan di-update berdasarkan nim
        sqlstr = sqlstr[:-1] + " where nim='{}' ".format(nim)  
        print(sqlstr)  # Mencetak perintah SQL yang akan dieksekusi untuk keperluan debugging
        
        try:
            cur.execute(sqlstr)  # Menjalankan perintah SQL untuk melakukan update pada database
            con.commit()  # Melakukan commit perubahan pada database
            # Mengatur header 'location' dalam respons untuk mengarahkan ke URL mahasiswa yang telah di-update
            response.headers["location"] = "/mahasiswa/{}".format(nim)  
        except Exception as e:
            raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e)))  
            # Melemparkan exception dengan status code 500 jika terTerjadi exception saat mencoba menghubungkan ke database.")
    
    else:  # Jika data mahasiswa tidak ditemukan
        raise HTTPException(status_code=404, detail="Data mahasiswa dengan nim {} tidak ditemukan.".format(nim))  
        # Melemparkan exception dengan status code 404 jika data mahasiswa tidak ditemukan

    return m  # Mengembalikan objek 'm' sebagai respons dari endpoint



#FASTAPI DELETE
@app.delete("/delete_mhs/{nim}")
def delete_mhs(nim: str):
    try:
        DB_NAME = "upi.db"
        con = sqlite3.connect(DB_NAME)  # Membuka koneksi ke database
        cur = con.cursor()  # Membuat objek cursor untuk mengeksekusi perintah SQL
        sqlstr = "delete from mahasiswa where nim='{}'".format(nim)  # String SQL untuk menghapus data mahasiswa berdasarkan nim
        print(sqlstr)  # Mencetak perintah SQL yang akan dieksekusi untuk keperluan debugging
        cur.execute(sqlstr)  # Menjalankan perintah SQL untuk menghapus data dari database
        con.commit()  # Melakukan commit perubahan pada database
    except:
        return {"status": "terjadi error"}  # Mengembalikan respons dengan status error jika terjadi kesalahan dalam proses penghapusan data
    finally:
        con.close()  # Menutup koneksi ke database pada blok finally untuk memastikan koneksi ditutup walaupun terjadi exception

    return {"status": "ok"}  # Mengembalikan respons dengan status ok jika penghapusan data berhasil


# POST and GET file IMAGE
from fastapi import File, UploadFile
from fastapi.responses import FileResponse

# Upload image
@app.post("/uploadimage")
def upload(file: UploadFile = File(...)):
    try:
        print("Mulai upload")
        print(file.filename)  # Menampilkan nama file yang diupload untuk keperluan debugging
        contents = file.file.read()  # Membaca konten file yang diupload
        with open("./data_file/" + file.filename, 'wb') as f:
            f.write(contents)  # Menyimpan konten file ke dalam direktori "./data_file/"
    except Exception:
        return {"message": "Error upload file"}  
        # Mengembalikan respons dengan pesan error jika terjadi kesalahan dalam proses upload file
    finally:
        file.file.close()  # Menutup file yang diupload pada blok finally untuk memastikan file ditutup walaupun terjadi exception

    return {"message": "Upload berhasil: {}".format(file.filename)}  
    # Mengembalikan respons dengan pesan sukses dan nama file yang diupload

# Ambil image berdasarkan nama file
@app.get("/getimage/{nama_file}")
async def getImage(nama_file: str):
    return FileResponse("./data_file/" + nama_file)  
    # Mengembalikan file response dengan mengambil file dari direktori "./data_file/" berdasarkan nama file