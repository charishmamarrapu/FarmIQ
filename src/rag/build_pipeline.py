import os
import sys
sys.path.append(os.path.dirname(__file__))

from pdf_loader import load_pdfs, chunk_documents
from csv_loader import load_crop_production_csv, load_mandi_prices_csv
from vectorstore import build_vectorstore

def build_full_pipeline():
    all_chunks = []

    pdf_folders = [
        "data/pdfs/crop_guides",
        "data/pdfs/pest_disease",
        "data/pdfs/ap_telangana",
        "data/pdfs/schemes",
    ]

    for folder in pdf_folders:
        if os.path.exists(folder) and os.listdir(folder):
            docs = load_pdfs(folder)
            chunks = chunk_documents(docs)
            all_chunks.extend(chunks)
        else:
            print(f"⚠️  Skipping empty folder: {folder}")

    crop_csv = "data/csvs/data_gov_in/crop_production.csv"
    mandi_csv = "data/csvs/data_gov_in/mandi_prices.csv"

    if os.path.exists(crop_csv):
        all_chunks.extend(load_crop_production_csv(crop_csv))
    else:
        print(f"⚠️  Crop CSV not found: {crop_csv}")

    if os.path.exists(mandi_csv):
        all_chunks.extend(load_mandi_prices_csv(mandi_csv))
    else:
        print(f"⚠️  Mandi CSV not found: {mandi_csv}")

    print(f"\n📦 Total chunks to embed: {len(all_chunks)}")

    if all_chunks:
        build_vectorstore(all_chunks)
        print("\n🎉 Pipeline complete! Vector store is ready.")
    else:
        print("\n❌ No documents found. Add PDFs/CSVs to data/ folder first.")

if __name__ == "__main__":
    build_full_pipeline()