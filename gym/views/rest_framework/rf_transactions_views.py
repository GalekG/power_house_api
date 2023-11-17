from rest_framework import generics, status
from rest_framework.response import Response

from gym.models import Transactions
from gym.serializers import TransactionSerializer

class TransactionsListView(generics.ListAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionsByPeopleId(generics.ListAPIView):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        people_id = self.kwargs['people_id']
        return Transactions.objects.filter(peopleId=people_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Transacción creada', 'id': transaction.id}, status=status.HTTP_201_CREATED, headers=headers)
