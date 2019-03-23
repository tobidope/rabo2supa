#! /usr/bin/env python3

import csv
import sys
from dataclasses import dataclass
from typing import Callable, Dict


def remove_whitespace(text: str) -> str:
    """
    >>> remove_whitespace("DE12 5001 0517 0648 4898 90")
    'DE12500105170648489890'
    """
    return text.replace(" ", "")


def to_supa_amount(number: str) -> str:
    """
    >>> to_supa_amount("-123.456,78")
    '123456.78'
    >>> to_supa_amount("41,04")
    '41.04'
    """
    n = number.replace(".", "").replace(",", ".")
    return "{:.2f}".format(abs(float(n)))


def create_debit_credit_indicator(number: str) -> str:
    """
    >>> create_debit_credit_indicator("-154.032,11")
    'DBIT'
    >>> create_debit_credit_indicator("41,04")
    'CRDT'
    """
    if number.startswith("-"):
        return "DBIT"
    return "CRDT"


@dataclass
class Mapping:
    source: str
    target: str
    converter: Callable[[str], str] = str


RABO_TO_SUPA_MAPPING = (
    Mapping(source="Buchungsdatum", target="BookgDt"),
    Mapping(source="Wertstellungsdatum", target="ValDt"),
    Mapping(source="Auftraggeber/Empfänger", target="RmtdNm"),
    Mapping(
        source="IBAN (Auftraggeber/Empfänger)",
        target="RmtdAcctIBAN",
        converter=remove_whitespace,
    ),
    Mapping(source="Betrag", target="Amt", converter=to_supa_amount),
    Mapping(
        source="Betrag",
        target="CdtDbtInd",
        converter=create_debit_credit_indicator,
    ),
    Mapping(source="Währung", target="AmtCcy"),
    Mapping(source="Buchungstyp", target="RmtInf"),
    Mapping(source="Transaktionsreferenz", target="Id"),
)

AIRPLUS_TO_SUPA_MAPPING = (
    Mapping(source="Buch.Datum", target="BookgDt"),
    Mapping(source="Leistungserbringer", target="RmtdNm"),
    Mapping(source="Abgerechnet", target="Amt"),
)


def map_row(row: Dict[str, str], mapping: Mapping) -> Dict[str, str]:
    """
    >>> map_row({"a": "1"}, [Mapping(source="a", target="b")])
    {'b': '1'}
    """
    supa_row = {}
    for m in mapping:
        value = row[m.source]
        supa_row[m.target] = m.converter(value)
    return supa_row


def main():
    supa_columns = [c.target for c in RABO_TO_SUPA_MAPPING]
    writer = csv.DictWriter(sys.stdout, supa_columns, dialect=csv.excel_tab)
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as rabo_file:
        writer.writeheader()
        reader = csv.DictReader(rabo_file)
        for row in reader:
            supa_row = map_row(row, RABO_TO_SUPA_MAPPING)
            writer.writerow(supa_row)


if __name__ == "__main__":
    sys.exit(main())
