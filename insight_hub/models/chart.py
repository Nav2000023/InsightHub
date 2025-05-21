from django.db import models
from .dashboard import Dashboard  # Import Dashboard model
from .CSVfile import CSVFile, os
from  insight_hub.utils.chart_utils import chart_function_map
import pandas as pd

class Chart(models.Model):
    # Define the choices for chart type
    LINE = 'line'
    BAR = 'bar'
    PIE = 'pie'
    
    CHART_TYPE_CHOICES = [
        (LINE, 'LineChart'),
        (BAR, 'BarChart'),
        (PIE, 'PieChart'),
    ]

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, null=False, related_name="charts")  # Many-to-One with Dashboard
    # Use CharField with choices
    chart_type = models.CharField(
        max_length=10, 
        choices=CHART_TYPE_CHOICES, 
        default=LINE,  # Default value if no value is provided
        null=False  # Not nullable
    )
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    x_column = models.CharField(max_length=100, null=False, default='default_x_column')
    y_column =models.CharField(max_length=100, null=True, default=None)
    operation=models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return f"Chart: {self.title} ({self.chart_type})"
    
    def get_chart_data(self):
        try:
            csv_file = self.csv_file.file_path
        except CSVFile.DoesNotExist:
            return {"error": "No CSV file attached to this chart."}

        if not csv_file or not os.path.exists(csv_file.path):
            return {"error": "CSV file not found."}

        try:
            df = pd.read_csv(csv_file.path)
        except Exception as e:
            return {"error": f"Error reading CSV: {str(e)}"}

        chart_func = chart_function_map.get(self.chart_type)

        if not chart_func:
            return {"error": "Unsupported chart type."}
        if self.chart_type == "pie":
            return chart_func(df, self.x_column)
        return chart_func(df, self.x_column, self.y_column if hasattr(self, 'y_column') else None, self.operation)
        # Pass appropriate args
        # if self.chart_type == "PieChart":
        #     return chart_func(df, self.x_column)
        # else:
        #     return chart_func(df, self.x_column, self.y_column)
    
    def get_chart_options(self):
        try:
            csv_file = self.csv_file.file_path
        except CSVFile.DoesNotExist:
            return {"error": "No CSV file attached to this chart."}

        if not csv_file or not os.path.exists(csv_file.path):
            return {"error": "CSV file not found."}

        try:
            df = pd.read_csv(csv_file.path)
        except Exception as e:
            return {"error": f"Error reading CSV: {str(e)}"}

        all_columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(include='number').columns)

        return {
            "all": all_columns,
            "numeric": numeric_columns
        }

