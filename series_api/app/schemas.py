from typing import Optional


def platform_to_dict(platform) -> Optional[dict]:
    if platform is None:
        return None
    return {"id": platform.id, "name": platform.name}


def genre_to_dict(genre) -> dict:
    return {"id": genre.id, "name": genre.name, "slug": genre.slug}


def tracking_to_dict(user_series) -> Optional[dict]:
    if user_series is None:
        return None
    return {
        "status": user_series.status,
        "seasons_watched": user_series.seasons_watched,
        "episodes_watched": user_series.episodes_watched,
        "rating": user_series.rating,
        "review": user_series.review,
    }


def series_to_dict(series) -> dict:
    return {
        "id": series.id,
        "title": series.title,
        "year_start": series.year_start,
        "year_end": series.year_end,
        "total_seasons": series.total_seasons,
        "platform": platform_to_dict(series.platform),
        "genres": [genre_to_dict(g) for g in series.genres],
        "tracking": tracking_to_dict(series.user_series),
    }
