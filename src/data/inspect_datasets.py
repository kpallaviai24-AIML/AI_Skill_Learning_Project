
from src.data.load_datasets import load_all_datasets


def inspect_all_datasets():
    datasets = load_all_datasets()

    for group, tables in datasets.items():
        for name, df in tables.items():
            print("\n" + "=" * 65)
            print(f"DATASET: {group}/{name}")
            print("=" * 65)

            print("\nColumn names and data types:")
            print(df.dtypes.to_string())

            print("\nMissing values per column:")
            print(df.isnull().sum().to_string())

            print("\nFirst 3 rows:")
            print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    inspect_all_datasets()
