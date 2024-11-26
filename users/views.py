from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny

from users.filters import PaymentFilter
from users.models import Payment, User
from users.serialiazer import UserSerializer
from users.serializers import PaymentSerializer
from users.services import create_stripe_price, create_stripe_sessions, create_stripe_product


class PaymentViewSet(viewsets.ModelViewSet):
    """позволяет автоматически реализовать стандартные методы CRUD для модели Payment"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = create_stripe_product(payment)
        price = create_stripe_price(payment.payment_amount, product_id)
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentListView(ListCreateAPIView):
    """позволяет реализовать методы только для получения списка объектов и создания новых объектов"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
