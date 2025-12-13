# seed.py
from app import db, Question, AnswerOption, app


def add_q(t, opts, correct_idx):
    # hindari duplikasi berdasarkan teks pertanyaan
    existing = Question.query.filter_by(text=t).first()
    if existing:
        return
    q = Question(text=t)
    db.session.add(q)
    db.session.flush()  # dapatkan q.id
    for i, txt in enumerate(opts):
        db.session.add(
            AnswerOption(question_id=q.id, text=txt, is_correct=(i == correct_idx))
        )
    db.session.commit()


with app.app_context():
    db.create_all()

    # 1
    add_q(
        "Apa yang dimaksud dengan Computer Vision?",
        [
            "Kemampuan komputer untuk menghasilkan gambar",
            "Kemampuan komputer untuk memahami dan menginterpretasi gambar",
            "Software untuk mengedit foto",
            "Hardware untuk menampilkan gambar",
        ],
        1,
    )
    # 2
    add_q(
        "Teknik apa yang digunakan untuk mendeteksi objek dalam gambar?",
        [
            "Text Processing",
            "Object Detection",
            "Audio Analysis",
            "Database Query",
        ],
        1,
    )
    # 3
    add_q(
        "Apa fungsi dari Image Classification?",
        [
            "Menghapus gambar",
            "Mengklasifikasikan gambar ke dalam kategori tertentu",
            "Mengkompress gambar",
            "Mengenkripsi gambar",
        ],
        1,
    )
    # 4
    add_q(
        "Algoritma apa yang sering digunakan dalam Computer Vision modern?",
        [
            "Sorting Algorithm",
            "Deep Learning dan Neural Networks",
            "Binary Search",
            "Quick Sort",
        ],
        1,
    )
    # 5
    add_q(
        "Apa itu Image Segmentation?",
        [
            "Menghapus sebagian gambar",
            "Membagi gambar menjadi beberapa segmen untuk analisis",
            "Memperbesar gambar",
            "Mengubah format gambar",
        ],
        1,
    )
    # 6
    add_q(
        "Teknologi apa yang digunakan untuk Face Recognition?",
        [
            "GPS",
            "Computer Vision dan Machine Learning",
            "Bluetooth",
            "Wi-Fi",
        ],
        1,
    )
    # 7
    add_q(
        "Apa aplikasi Computer Vision dalam dunia medis?",
        [
            "Medical Imaging untuk diagnosis penyakit",
            "Menghitung gaji dokter",
            "Menyimpan data pasien",
            "Membuat jadwal dokter",
        ],
        0,
    )
    # 8
    add_q(
        "Apa itu OCR (Optical Character Recognition)?",
        [
            "Teknologi untuk membaca teks dari gambar",
            "Software editing gambar",
            "Hardware scanner",
            "Format file gambar",
        ],
        0,
    )
    # 9
    add_q(
        "Convolutional Neural Network (CNN) sering digunakan untuk apa?",
        [
            "Tidak digunakan dalam Computer Vision",
            "Image recognition dan classification",
            "Database management",
            "Network security",
        ],
        1,
    )
    # 10
    add_q(
        "Apa itu Feature Extraction dalam Computer Vision?",
        [
            "Mengidentifikasi karakteristik penting dari gambar",
            "Menghapus fitur dari gambar",
            "Mengubah warna gambar",
            "Memperkecil ukuran file",
        ],
        0,
    )
    # 11
    add_q(
        "Autonomous Vehicles menggunakan Computer Vision untuk apa?",
        [
            "Memutar musik",
            "Mendeteksi objek di jalan dan navigasi",
            "Menghitung BBM",
            "Mengatur suhu kabin",
        ],
        1,
    )
    # 12
    add_q(
        "Apa itu Edge Detection dalam Image Processing?",
        [
            "Menghapus tepi gambar",
            "Mengidentifikasi batas atau tepi objek dalam gambar",
            "Membuat bingkai gambar",
            "Mengubah resolusi gambar",
        ],
        1,
    )
    # 13
    add_q(
        "Library Python apa yang populer untuk Computer Vision?",
        [
            "Pandas",
            "OpenCV",
            "Django",
            "Flask",
        ],
        1,
    )
    # 14
    add_q(
        "Apa fungsi dari Image Preprocessing?",
        [
            "Menghapus gambar",
            "Meningkatkan kualitas gambar sebelum analisis",
            "Menyimpan gambar",
            "Mengirim gambar",
        ],
        1,
    )
    # 15
    add_q(
        "Apa itu Augmented Reality (AR)?",
        [
            "Menghapus objek dari dunia nyata",
            "Menambahkan informasi digital ke dunia nyata melalui kamera",
            "Membuat dunia virtual sepenuhnya",
            "Mengedit foto",
        ],
        1,
    )
    # 16
    add_q(
        "Apa peran Computer Vision dalam sistem keamanan?",
        [
            "Tidak ada peran",
            "Pengenalan wajah dan deteksi aktivitas mencurigakan",
            "Mengganti password",
            "Mengenkripsi data",
        ],
        1,
    )
    # 17
    add_q(
        "Apa itu Image Filtering?",
        [
            "Menghapus gambar",
            "Memodifikasi gambar untuk meningkatkan fitur tertentu",
            "Menyimpan gambar",
            "Mengirim gambar via email",
        ],
        1,
    )
    # 18
    add_q(
        "YOLO (You Only Look Once) adalah algoritma untuk apa?",
        [
            "Editing video",
            "Real-time object detection",
            "Audio processing",
            "Text generation",
        ],
        1,
    )
    # 19
    add_q(
        "Apa kegunaan Computer Vision dalam industri manufaktur?",
        [
            "Quality control dan deteksi cacat produk",
            "Menghitung gaji karyawan",
            "Membuat laporan keuangan",
            "Mengatur jadwal produksi",
        ],
        0,
    )
    # 20
    add_q(
        "Apa perbedaan antara Image Classification dan Object Detection?",
        [
            "Classification mengkategorikan gambar, Detection melokalisasi objek",
            "Tidak ada perbedaan",
            "Classification lebih lambat",
            "Detection tidak akurat",
        ],
        0,
    )

print("Seeding completed: 20 computer vision questions added if not already present.")
