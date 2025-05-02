# -*- coding: utf-8 -*-

"""Utility module for Tables app."""

import chardet
import os

def csv_file_path(file_name):
    """Return complete csv file path."""

    return "/".join([os.getcwd(), "Football", "csv", file_name])


def detect_encoding(file_path):
    """Detects the encoding of a file and returns the appropriate encoding."""

    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result.get("encoding")

        if encoding is not None:
            return encoding

        # fallback encoding if detection fails
        print(f"⚠️  Encoding detection failed for {file_path}, using default 'utf-8'")
        return "utf-8"
