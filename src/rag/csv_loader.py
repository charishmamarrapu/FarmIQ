from langchain_community.document_loaders import CSVLoader


def load_crop_production_csv(file_path: str):
    loader = CSVLoader(
        file_path=file_path,
        metadata_columns=["Crop"],
        encoding="utf-8"
    )
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} rows from crop production CSV")
    return docs


def load_mandi_prices_csv(file_path: str):
    loader = CSVLoader(
        file_path=file_path,
        encoding="utf-8"
    )
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} rows from mandi prices CSV")
    return docs