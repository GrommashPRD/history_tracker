from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VisitedLink
from .serializers import VisitedLinkSerializer
from urllib.parse import urlparse


class VisitedLinksView(APIView):
    def post(self, request):
        urls = request.data.get('urls')

        if isinstance(urls, str):
            urls = [urls]

        if not isinstance(urls, list):
            return Response({'error': 'Входные данные должны быть списком или строкой.'},
                            status=status.HTTP_400_BAD_REQUEST)

        for url in urls:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc:
                VisitedLink.objects.get_or_create(url=url)

        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        from_timestamp = request.query_params.get('from', None)
        to_timestamp = request.query_params.get('to', None)

        if from_timestamp is None or to_timestamp is None:
            return Response({"status": "Параметры 'from' и 'to' обязательны."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_timestamp = int(from_timestamp)
            to_timestamp = int(to_timestamp)
        except ValueError:
            return Response({"status": "Некорректные временные метки."}, status=status.HTTP_400_BAD_REQUEST)

        from_datetime = timezone.datetime.fromtimestamp(from_timestamp)
        to_datetime = timezone.datetime.fromtimestamp(to_timestamp)

        visited_links = VisitedLink.objects.filter(timestamp__range=(from_datetime, to_datetime))
        unique_domains = {urlparse(link.url).netloc for link in visited_links}

        return Response({"domains": list(unique_domains), "status": "ok"}, status=status.HTTP_200_OK)

