from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from app import create_app

# Flask necesita `app` a nivel de módulo para `flask run`
app = create_app()

if __name__ == "__main__":
    from app.database import Base, engine

    if engine is None:
        print("ERROR: DATABASE_URL no está configurado.")
        print("Copiá .env.example a .env y completá tus credenciales.")
        raise SystemExit(1)

    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(engine)
    print("Tablas creadas correctamente.")

    print("Iniciando servidor Flask...")
    app.run(debug=True, host="0.0.0.0", port=5000)
