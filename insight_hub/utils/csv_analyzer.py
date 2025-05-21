import pandas as pd

def analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path)

        analysis = {
            "columns": {},
            "numeric": list(df.select_dtypes(include='number').columns)
        }

        for col in df.columns:
            series = df[col]
            dtype = str(series.dtype)

            column_info = {
                "type": dtype,
                "num_unique": int(series.nunique()),
                "sample_values": series.dropna().unique()[:5].tolist()
            }

            if pd.api.types.is_numeric_dtype(series):
                column_info["min"] = float(series.min())
                column_info["max"] = float(series.max())
                column_info["mean"] = float(series.mean())

            elif pd.api.types.is_datetime64_any_dtype(series):
                column_info["min_date"] = str(series.min())
                column_info["max_date"] = str(series.max())

            elif pd.api.types.is_object_dtype(series):
                try:
                    pd.to_datetime(series)
                    column_info["type"] = "datetime"
                except Exception:
                    pass

            analysis["columns"][col] = column_info
        return analysis

    except Exception as e:
        return {"error": str(e)}