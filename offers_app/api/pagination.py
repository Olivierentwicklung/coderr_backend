from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Pagination for offers."""

    page_size = 6
    page_size_query_param = "page_size"

    def get_page_size(self, request):
        """Validate page size query parameter."""
        page_size = request.query_params.get(self.page_size_query_param)

        if page_size is None:
            return self.page_size

        try:
            return int(page_size)
        except (TypeError, ValueError):
            raise ValidationError({"page_size": "A valid integer is required."})
