import pandas as pd

def _stringify_counts(counts, x_column, chart_type):
    return {
        "labels": [str(label) for label in counts.index.tolist()],
        "data": counts.values.tolist(),
        "type": chart_type,
        "column": x_column
    }

def generate_grouped_chart(df, x_column, chart_type,y_column=None, operation="sum"):
    if y_column != "None" and y_column !="" and y_column != None:
        # Group by x_column and sum y_column
        grouped = df.groupby(x_column)[y_column]
        if operation == "avg":
            grouped = grouped.mean()
            y_column="Average "+y_column
        else:
            grouped = grouped.sum()
            y_column="Total "+y_column
        return _stringify_counts(grouped, y_column, chart_type)
    else:
        # Just count occurrences of each x_column value
        grouped = df[x_column].value_counts()
        return _stringify_counts(grouped, "Count", chart_type)
    

def generate_pie_chart(df, x_column, y_column=None):
    counts = df[x_column].value_counts()
    return _stringify_counts(counts, "Count", "pie")

chart_function_map = {
    "line": lambda df, x, y=None, op="sum": generate_grouped_chart(df, x, "line",y, op),
    "bar": lambda df, x, y=None, op="sum": generate_grouped_chart(df, x, "bar",y, op),
    "scatter": lambda df, x, y=None, op="sum": generate_grouped_chart(df, x, "scatter",y, op),
    "pie": generate_pie_chart,  # Pie doesn't need operation or y_column
}
