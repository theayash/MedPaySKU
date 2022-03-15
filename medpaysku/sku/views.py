from rest_framework.views import APIView
from rest_framework.response import Response

"""
Get the transaction details by transaction id
"""


class TransactionDetails(APIView):
    def get(self, request, transaction_id, format=None):
        return Response(transaction_id)


"""
Get transaction summary by SKU
"""


class TransactionSummaryBySKU(APIView):
    def get(self, request, number_of_days, format=None):
        return Response(number_of_days)


"""
Get transaction summary by SKU category
"""


class TransactionSummaryBySKUCategory(APIView):
    def get(self, request, number_of_days, format=None):
        return Response(number_of_days)

