from enum import Enum


class ProductUnit(str, Enum):
    page = "page"
    piece = "piece"
    photo = "photo"
    order = "order"
    hour = "hour"


class OrderStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"
