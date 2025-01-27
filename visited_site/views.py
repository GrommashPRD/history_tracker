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
            if parsed_url.scheme and parsed_url.netloc:  # Проверяем, что URL валиден
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











# class VisitedLinks(ModelViewSet):
#     queryset = Visited.objects.all()
#     serializer_class = VisitLink
#
#     def post(self, request, *args, **kwargs):
#         url = request.data.get['url', []]
#
#         if isinstance(url, list):
#             for link in url:
#                 Visited.objects.create(url=link)
#
#         return Response({"status": "OK"}, status=status.HTTP_201_CREATED)
#


# class VisitedLinks(ModelViewSet):
#     queryset = Visited.objects.all()
#     serializer_class = VisitLink
#
#     def create(self, request, *args, **kwargs):
#         worker_id = request.data.get('worker_id')
#         url = request.data.get('url', [])
#
#         if isinstance(url, list):
#             for link in url:
#                 Visited.objects.get_or_create(worker_id=worker_id, url=link)
#
#         if not worker_id or not url:
#             return Response({'error': 'ID сотрудника не найден'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             worker = Worker.objects.get(id=worker_id)
#             visited_link = Visited.objects.create(worker=worker, url=url)
#             serializer = self.get_serializer(visited_link)
#             return Response({"status": "OK"}, status=status.HTTP_201_CREATED)
#
#         except Worker.DoesNotExist:
#             return Response({'error': 'Сотрудник не найден.'}, status=status.HTTP_404_NOT_FOUND)


    # def get(self, request):
    #     all_links = Visited.objects.all()
    #     serializer = self.get_serializer(all_links, many=True)
    #
    #     unique_urls = list(set(link['url'] for link in serializer.data))
    #
    #     return Response({"links": unique_urls, "status": "OK"}, status=status.HTTP_200_OK)





# class VisitedLinks(ModelViewSet):
#     queryset = Visited.objects.all()
#     serializer_class = VisitLink
#
#     def create(self, request, *args, **kwargs):
#         worker_id = request.data.get('worker_id')
#         url = request.data.get('url', [])
#
#         if not worker_id or not url:
#             return Response({'error': 'ID сотрудника не найден'}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             worker = Worker.objects.get(id=worker_id)
#             visited_link = Visited.objects.create(worker=worker, url=url)
#             serializer = self.get_serializer(visited_link)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         except Worker.DoesNotExist:
#             return Response({'error': 'Сотрудник не найден.'}, status=status.HTTP_404_NOT_FOUND)


# class WorkerViewSet(ModelViewSet):
#     queryset = Worker.objects.all()
#     serializer_class = WorkerDomains
