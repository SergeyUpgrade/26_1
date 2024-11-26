from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Courses, Lessons


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )

    city = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Ваш аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    payment_date = models.DateField(verbose_name="Дата оплаты", blank=True, null=True)
    paid_course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, verbose_name="Оплаченный курс", blank=True, null=True
    )
    separately_paid_lesson = models.ForeignKey(
        Lessons, on_delete=models.CASCADE, verbose_name="Отдельно оплаченный урок", blank=True, null=True
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
        blank=True,
        null=True,
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        blank=True,
        null=True,
    )

    session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии",
        blank=True,
        null=True,
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=50,
        verbose_name="Статус платежа",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user} - {self.payment_amount} - {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

