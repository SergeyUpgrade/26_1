from rest_framework.serializers import ModelSerializer

from users.models import Payment


class PaymentSerializer(ModelSerializer):
    """позволяет нам автоматически генерировать сериализацию и десериализацию на основе модели Payment
    также поля для сериализации"""

    class Meta:
        model = Payment
        fields = '__all__'
