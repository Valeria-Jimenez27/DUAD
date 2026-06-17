try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from sqlalchemy import select
from app.database import engine, Base, get_db
from app.models import Platform, Genre, Series, UserSeries


def seed() -> None:
    if engine is None:
        print("ERROR: DATABASE_URL no está configurado.")
        print("Copiá .env.example a .env y completá tus credenciales.")
        return

    Base.metadata.create_all(engine)

    with get_db() as db:
        if db.execute(select(Series)).first():
            print("La base de datos ya tiene datos. Saltando seed.")
            return

        # --- Plataformas ---
        netflix = Platform(name="Netflix")
        apple_tv = Platform(name="Apple TV+")
        hbo = Platform(name="HBO Max")
        hulu = Platform(name="Hulu")
        db.add_all([netflix, apple_tv, hbo, hulu])
        db.flush()

        # --- Géneros ---
        drama = Genre(name="Drama", slug="drama")
        thriller = Genre(name="Thriller", slug="thriller")
        crime = Genre(name="Crime", slug="crime")
        sci_fi = Genre(name="Sci-Fi", slug="sci-fi")
        comedy = Genre(name="Comedy", slug="comedy")
        satire = Genre(name="Satire", slug="satire")
        db.add_all([drama, thriller, crime, sci_fi, comedy, satire])
        db.flush()

        # --- Series ---
        breaking_bad = Series(
            title="Breaking Bad",
            year_start=2008,
            year_end=2013,
            total_seasons=5,
            platform=netflix,
            genres=[drama, thriller, crime],
        )
        severance = Series(
            title="Severance",
            year_start=2022,
            year_end=None,
            total_seasons=2,
            platform=apple_tv,
            genres=[thriller, sci_fi, drama],
        )
        succession = Series(
            title="Succession",
            year_start=2018,
            year_end=2023,
            total_seasons=4,
            platform=hbo,
            genres=[drama, satire, comedy],
        )
        the_bear = Series(
            title="The Bear",
            year_start=2022,
            year_end=None,
            total_seasons=3,
            platform=hulu,
            genres=[drama, comedy],
        )
        db.add_all([breaking_bad, severance, succession, the_bear])
        db.flush()

        # --- Tracking personal ---
        db.add_all([
            UserSeries(
                series_id=breaking_bad.id,
                status="completed",
                seasons_watched=5,
                episodes_watched=62,
                rating=5,
                review="Una obra maestra. El arco de Walter White es de lo mejor que ha dado la televisión.",
            ),
            UserSeries(
                series_id=severance.id,
                status="watching",
                seasons_watched=2,
                episodes_watched=19,
                rating=5,
                review="Adictiva y perturbadora. Cada episodio deja con más preguntas que respuestas.",
            ),
            UserSeries(
                series_id=succession.id,
                status="completed",
                seasons_watched=4,
                episodes_watched=39,
                rating=5,
                review="Los Roy me rompieron el corazón. La mejor escritura en la historia reciente de la TV.",
            ),
            UserSeries(
                series_id=the_bear.id,
                status="watching",
                seasons_watched=2,
                episodes_watched=18,
                rating=4,
                review="Ansiedad en forma de chef. El episodio Fishes de la T2 es obra de arte.",
            ),
        ])
        # get_db() hace commit automático al salir del with

    print("Seed completado exitosamente!")
    print("  - 4 plataformas (Netflix, Apple TV+, HBO Max, Hulu)")
    print("  - 6 géneros (Drama, Thriller, Crime, Sci-Fi, Comedy, Satire)")
    print("  - 4 series (Breaking Bad, Severance, Succession, The Bear)")
    print("  - 4 entradas de tracking")


if __name__ == "__main__":
    seed()
