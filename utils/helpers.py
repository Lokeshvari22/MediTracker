import os
import uuid
from datetime import datetime


class Helper:

    # ==================================
    # Generate Unique Filename
    # ==================================

    @staticmethod
    def unique_filename(filename):

        extension = os.path.splitext(
            filename
        )[1]

        return (

            f"{uuid.uuid4().hex}"

            f"{extension}"

        )

    # ==================================
    # Format Currency
    # ==================================

    @staticmethod
    def currency(amount):

        amount = amount or 0

        return f"₹{amount:,.2f}"

    # ==================================
    # Format Date
    # ==================================

    @staticmethod
    def format_date(date_value):

        if not date_value:

            return ""

        if isinstance(
            date_value,
            datetime
        ):

            return date_value.strftime(
                "%d-%m-%Y"
            )

        return date_value.strftime(
            "%d-%m-%Y"
        )

    # ==================================
    # Format Date & Time
    # ==================================

    @staticmethod
    def format_datetime(date_time):

        if not date_time:

            return ""

        return date_time.strftime(
            "%d-%m-%Y %I:%M %p"
        )

    # ==================================
    # Calculate Medicine Value
    # ==================================

    @staticmethod
    def stock_value(

        quantity,

        price

    ):

        return quantity * price

    # ==================================
    # Safe Integer
    # ==================================

    @staticmethod
    def to_int(

        value,

        default=0

    ):

        try:

            return int(value)

        except (

            TypeError,

            ValueError

        ):

            return default

    # ==================================
    # Safe Float
    # ==================================

    @staticmethod
    def to_float(

        value,

        default=0.0

    ):

        try:

            return float(value)

        except (

            TypeError,

            ValueError

        ):

            return default

    # ==================================
    # Percentage
    # ==================================

    @staticmethod
    def percentage(

        value,

        total

    ):

        if total == 0:

            return 0

        return round(

            (value / total) * 100,

            2

        )

    # ==================================
    # Generate Invoice Number
    # ==================================

    @staticmethod
    def invoice_number():

        return (

            "INV-"

            + datetime.now().strftime(

                "%Y%m%d%H%M%S"

            )

        )

    # ==================================
    # Generate Purchase Number
    # ==================================

    @staticmethod
    def purchase_number():

        return (

            "PUR-"

            + datetime.now().strftime(

                "%Y%m%d%H%M%S"

            )

        )

    # ==================================
    # Truncate Text
    # ==================================

    @staticmethod
    def truncate(

        text,

        length=50

    ):

        if not text:

            return ""

        if len(text) <= length:

            return text

        return text[:length] + "..."

    # ==================================
    # File Size
    # ==================================

    @staticmethod
    def readable_size(size):

        for unit in [

            "B",

            "KB",

            "MB",

            "GB"

        ]:

            if size < 1024:

                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} TB"

    # ==================================
    # Current Timestamp
    # ==================================

    @staticmethod
    def timestamp():

        return datetime.now()

    # ==================================
    # Current Date
    # ==================================

    @staticmethod
    def today():

        return datetime.today().date()