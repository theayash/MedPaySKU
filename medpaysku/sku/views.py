from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, timedelta
import pandas as pd
import glob
import os

"""
Get the transaction details by transaction id
"""


class TransactionDetails(APIView):
    def get(self, request, transaction_id, format=None):

        # Read CSV file and create the data frame
        data_frame = CSVFileHandler.readfile()

        if not data_frame.empty:
            data_frame = data_frame[data_frame['transaction_id'] == transaction_id]

            # Prepare the response format
            for index, row in data_frame.iterrows():
                response = {
                    "transaction_id": row['transaction_id'],
                    "sku_name": row['sku_name'],
                    "sku_price": row["sku_price"],
                    "transaction_datetime": row['transaction_datetime']
                }
        else:
            response = {}

        return Response(response)


"""
Get transaction summary by SKU
"""


class TransactionSummaryBySKU(APIView):
    def get(self, request, number_of_days, format=None):

        # Get the date by subtracting the last n number of days
        obj = DateFinder(number_of_days, 'subtract')
        from_date = obj.date_operation()

        # Get the Data Frame from CSV files
        data_frame = CSVFileHandler.readfile()
        response_list = []

        # Check if data frame is not empty then do the validations
        if not data_frame.empty:
            data_frame['transaction_datetime'] = pd.to_datetime(
                data_frame['transaction_datetime'], format='%d/%m/%Y').dt.date
            data_frame = data_frame[data_frame['transaction_datetime'] >= from_date]

            # Prepare the Response Format
            for index, row in data_frame.iterrows():
                response_list.append({"sku_name": row["sku_name"], "total_amount": row["sku_price"]})

        return Response({"summary": response_list})


"""
Get transaction summary by SKU category
"""


class TransactionSummaryBySKUCategory(APIView):
    def get(self, request, number_of_days, format=None):

        # Get the date by subtracting the last n number of days
        obj = DateFinder(number_of_days, 'subtract')
        from_date = obj.date_operation()

        # Get the Data Frame from CSV files
        data_frame = CSVFileHandler.readfile()
        response_list = []

        # Check if data frame is not empty then do the validations
        if not data_frame.empty:
            data_frame['transaction_datetime'] = pd.to_datetime(
                data_frame['transaction_datetime'], format='%d/%m/%Y').dt.date
            data_frame = data_frame[data_frame['transaction_datetime'] >= from_date]

            # Prepare the Response Format
            for index, row in data_frame.iterrows():
                response_list.append({"sku_category": row["sku_category"], "total_amount": row["sku_price"]})

        return Response({"summary": response_list})


"""
All the pandas activity should be done here in this class
"""


class CSVFileHandler:
    def __init__(self):
        pass

    @staticmethod
    def readfile():
        # get static as well as dynamic files
        all_inputfiles = glob.glob(os.path.join(os.getcwd() + "/storage", "*.csv"))
        all_staticfiles = glob.glob(os.path.join(os.getcwd() + "/static", "*.csv"))

        if all_inputfiles:
            input_df = pd.concat(map(pd.read_csv, all_inputfiles))
        if all_staticfiles:
            output_df = pd.concat(map(pd.read_csv, all_staticfiles))

        response = pd.merge(input_df, output_df, on='sku_id')

        return response


"""
Add or subtract dates
"""


class DateFinder:
    def __init__(self, days, operation=''):
        self.days = days
        self.operation = operation

    def date_operation(self):
        if self.operation == "add":
            dt = date.today() + timedelta(self.days)
        if self.operation == "subtract":
            dt = date.today() - timedelta(self.days)

        return dt
