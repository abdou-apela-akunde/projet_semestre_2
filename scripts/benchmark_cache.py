"""Mesure rapidement le gain apporte par le cache API."""

import time

from services.ameli_api import AmeliAPI


def mesurer_cache():
    """Compare le premier appel a un appel lu depuis le cache."""
    api = AmeliAPI()

    debut = time.perf_counter()
    api.get_effectifs("Allergologues", "01", 2023)
    premier = time.perf_counter() - debut

    debut = time.perf_counter()
    api.get_effectifs("Allergologues", "01", 2023)
    second = time.perf_counter() - debut

    print(f"Premier appel : {premier:.4f} s")
    print(f"Deuxieme appel : {second:.6f} s")


if __name__ == "__main__":
    mesurer_cache()
