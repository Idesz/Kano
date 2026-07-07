import sys
import os
from ui.dashboard import KanoDashboard

def main():
    # Setup paths
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Initialize UI
    app = KanoDashboard()

    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting Kano...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
