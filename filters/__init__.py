from loader import UABarbershop
from .admin_filter import AdminFilter

if __name__ == "filters":
    UABarbershop.filters_factory.bind(AdminFilter)