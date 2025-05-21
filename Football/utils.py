# -*- coding: utf-8 -*-

"""Utility module for Tables app."""

import chardet
import os


def csv_file_path(file_name):
    """
    Construit le chemin complet vers un fichier CSV situé dans le dossier 'Football/csv/'.

    :param file_name: Nom du fichier CSV (avec extension).
    :type file_name: str
    :return: Chemin absolu complet du fichier CSV.
    :rtype: str
    """

    return "/".join([os.getcwd(), "Football", "csv", file_name])


def detect_encoding(file_path):
    """
    Détecte l'encodage d'un fichier à partir de son contenu brut.

    :param file_path: Chemin du fichier dont on veut détecter l'encodage.
    :type file_path: str
    :return: L'encodage détecté du fichier, ou 'utf-8' si la détection échoue.
    :rtype: str
    """

    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result.get("encoding")

        if encoding is not None:
            return encoding

        # fallback encoding if detection fails
        print(f"⚠️  Encoding detection failed for {file_path}, using default 'utf-8'")
        return "utf-8"
