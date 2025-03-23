# pagination.py
from rest_framework.pagination import PageNumberPagination

class PaginationClass(PageNumberPagination):
    page_size_query_param = 'page_size'

    def __init__(self, page_size=10, max_page_size=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = page_size
        self.max_page_size = max_page_size