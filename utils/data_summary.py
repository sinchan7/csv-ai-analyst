import pandas as pd

def summarize_dataframe(df: pd.DataFrame) -> dict:
    summary = {
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "summary_stats": df.describe(include="all").to_dict()
    }
    return summary
