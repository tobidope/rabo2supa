#! /usr/bin/env python3

import csv
import doctest
import sys
import os


def remove_whitespace(text):
    """
    >>> remove_whitespace("DE12 5001 0517 0648 4898 90")
    'DE12500105170648489890'
    """
    return text.replace(" ", "")


def to_supa_amount(number):
    """
    >>> to_supa_amount("-123.456,78")
    123456.78
    >>> to_supa_amount("41,04")
    41.04
    """
    n = number.replace(".", "").replace(",", ".")
    return abs(float(n))


def create_debit_credit_indicator(number):
    """
    >>> create_debit_credit_indicator("-154.032,11")
    'DBIT'
    >>> create_debit_credit_indicator("41,04")
    'CRDT'
    """
    if number.startswith("-"):
        return "DBIT"
    return "CRDT"


RABO_TO_SUPA_MAPPING = (
    {"raboName": "Buchungsdatum", "supaName": "BookgDt", "converter": str},
    {"raboName": "Wertstellungsdatum", "supaName": "ValDt", "converter": str},
    {"raboName": "Auftraggeber/Empfänger", "supaName": "RmtdNm", "converter": str},
    {
        "raboName": "IBAN (Auftraggeber/Empfänger)",
        "supaName": "RmtdAcctIBAN",
        "converter": remove_whitespace,
    },
    {"raboName": "Betrag", "supaName": "Amt", "converter": to_supa_amount},
    {
        "raboName": "Betrag",
        "supaName": "CdtDbtInd",
        "converter": create_debit_credit_indicator,
    },
    {"raboName": "Währung", "supaName": "AmtCcy", "converter": str},
    {"raboName": "Buchungstyp", "supaName": "RmtInf", "converter": str},
    {"raboName": "Transaktionsreferenz", "supaName": "Id", "converter": str},
)


def map_supa_row(row, mapping):
    """
    >>> map_supa_row({"a": "1"}, [{"raboName": "a", "supaName": "b", "converter": str}])
    {'b': '1'}
    """
    supa_row = {}
    for m in mapping:
        supa_name = m["supaName"]
        value = row[m["raboName"]]
        converter = m["converter"]
        supa_row[supa_name] = converter(value)
    return supa_row


def main():
    supa_columns = [c["supaName"] for c in RABO_TO_SUPA_MAPPING]
    writer = csv.DictWriter(sys.stdout, supa_columns, dialect=csv.excel_tab)
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as rabo_file:
        writer.writeheader()
        reader = csv.DictReader(rabo_file)
        for row in reader:
            supa_row = map_supa_row(row, RABO_TO_SUPA_MAPPING)
            writer.writerow(supa_row)


if __name__ == "__main__":
    sys.exit(main())
