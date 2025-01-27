import pytest
from datetime import datetime, timedelta
from rest_framework import status
from django.urls import reverse
from .models import VisitedLink  # Импорт модели VisitedLink


@pytest.mark.django_db
class TestVisitedDomainView:

    @pytest.fixture
    def setup_data(self):
        # Создание записей в базе данных
        VisitedLink.objects.create(url='https://example.com')
        VisitedLink.objects.create(url='https://testsite.com')
        VisitedLink.objects.create(url='https://anotherdomain.com')

    def test_get_visited_domains_success(self, client, setup_data):
        # Получение временных рамок
        to_date = int(datetime.now().timestamp())
        from_date = int((datetime.now() - timedelta(days=3)).timestamp())

        # GET запрос
        response = client.get(reverse('visited_domains'), {'from': from_date, 'to': to_date})

        assert response.status_code == status.HTTP_200_OK

        # Валидность доменов
        expected_domains = ['example.com', 'testsite.com', 'anotherdomain.com']
        returned_domains = [domains for domains in response.data.get('domains')]
        assert sorted(returned_domains) == sorted(expected_domains)

    def test_get_visited_domains_bad_request(self, client):
        # Запрос без параметров
        response = client.get(reverse('visited_domains'))

        # Без параметров from и to
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"status": "Параметры 'from' и 'to' обязательны."}

    def test_get_visited_domains_invalid_timestamp(self, client, setup_data):
        # Некоректное время
        response = client.get(reverse('visited_domains'), {'from': 'invalid', 'to': 'invalid'})

        # Проверка на более детальное сообщение об ошибке
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"status": "Некорректные временные метки."}