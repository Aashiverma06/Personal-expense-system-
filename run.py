import os
import socket
from app import create_app

app = create_app(os.environ.get("FLASK_ENV", "development"))

def find_available_port(preferred_port=5050):
    """Checks if preferred_port is open; finds next available port if occupied."""
    port = preferred_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
            port += 1

if __name__ == "__main__":
    preferred = int(os.environ.get("PORT", 5050))
    port = find_available_port(preferred)
    
    print("\n" + "=" * 60)
    print(" ⚡ Personal Expense Intelligence System (PEIS)")
    print(f" 🚀 Running live at: http://127.0.0.1:{port}")
    print("=" * 60 + "\n")

    app.run(host="127.0.0.1", port=port, debug=True)
