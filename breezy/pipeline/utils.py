from datetime import date


def current_year() -> dict[str, str]:
    return {
        "date_range": "customRange",
        "start_date": date.today().replace(month=1, day=1).isoformat(),
        "end_date": date.today().isoformat(),
    }
