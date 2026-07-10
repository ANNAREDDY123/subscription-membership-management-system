def valid_phone(phone):

    return (
        phone.isdigit()
        and len(phone) == 10
    )


def valid_subscription_status(status):

    return status in [
        "Active",
        "Expired",
        "Cancelled"
    ]


def valid_dates(start_date, end_date):

    return end_date > start_date
