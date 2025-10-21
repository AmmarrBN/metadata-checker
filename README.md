# Metadata Checker Tool

Metadata Checker adalah aplikasi web berbasis Flask yang memungkinkan Anda untuk mengekstrak, menganalisis, mengedit, dan mengelola metadata dari berbagai jenis file dengan mudah dan cepat.

---

## Daftar Isi

- [Apa itu Metadata Checker?](#apa-itu-metadata-checker)
- [Kegunaan & Use Case](#kegunaan--use-case)
- [Fitur Utama](#fitur-utama)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Tools yang Didukung](#tools-yang-didukung)
- [Troubleshooting](#troubleshooting)
- [API Endpoints](#api-endpoints)
- [Keamanan](#keamanan)
- [Logging](#logging)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

---

## Apa itu Metadata Checker?

Metadata adalah informasi tentang data. Setiap file digital (gambar, video, audio, dokumen, dll) menyimpan metadata yang berisi informasi seperti:

- **Untuk Gambar**: Kamera yang digunakan, tanggal pengambilan, lokasi GPS, ISO, aperture, focal length, dll
- **Untuk Video**: Durasi, codec, bitrate, frame rate, resolusi, audio track, dll
- **Untuk Audio**: Judul lagu, artis, album, durasi, bitrate, sample rate, dll
- **Untuk Dokumen**: Penulis, tanggal pembuatan, aplikasi pembuat, dll

**Metadata Checker** adalah tool yang memudahkan Anda untuk:
1. Melihat semua metadata dari file
2. Menganalisis informasi teknis file
3. Mengedit atau menambah metadata
4. Menghapus metadata sensitif
5. Mengekspor metadata dalam format terstruktur

---

## Kegunaan & Use Case

### 1. Fotografi & Editing Gambar
- Melihat EXIF data dari kamera (ISO, aperture, shutter speed)
- Melihat lokasi GPS pengambilan foto
- Mengedit informasi copyright dan photographer
- Menghapus metadata sensitif sebelum sharing

### 2. Video Production & Streaming
- Menganalisis codec dan bitrate video
- Melihat informasi audio track
- Memverifikasi resolusi dan frame rate
- Menambah metadata judul dan deskripsi

### 3. Audit Keamanan & Forensik Digital
- Mengidentifikasi informasi tersembunyi dalam file
- Mendeteksi metadata yang mencurigakan
- Analisis string dalam binary files
- Verifikasi integritas file

### 4. Content Management & Publishing
- Mengelola metadata untuk SEO
- Menambah informasi penulis dan tanggal publikasi
- Mengorganisir file berdasarkan metadata
- Batch processing metadata

### 5. Compliance & Privacy
- Menghapus metadata pribadi sebelum sharing
- Memastikan file tidak mengandung informasi sensitif
- Audit trail untuk file yang diproses
- Dokumentasi metadata untuk compliance

### 6. Development & Testing
- Verifikasi file uploads
- Testing metadata extraction
- Debugging file format issues
- Integration testing dengan berbagai file types

---

## Fitur Utama

### Ekstraksi Metadata
- Menggunakan 7 tools profesional (ExifTool, MediaInfo, FFprobe, ImageMagick, File, Zipinfo, Strings)
- Mendukung 100+ format file
- Output dalam format JSON yang terstruktur
- Pengelompokan metadata berdasarkan kategori

### Editing Metadata
- Tambah field metadata baru
- Edit field yang sudah ada
- Pilihan field predefined (Common, Image, Video, Audio, Custom)
- Simpan perubahan langsung ke file

### File Management
- Upload file dengan drag & drop
- Download file dengan metadata yang diperbarui
- Hapus file dari server
- Support file hingga 100MB

### Web Interface
- Interface yang user-friendly dan responsif
- Real-time metadata display
- Search functionality untuk menemukan field spesifik
- Status indicator untuk setiap tool

### Logging & Monitoring
- Comprehensive logging dengan timestamp
- Track semua operasi yang dilakukan
- Performance monitoring
- Error tracking dan debugging

---

## Persyaratan Sistem

### Minimum Requirements
- Python 3.7+
- 2GB RAM
- 500MB disk space
- Internet connection (untuk download dependencies)

### Supported OS
- Linux (Ubuntu, Debian, CentOS, dll)
- macOS (Intel & Apple Silicon)
- Windows (dengan WSL atau native)
- Termux (Android)

### External Tools (akan diinstall otomatis)
- ExifTool
- MediaInfo
- FFmpeg (untuk FFprobe)
- ImageMagick
- File command
- Zip utilities
- Binutils (untuk strings)

---

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/AmmarrBN/metadata-checker.git
cd metadata-checker
```

### 2. Installing Package & Modules

```bash
chmod +x install.sh
```
```bash
./install.sh
```

### 3. Install External Tools

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y exiftool mediainfo ffmpeg imagemagick file zip binutils
```

#### Linux (CentOS/RHEL)

```bash
sudo yum install -y exiftool mediainfo ffmpeg ImageMagick file zip binutils
```

#### macOS

```bash
brew install exiftool mediainfo ffmpeg imagemagick file-formula binutils
```

#### Windows (dengan WSL)

```bash
wsl
sudo apt-get update
sudo apt-get install -y exiftool mediainfo ffmpeg imagemagick file zip binutils
```

#### Termux (Android)

```bash
pkg update
pkg install -y exiftool mediainfo ffmpeg imagemagick file zip binutils
```

### 4. Verifikasi Instalasi

```bash
exiftool -ver
mediainfo --version
ffprobe -version
identify -version
file --version
zipinfo -v
strings --version
```

Semua command di atas harus menampilkan versi tool yang terinstall.

---

## Cara Penggunaan

### Menjalankan Aplikasi

```bash
python app.py
```

Atau dengan custom host dan port:

```bash
python app.py -r 0.0.0.0:5000
```

Atau jalankan di background:

```bash
nohup python app.py &
```

### Akses Web Interface

1. Buka browser web Anda
2. Kunjungi: `http://localhost:8080`
3. Anda akan melihat interface Metadata Checker

### Workflow Penggunaan

#### Step 1: Upload File

1. Klik area upload atau drag & drop file ke area yang disediakan
2. Pilih file yang ingin dianalisis
3. Tunggu proses ekstraksi selesai (biasanya 2-5 detik)

#### Step 2: Lihat Metadata

1. Metadata akan ditampilkan di panel kanan
2. Dikelompokkan berdasarkan tool yang digunakan
3. Gunakan search box untuk menemukan field spesifik
4. Klik pada field untuk melihat nilai lengkapnya

#### Step 3: Edit Metadata (Opsional)

1. Klik tombol "Add Field" di bagian bawah
2. Pilih tipe field dari dropdown (Common, Image, Video, Audio, Custom)
3. Masukkan nama field dan nilai yang diinginkan
4. Klik "Save" untuk menyimpan perubahan
5. File akan diperbarui dengan metadata baru

#### Step 4: Download atau Hapus

1. Klik "Download" untuk download file dengan metadata yang telah diperbarui
2. Klik "Delete" untuk menghapus file dari server
3. Klik "Upload New" untuk upload file lain

### Contoh Penggunaan Praktis

#### Contoh 1: Analisis Foto dari Kamera

```
1. Upload file JPG dari kamera digital
2. Lihat EXIF data (model kamera, lensa, ISO, shutter speed, aperture)
3. Lihat lokasi GPS jika tersedia
4. Edit field copyright dan photographer name
5. Download foto dengan metadata baru
```

#### Contoh 2: Analisis Video

```
1. Upload file MP4 atau MKV
2. Lihat durasi, codec video, bitrate, frame rate
3. Lihat informasi audio track (codec, channels, sample rate)
4. Tambah judul, deskripsi, dan tahun produksi
5. Download video dengan metadata baru
```

#### Contoh 3: Audit Keamanan File

```
1. Upload dokumen PDF atau file lainnya
2. Lihat informasi penulis dan tanggal pembuatan
3. Lihat string tersembunyi dengan strings analysis
4. Identifikasi informasi sensitif yang mungkin ada
5. Hapus metadata jika diperlukan sebelum sharing
```

#### Contoh 4: Batch Processing

```
1. Upload file pertama, lihat metadata
2. Edit metadata sesuai kebutuhan
3. Download file yang sudah diperbarui
4. Ulangi untuk file berikutnya
```

---

## Struktur Proyek

```
metadata-checker/
├── app.py                      # Main Flask application
├── install.sh                  # Installer Package & Modules
├── README.md                   # Dokumentasi ini
├── templates/
│   └── index.html             # Web interface HTML
├── static/
│   ├── style.css              # Styling dan layout
│   └── script.js              # Frontend JavaScript
└── uploads/                   # Folder untuk file yang diupload
    └── (files akan disimpan di sini)
```

### Penjelasan File:

| File | Fungsi |
|------|--------|
| `app.py` | Backend Flask, API endpoints, tool integration, metadata extraction logic |
| `templates/index.html` | Frontend HTML structure, form elements, display layout |
| `static/style.css` | Styling, responsive design, dark mode support |
| `static/script.js` | JavaScript untuk interaksi UI, file upload, AJAX calls |
| `uploads/` | Temporary storage untuk file yang diupload (auto-cleanup) |
| `install.sh` | List packages & Modules yang diperlukan |

---

## Tools yang Didukung

### 1. ExifTool

**Fungsi**: Ekstraksi metadata universal dari berbagai format file

**Tipe File**: Gambar (JPG, PNG, TIFF, GIF), Video (MP4, MKV, AVI), Audio (MP3, FLAC, WAV), PDF, dan 100+ format lainnya

**Output**: JSON format dengan semua metadata fields

**Kegunaan**: 
- Analisis metadata lengkap
- Editing metadata
- Batch processing
- Metadata removal

**Contoh Output**:
```
{
  "FileName": "photo.jpg",
  "FileSize": "2.5 MB",
  "Make": "Canon",
  "Model": "Canon EOS 5D Mark IV",
  "LensModel": "Canon EF 24-70mm f/2.8L II USM",
  "ISO": 400,
  "FNumber": 2.8,
  "ExposureTime": "1/125",
  "FocalLength": "50 mm",
  "GPSLatitude": "37.7749",
  "GPSLongitude": "-122.4194"
}
```

### 2. MediaInfo

**Fungsi**: Analisis mendalam untuk media files (video dan audio)

**Tipe File**: Video (MP4, MKV, AVI, MOV, FLV), Audio (MP3, FLAC, AAC, OGG)

**Output**: Informasi codec, bitrate, durasi, frame rate, dll

**Kegunaan**:
- Verifikasi kualitas video
- Analisis audio track
- Checking codec compatibility
- Streaming optimization

**Contoh Output**:
```
{
  "Duration": "1:23:45",
  "VideoCodec": "H.264",
  "VideoBitrate": "5000 kbps",
  "FrameRate": "29.97 fps",
  "Resolution": "1920x1080",
  "AudioCodec": "AAC",
  "AudioBitrate": "128 kbps",
  "AudioChannels": 2,
  "SampleRate": "48000 Hz"
}
```

### 3. FFprobe

**Fungsi**: Analisis audio/video dengan FFmpeg library

**Tipe File**: Video, Audio (semua format yang didukung FFmpeg)

**Output**: Stream info, format details, codec parameters

**Kegunaan**:
- Analisis mendalam audio/video
- Debugging format issues
- Stream information
- Codec verification

### 4. ImageMagick (identify)

**Fungsi**: Analisis properti gambar

**Tipe File**: JPG, PNG, GIF, BMP, TIFF, WebP, SVG, dan lainnya

**Output**: Resolusi, color space, DPI, bit depth, dll

**Kegunaan**:
- Analisis properti gambar
- Verifikasi resolusi dan DPI
- Color space checking
- Image format validation

**Contoh Output**:
```
{
  "Filename": "image.png",
  "Format": "PNG",
  "Geometry": "1920x1080",
  "Colorspace": "sRGB",
  "Depth": "8-bit",
  "DPI": "72x72",
  "Interlace": "None"
}
```

### 5. File Command

**Fungsi**: Deteksi tipe file berdasarkan magic bytes

**Tipe File**: Semua file

**Output**: MIME type dan deskripsi file

**Kegunaan**:
- Verifikasi tipe file
- Security scanning
- File validation
- MIME type detection

### 6. Zipinfo

**Fungsi**: Analisis struktur archive

**Tipe File**: ZIP, JAR, dan archive lainnya

**Output**: Daftar file dalam archive, compression info

**Kegunaan**:
- Analisis struktur archive
- File listing
- Compression ratio checking
- Archive validation

### 7. Strings

**Fungsi**: Ekstraksi string readable dari binary files

**Tipe File**: Executable, binary files, compiled code

**Output**: Readable strings yang ditemukan

**Kegunaan**:
- Analisis forensik
- Deteksi URL dan email tersembunyi
- Security analysis
- Reverse engineering

---

## Troubleshooting

### Problem: "Tool not available" error

**Penyebab**: Tool eksternal belum terinstall atau tidak ditemukan di PATH

**Solusi**:

```bash
# Verifikasi tool terinstall
which exiftool
which mediainfo
which ffprobe

# Install yang hilang
sudo apt-get install exiftool mediainfo ffmpeg imagemagick

# Atau di macOS
brew install exiftool mediainfo ffmpeg imagemagick
```

### Problem: "Permission denied" saat upload

**Penyebab**: Folder uploads tidak memiliki permission yang tepat

**Solusi**:

```bash
# Beri permission ke folder uploads
chmod 755 uploads/
chmod 755 .

# Atau jalankan dengan sudo
sudo python app.py
```

### Problem: File terlalu besar

**Penyebab**: File melebihi batas maksimal (default 100MB)

**Solusi**:

Edit file `app.py` dan ubah baris:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
```

Ubah nilai 100 sesuai kebutuhan (dalam MB).

### Problem: Server tidak bisa diakses dari device lain

**Penyebab**: Server hanya listen di localhost

**Solusi**:

```bash
# Jalankan dengan 0.0.0.0 untuk accept semua interface
python app.py -r 0.0.0.0:8080

# Akses dari device lain dengan IP server
http://192.168.1.100:8080
```

### Problem: Metadata tidak bisa disimpan

**Penyebab**: ExifTool tidak terinstall atau file read-only

**Solusi**:

```bash
# Pastikan exiftool terinstall
exiftool -ver

# Cek permission file
ls -la uploads/

# Ubah permission file
chmod 644 uploads/filename

# Jalankan dengan sudo jika perlu
sudo python app.py
```

### Problem: Aplikasi crash saat upload file besar

**Penyebab**: RAM tidak cukup atau timeout

**Solusi**:

- Tingkatkan timeout di `app.py`
- Gunakan file yang lebih kecil
- Cek RAM yang tersedia dengan `free -h` (Linux) atau `top` (macOS)
- Tutup aplikasi lain yang menggunakan banyak RAM

### Problem: "ModuleNotFoundError" saat menjalankan app

**Penyebab**: Python dependencies belum terinstall

**Solusi**:

```bash
# Install dependencies
pip install -r requirements.txt

# Atau dengan pip3
pip3 install -r requirements.txt

# Verifikasi instalasi
pip list
```

---

## API Endpoints

Aplikasi menyediakan REST API untuk integrasi dengan aplikasi lain:

### Upload File

```
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "file_id": "20240115_103045_photo.jpg",
  "filename": "photo.jpg",
  "size": 2500000
}
```

### Get Metadata

```
GET /api/metadata/<file_id>

Response:
{
  "success": true,
  "metadata": {
    "exiftool": { ... },
    "mediainfo": { ... },
    "ffprobe": { ... },
    ...
  }
}
```

### Update Metadata

```
POST /api/metadata/<file_id>
Content-Type: application/json

Body:
{
  "fields": {
    "Copyright": "2024 My Company",
    "Artist": "John Doe"
  }
}

Response:
{
  "success": true,
  "message": "Metadata updated successfully"
}
```

### Download File

```
GET /api/download/<file_id>

Response: File binary data
```

### Delete File

```
DELETE /api/delete/<file_id>

Response:
{
  "success": true,
  "message": "File deleted successfully"
}
```

### Check Tools Status

```
GET /api/tools-status

Response:
{
  "exiftool": { "installed": true, "version": "12.40" },
  "mediainfo": { "installed": true, "version": "21.09" },
  "ffprobe": { "installed": true, "version": "4.4.2" },
  ...
}
```

### Get Supported Fields

```
GET /api/supported-fields

Response:
{
  "common": ["Title", "Author", "Copyright", "Description"],
  "image": ["Make", "Model", "ISO", "FNumber", "ExposureTime"],
  "video": ["Duration", "VideoCodec", "FrameRate", "Resolution"],
  "audio": ["AudioCodec", "SampleRate", "Channels", "BitRate"],
  "custom": []
}
```

---

## Keamanan

### Best Practices

1. **Jangan upload file sensitif ke server publik**
   - Gunakan HTTPS untuk enkripsi data in-transit
   - Pertimbangkan menggunakan aplikasi secara lokal

2. **Gunakan HTTPS di production**
   - Setup SSL certificate
   - Redirect HTTP ke HTTPS
   - Gunakan secure cookies

3. **Batasi akses dengan authentication**
   - Implementasikan login system
   - Gunakan API keys untuk akses programmatic
   - Setup role-based access control

4. **Regular cleanup uploaded files**
   - Hapus file yang sudah lama
   - Implementasikan auto-cleanup
   - Monitor disk space

5. **Validate file types**
   - Whitelist file extensions yang diizinkan
   - Verify MIME types
   - Scan untuk malware

6. **Monitor disk space**
   - Setup alerts untuk disk usage
   - Implementasikan quota per user
   - Regular maintenance

### Cleanup Files Script

```bash
# Hapus file yang lebih dari 24 jam
find uploads/ -type f -mtime +1 -delete

# Atau setup cron job (jalankan setiap hari jam 00:00)
0 0 * * * find /path/to/uploads -type f -mtime +1 -delete
```

### Setup HTTPS (Production)

```bash
# Dengan Let's Encrypt dan Certbot
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com

# Update app.py untuk menggunakan SSL
python app.py --ssl-cert /etc/letsencrypt/live/yourdomain.com/fullchain.pem --ssl-key /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

---

## Logging

Aplikasi mencatat semua operasi dengan timestamp untuk debugging dan audit:

### Log Format

```
[2024-01-15 10:30:45] [SUCCESS] EXIFTOOL: Extracted 45 metadata fields - File: photo.jpg
[2024-01-15 10:30:46] [INFO] UPLOAD: Uploading file: 20240115_103045_video.mp4
[2024-01-15 10:30:50] [SUCCESS] MEDIAINFO: Media information extracted successfully
[2024-01-15 10:30:51] [ERROR] FFPROBE: Failed to extract metadata - Error: File not found
[2024-01-15 10:31:00] [WARNING] UPLOAD: File size approaching limit (95MB/100MB)
```

### Log Levels

- **SUCCESS**: Operasi berhasil dilakukan
- **INFO**: Informasi umum tentang operasi
- **WARNING**: Peringatan tentang kondisi yang perlu diperhatikan
- **ERROR**: Error yang terjadi saat operasi

### Kegunaan Logs

- **Debugging issues**: Trace error dan understand flow
- **Audit trail**: Track semua operasi yang dilakukan
- **Performance monitoring**: Identify bottlenecks
- **Security analysis**: Detect suspicious activities

### View Logs

```bash
# View real-time logs
tail -f app.log

# View last 100 lines
tail -100 app.log

# Search logs
grep "ERROR" app.log
grep "EXIFTOOL" app.log

# Count occurrences
grep -c "SUCCESS" app.log
```

---

## Kontribusi

Kontribusi sangat diterima! Silakan ikuti langkah berikut:

### 1. Fork Repository

Klik tombol "Fork" di GitHub untuk membuat copy repository di akun Anda.

### 2. Clone Repository Anda

```bash
git clone https://github.com/AmmarrBN/metadata-checker.git
cd metadata-checker
```

### 3. Buat Branch Feature

```bash
git checkout -b feature/AmazingFeature
```

### 4. Commit Changes

```bash
git add .
git commit -m 'Add AmazingFeature'
```

### 5. Push ke Branch

```bash
git push origin feature/AmazingFeature
```

### 6. Open Pull Request

Buka Pull Request di GitHub dengan deskripsi yang jelas tentang perubahan Anda.

### Contribution Guidelines

- Follow PEP 8 untuk Python code
- Tambahkan comments untuk kode yang kompleks
- Test perubahan sebelum submit
- Update dokumentasi jika diperlukan
- Gunakan meaningful commit messages

---

## Lisensi

Project ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail lengkap.

```
MIT License

Copyright (c) 2024 Metadata Checker Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Support & Contact

- **Issues**: Buka issue di GitHub untuk bug reports dan feature requests
- **Discussions**: Gunakan GitHub Discussions untuk pertanyaan umum
- **Email**: support@example.com
- **Documentation**: Lihat README.md untuk dokumentasi lengkap

---

## Terima Kasih

Terima kasih kepada:

- **ExifTool** oleh Phil Harvey - Universal metadata extraction
- **MediaInfo** oleh Jerome Martinez - Media file analysis
- **FFmpeg Project** - Audio/video processing
- **ImageMagick** - Image manipulation dan analysis
- **Flask Community** - Web framework
- **Semua contributors** yang telah membantu project ini

---

## Referensi Tambahan

- [ExifTool Documentation](https://exiftool.org/)
- [MediaInfo Documentation](https://mediaarea.net/en/MediaInfo)
- [FFprobe Documentation](https://ffmpeg.org/ffprobe.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [EXIF Standard](https://en.wikipedia.org/wiki/Exif)
- [IPTC Standard](https://en.wikipedia.org/wiki/IPTC_Information_Interchange_Model)
- [XMP Standard](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform)

---

*Dibuat dengan ❤️ untuk memudahkan analisis metadata*
*Dibuat dengan ❤️ untuk memudahkan analisis metadata*
