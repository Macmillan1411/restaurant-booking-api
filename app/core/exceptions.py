class TableNotFoundException(Exception):
    """Raised when a table is not found"""

    pass


class ReservationNotFoundException(Exception):
    """Raised when a reservation is not found"""

    pass


class DatabaseOperationException(Exception):
    """Raised when a database operation fails"""

    pass
