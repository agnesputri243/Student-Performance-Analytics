# Student Performance Analytics Dashboard

Dashboard interaktif berbasis **Streamlit** untuk menganalisis performa akademik mahasiswa menggunakan dataset `student_performance_finalscore.csv`. Proyek ini dibuat untuk tugas **Visualisasi Data – Kelas B** dengan fokus pada data cleaning, EDA, statistik deskriptif, visual encoding, storytelling, dan dashboard interaktif.

---

## Identitas

**Mata Kuliah:** Visualisasi Data  
**Kelas:** B  
**Dosen Pengampu:** Supriyanto  

**Anggota Kelompok:**

| NIM | Nama |
|---|---|
| 2300018407 | Agnes Putri Alfalahi |
| 2300018437 | Alya Aulia Azzahra |
| 2300018444 | Caressa Suchi Dabrila |

---

## Tujuan Project

Project ini bertujuan untuk mengubah data mentah performa mahasiswa menjadi insight visual yang mudah dipahami. Dashboard membantu menjawab pertanyaan utama:

> Faktor apa saja yang paling berkaitan dengan nilai akhir mahasiswa, dan kelompok mahasiswa seperti apa yang berpotensi membutuhkan perhatian akademik?

---

## Struktur Folder

```text
VD/
├── Data/
│   ├── cleaned_student_performance.csv
│   └── student_performance_finalscore.csv
├── Notebooks/
│   └── Analysis.ipynb
├── References/
│   ├── Guideline/
│   │   ├── 1.PERANCANGAN.pdf
│   │   ├── 4b Project.pdf
│   │   ├── Panduan Project Tahap 2.pdf
│   │   └── VISDAT.txt
│   └── Materi/
│       ├── 1a The_Data_Prism.pdf
│       ├── 1b Designing_for_the_Mind.pdf
│       ├── 2a Advanced_Data_Science_Visualization.pdf
│       ├── 2b The_Analytic_Lens.pdf
│       ├── 3 Visual_Encoding_Blueprint.pdf
│       ├── 4a Color_as_Data.pdf
│       ├── 6a Spreadsheet_Analytics_Mastery.pdf
│       ├── 6b Mastering_Data_Dimensions.pdf
│       ├── 7a Mastering_Data_Distributions.pdf
│       └── 7b The_Data_Refinery.pdf
├── Reports/
│   ├── insight_eda_student_performance.txt
│   └── master_matrix_tipe_data.xlsx
├── Streamlit/
│   ├── app.py
│   └── requirements.txt
├── assets/
│   └── eda_charts/
│       ├── 01_distribusi_final_score.html
│       ├── 02_komposisi_performance_category.html
│       ├── 03_distribusi_numerik_utama.html
│       ├── 04_korelasi_terhadap_final_score.html
│       ├── 05_heatmap_korelasi.html
│       ├── 06_hours_studied_vs_final_score.html
│       ├── 07_exam_anxiety_vs_final_score.html
│       ├── 08_tutoring_vs_final_score.html
│       ├── 09_category_mean_final_score.html
│       ├── 10_heatmap_stress_anxiety.html
│       ├── 11_bubble_multivariate.html
│       ├── 12_risk_level_summary.html
│       ├── box_final_score_by_diet_quality.html
│       ├── box_final_score_by_family_income_level.html
│       ├── box_final_score_by_part_time_job.html
│       ├── box_final_score_by_study_method.html
│       ├── cat_distribution_diet_quality.html
│       ├── cat_distribution_family_income_level.html
│       ├── cat_distribution_gender.html
│       ├── cat_distribution_part_time_job.html
│       └── cat_distribution_study_method.html
├── environment.yml
└── README.md
```

---

## File Utama

| File | Fungsi |
|---|---|
| `Data/student_performance_finalscore.csv` | Dataset mentah |
| `Data/cleaned_student_performance.csv` | Dataset hasil cleaning |
| `Notebooks/Analysis.ipynb` | Notebook analisis end-to-end |
| `Streamlit/app.py` | Dashboard interaktif |
| `Streamlit/requirements.txt` | Dependency Python untuk Streamlit |
| `Reports/insight_eda_student_performance.txt` | Ringkasan insight hasil EDA |
| `Reports/master_matrix_tipe_data.xlsx` | Matrix tipe data dan strategi visual |
| `assets/eda_charts/` | Kumpulan chart HTML hasil EDA |
| `environment.yml` | Konfigurasi environment Conda |

---

## Workflow Analisis

