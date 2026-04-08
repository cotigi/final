"""Main file responsable for program init."""

from modules.frontend import orchestrator, app

def main():
    orchestrator.start_polling(app)

if __name__ == "__main__":
    main()
