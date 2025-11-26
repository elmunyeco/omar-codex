import argparse

from .client import ScrapClient
from .crawlers.pacientes import scrape_pacientes
from .crawlers.historias import scrape_historias


def main():
    parser = argparse.ArgumentParser(description="Scraper cardioprietohc")
    parser.add_argument("run", nargs="?")
    parser.add_argument("--target", choices=["pacientes", "historias"], required=True)
    args = parser.parse_args()

    client = ScrapClient()
    if not client.login():
        raise SystemExit("Login falló; revisá credenciales o endpoint")

    if args.target == "pacientes":
        scrape_pacientes(client)
    elif args.target == "historias":
        scrape_historias(client)

    client.close()


if __name__ == "__main__":
    main()