```text
Data Acquisition
→ Data Understanding
→ Data Cleaning
→ Data Profiling
→ Statistik Deskriptif
→ Exploratory Data Analysis
→ Insight
→ Storytelling
→ Visual Encoding
→ Streamlit Dashboard
```

Analisis lengkap tersedia pada:

```text
Notebooks/Analysis.ipynb
```

---

## Ringkasan Dataset

Dataset berisi **8.000 data mahasiswa** dengan fitur akademik, psikologis, gaya hidup, sosial-ekonomi, dan nilai akhir.

Target utama analisis:

```text
Final_Score
```

Hasil cleaning utama:

| Komponen | Hasil |
|---|---:|
| Missing value | 0 |
| Duplicate data | 0 |
| Baris setelah cleaning | 8.000 |
| Dataset bersih | `cleaned_student_performance.csv` |

---

## Insight Utama

Beberapa temuan penting dari EDA:

1. `Hours_Studied` memiliki hubungan positif paling kuat terhadap `Final_Score`.
2. `Exam_Anxiety_Score` memiliki hubungan negatif terhadap `Final_Score`.
3. `Tutoring_Sessions_Per_Week` berkaitan positif dengan performa akademik.
4. `Stress_Level` yang tinggi berkaitan dengan nilai akhir yang lebih rendah.
5. Kombinasi jam belajar rendah, attendance rendah, stress tinggi, dan anxiety tinggi dapat menjadi indikator kelompok mahasiswa berisiko.

---

## Fitur Dashboard

Dashboard Streamlit terdiri dari beberapa bagian utama:

- **Executive Overview** – ringkasan KPI dan distribusi nilai.
- **Academic Drivers** – analisis faktor akademik seperti jam belajar, attendance, dan tutoring.
- **Psychological Risk** – analisis stress dan anxiety terhadap nilai akhir.
- **Student Segmentation** – segmentasi mahasiswa berdasarkan risiko/performa.
- **Category Comparison** – perbandingan performa berdasarkan kategori.
- **Data Quality & Methodology** – profil data, cleaning, statistik, outlier, dan master matrix.

Dashboard juga dilengkapi:

- Sidebar filter interaktif
- KPI cards
- Plotly interactive charts
- Download filtered data
- Auto-search dataset agar portable di laptop/komputer lain

---

## Visual Encoding

Dashboard menggunakan warna sebagai data, bukan dekorasi:

| Warna | Makna |
|---|---|
| Biru | Informasi utama |
| Hijau | Performa baik |
| Oranye | Peringatan |
| Merah | Risiko |

Visualisasi dipilih berdasarkan tipe data dan tujuan komunikasi, seperti histogram untuk distribusi, scatter plot untuk hubungan, bar chart untuk perbandingan, dan heatmap untuk pola kombinasi.

---

## Cara Menjalankan Project

### 1. Masuk ke folder project

```bash
cd VD
```

### 2. Buat environment Conda

```bash
conda env create -f environment.yml
```

### 3. Aktifkan environment

```bash
conda activate vd-env
```

### 4. Jalankan notebook

```bash
jupyter lab
```

Buka:

```text
Notebooks/Analysis.ipynb
```

### 5. Jalankan dashboard Streamlit

```bash
streamlit run Streamlit/app.py
```

---

## Auto-Search Dataset

Notebook dan dashboard sudah dibuat portable. Dataset akan dicari otomatis dari beberapa lokasi berikut:

```text
Data/cleaned_student_performance.csv
Data/student_performance_finalscore.csv
cleaned_student_performance.csv
student_performance_finalscore.csv
```

Rekomendasi struktur paling aman:

```text
VD/Data/cleaned_student_performance.csv
VD/Data/student_performance_finalscore.csv
```

---

## Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook
- Conda

---

## Status Project

| Komponen | Status |
|---|---|
| Notebook Analysis | Selesai |
| Data Cleaning | Selesai |
| EDA & Insight | Selesai |
| Master Matrix | Selesai |
| Streamlit Dashboard | Siap digunakan / UI refinement |
| Laporan Tahap 2 | On Progress |

---

## Kesimpulan

Project ini menunjukkan proses lengkap dari data mentah menjadi insight visual. Hasil analisis menunjukkan bahwa performa akademik mahasiswa berkaitan dengan kombinasi faktor akademik, psikologis, dan dukungan belajar. Dashboard Streamlit berfungsi sebagai media eksplorasi interaktif untuk memahami pola performa dan kelompok mahasiswa berisiko secara lebih cepat dan berbasis data.
