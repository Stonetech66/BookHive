from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class PaystackWebhook(APIView):
    def post(self,request, *args, **kwargs):
        c=request.data
        if c['event']== 'charge.success':
            bought_ticket=c['data']['metadata']['order_id']
            price=c['data']['metadata']['price']
            # Create_PaymentRecord.delay(amount=price,order_id=bought_ticket)
            # return Response({'message':'ok'},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

