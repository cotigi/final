"""Main file responsable for program init."""

from modules.frontend.base import Base

def main():
    app = Base()
    app.run()


if __name__ == "__main__":
    main()
