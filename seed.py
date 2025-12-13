# seed.py
from app import db, Question, AnswerOption, app


def add_q(t, opts, correct_idx):
    # Hindari duplikasi berdasarkan teks pertanyaan
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
        "Apa yang dimaksud dengan 'AI Bias'?",
        [
            "Kesalahan teknis dalam kode",
            "Prasangka yang tertanam dalam data dan model AI",
            "Bug dalam algoritma",
            "Masalah hardware",
        ],
        1,
    )
    # 2
    add_q(
        "Prinsip etika apa yang paling penting dalam pengembangan AI?",
        [
            "Kecepatan pemrosesan",
            "Transparansi dan akuntabilitas",
            "Ukuran model",
            "Jumlah parameter",
        ],
        1,
    )
    # 3
    add_q(
        "Bagaimana cara terbaik menangani data pribadi dalam sistem AI?",
        [
            "Menyimpan semua data",
            "Menerapkan prinsip privasi sejak desain",
            "Membagikan ke publik",
            "Mengabaikan masalah privasi",
        ],
        1,
    )
    # 4
    add_q(
        "Apa itu 'Explainable AI' (XAI)?",
        [
            "AI yang cepat",
            "AI yang bisa dijelaskan keputusannya",
            "AI yang mahal",
            "AI yang kompleks",
        ],
        1,
    )
    # 5
    add_q(
        "Mengapa keberagaman tim pengembang AI penting?",
        [
            "Tidak penting",
            "Mengurangi bias dan meningkatkan perspektif",
            "Meningkatkan profit",
            "Formalitas saja",
        ],
        1,
    )
    # 6
    add_q(
        "Apa tanggung jawab utama pengembang AI?",
        [
            "Profit maksimal",
            "Memastikan AI bermanfaat dan tidak merugikan",
            "Kecepatan development",
            "Mengikuti tren",
        ],
        1,
    )
    # 7
    add_q(
        "Bagaimana AI seharusnya memperlakukan data anak-anak?",
        [
            "Dengan perlindungan khusus",
            "Sama seperti data lain",
            "Mengabaikan",
            "Mempublikasikan",
        ],
        0,
    )
    # 8
    add_q(
        "Apa itu 'AI Fairness'?",
        [
            "Keadilan dalam hasil AI untuk semua kelompok",
            "Kecepatan AI",
            "Harga AI",
            "Ukuran model AI",
        ],
        0,
    )
    # 9
    add_q(
        "Mengapa transparansi AI penting?",
        [
            "Tidak penting",
            "Membangun kepercayaan dan akuntabilitas",
            "Meningkatkan kecepatan",
            "Mengurangi biaya",
        ],
        1,
    )
    # 10
    add_q(
        "Apa yang dimaksud dengan 'AI Safety'?",
        [
            "Memastikan AI aman dan terkendali",
            "Keamanan server",
            "Backup data",
            "Kecepatan AI",
        ],
        0,
    )
    # 11
    add_q(
        "Bagaimana menangani kesalahan prediksi AI dalam konteks medis?",
        [
            "Mengabaikan",
            "Menerapkan review manusia dan protokol keamanan",
            "Menyembunyikan",
            "Menghapus data",
        ],
        1,
    )
    # 12
    add_q(
        "Apa peran etika dalam pengembangan chatbot?",
        [
            "Tidak ada",
            "Memastikan interaksi yang aman dan bertanggung jawab",
            "Hanya estetika",
            "Formalitas",
        ],
        1,
    )
    # 13
    add_q(
        "Bagaimana menangani bias gender dalam AI?",
        [
            "Mengabaikan",
            "Mengaudit dan memperbaiki dataset",
            "Menyembunyikan",
            "Tidak penting",
        ],
        1,
    )
    # 14
    add_q(
        "Apa dampak sosial yang perlu dipertimbangkan dalam pengembangan AI?",
        [
            "Tidak ada",
            "Dampak pada pekerjaan dan kesenjangan sosial",
            "Hanya profit",
            "Kecepatan saja",
        ],
        1,
    )
    # 15
    add_q(
        "Bagaimana menyeimbangkan inovasi AI dengan etika?",
        [
            "Fokus profit saja",
            "Menerapkan framework etika dalam setiap tahap pengembangan",
            "Mengabaikan etika",
            "Fokus kecepatan",
        ],
        1,
    )
    # 16
    add_q(
        "Apa itu 'AI Governance'?",
        [
            "Tidak penting",
            "Kerangka kerja untuk mengatur pengembangan AI yang bertanggung jawab",
            "Kecepatan AI",
            "Harga AI",
        ],
        1,
    )
    # 17
    add_q(
        "Bagaimana melindungi privasi dalam sistem pengenalan wajah?",
        [
            "Mengabaikan",
            "Menerapkan consent dan enkripsi data",
            "Menyimpan semua data",
            "Membagi data",
        ],
        1,
    )
    # 18
    add_q(
        "Apa tanggung jawab AI terhadap lingkungan?",
        [
            "Tidak ada",
            "Efisiensi energi dan keberlanjutan",
            "Hanya profit",
            "Kecepatan saja",
        ],
        1,
    )
    # 19
    add_q(
        "Bagaimana menangani dilema etis dalam keputusan AI?",
        [
            "Framework etika dan review manusia",
            "Mengabaikan",
            "Otomatis saja",
            "Tidak penting",
        ],
        0,
    )
    # 20
    add_q(
        "Apa peran transparansi dalam AI medis?",
        [
            "Membangun kepercayaan dan keamanan pasien",
            "Tidak penting",
            "Formalitas saja",
            "Mengabaikan",
        ],
        0,
    )

print("Seeding completed: 20 ethical AI questions added if not already present.")
