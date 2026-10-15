import os
from app import create_app

app = create_app(os.environ.get("FLASK_ENV", "production"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    print("\n" + "=" * 60)
    print("Personal Expense Intelligence System (PEIS)")
    print(f"Running on port: {port}")
    print("=" * 60 + "\n")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

