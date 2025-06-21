import pandas as pd
import os
from datetime import datetime

def clean_and_merge_datasets():
    """
    Script untuk mengubah data1.tsv ke CSV dan menggabungkannya dengan data_toxic.csv
    Kolom output: comments, toxic
    - data1.tsv: CB = 1, Non_CB = 0
    - data_toxic.csv: toxic = 1, non-toxic = 0
    """
    # Path ke file data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'rawsDataset')
    clean_dataset_dir = os.path.join(script_dir, '..', 'cleanDataset')
    
    # Buat folder cleanDataset jika belum ada
    if not os.path.exists(clean_dataset_dir):
        os.makedirs(clean_dataset_dir)
        print(f"Folder {clean_dataset_dir} berhasil dibuat")
    
    data1_path = os.path.join(data_dir, 'data1.tsv')
    data_toxic_path = os.path.join(data_dir, 'data_toxic.csv')
    
    print("Membaca data1.tsv...")
    # Baca data1.tsv
    try:
        data1_df = pd.read_csv(data1_path, sep='\t')
        print(f"Data1.tsv berhasil dibaca: {len(data1_df)} baris")
        print(f"Kolom yang ada: {list(data1_df.columns)}")
        print(f"Sample data:\n{data1_df.head()}")
    except Exception as e:
        print(f"Error membaca data1.tsv: {e}")
        return
    
    print("\nMembaca data_toxic.csv...")
    # Baca data_toxic.csv
    try:
        data_toxic_df = pd.read_csv(data_toxic_path)
        print(f"Data_toxic.csv berhasil dibaca: {len(data_toxic_df)} baris")
        print(f"Kolom yang ada: {list(data_toxic_df.columns)}")
        print(f"Sample data:\n{data_toxic_df.head()}")
    except Exception as e:
        print(f"Error membaca data_toxic.csv: {e}")
        return
    
    # Proses data1.tsv
    print("\nMemproses data1.tsv...")
    # Ubah label CB menjadi 1, Non_CB menjadi 0
    data1_df['toxic'] = data1_df['label'].map({'CB': 1, 'Non_CB': 0})
    
    # Rename kolom text menjadi comments
    data1_df = data1_df.rename(columns={'text': 'comments'})
    
    # Pilih hanya kolom yang diperlukan
    data1_processed = data1_df[['comments', 'toxic']].copy()
    
    print(f"Data1.tsv setelah diproses:")
    print(f"- Total baris: {len(data1_processed)}")
    print(f"- CB (toxic=1): {len(data1_processed[data1_processed['toxic'] == 1])}")
    print(f"- Non_CB (toxic=0): {len(data1_processed[data1_processed['toxic'] == 0])}")
    
    # Proses data_toxic.csv
    print("\nMemproses data_toxic.csv...")
    # Rename kolom processed_text menjadi comments
    data_toxic_df = data_toxic_df.rename(columns={'processed_text': 'comments'})
    
    print(f"Data_toxic.csv setelah diproses:")
    print(f"- Total baris: {len(data_toxic_df)}")
    print(f"- Toxic (toxic=1): {len(data_toxic_df[data_toxic_df['toxic'] == 1])}")
    print(f"- Non-toxic (toxic=0): {len(data_toxic_df[data_toxic_df['toxic'] == 0])}")
    
    # Gabungkan kedua dataset
    print("\nMenggabungkan dataset...")
    merged_df = pd.concat([data1_processed, data_toxic_df], ignore_index=True)
    
    print(f"Dataset gabungan:")
    print(f"- Total baris: {len(merged_df)}")
    print(f"- Toxic (toxic=1): {len(merged_df[merged_df['toxic'] == 1])}")
    print(f"- Non-toxic (toxic=0): {len(merged_df[merged_df['toxic'] == 0])}")
    
    # Hapus baris yang duplikat berdasarkan kolom comments
    print("\nMenghapus duplikat...")
    initial_count = len(merged_df)
    merged_df = merged_df.drop_duplicates(subset=['comments'])
    final_count = len(merged_df)
    removed_count = initial_count - final_count
    
    print(f"Duplikat yang dihapus: {removed_count}")
    print(f"Total baris setelah hapus duplikat: {final_count}")
    
    # Generate nama file dengan timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"clean_{timestamp}.csv"
    output_path = os.path.join(clean_dataset_dir, output_filename)
    
    # Simpan ke file CSV
    print(f"\nMenyimpan ke {output_filename}...")
    try:
        merged_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"File berhasil disimpan: {output_path}")
        
        # Tampilkan sample data
        print(f"\nSample data hasil akhir:")
        print(merged_df.head(10))
        
        # Statistik akhir
        print(f"\nStatistik akhir:")
        print(f"- Total komentar: {len(merged_df)}")
        print(f"- Komentar toxic: {len(merged_df[merged_df['toxic'] == 1])}")
        print(f"- Komentar non-toxic: {len(merged_df[merged_df['toxic'] == 0])}")
        
    except Exception as e:
        print(f"Error menyimpan file: {e}")
        return
    
    print(f"\nProses selesai! File tersimpan di: {output_path}")

if __name__ == "__main__":
    clean_and_merge_datasets()
