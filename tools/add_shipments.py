#!/usr/bin/python
"""
Imports shipments into Owney's Shipment database from an Endicia
XML output file.
"""

DB_NAME = "shipments.db"
DB_ENGINE='sqlite3'

def main():
    source = sys.stdin
    tree = et.parse(source)
    for package in tree.getiterator('Package'):
        if package.find('Status').text == 'Success':
            tracking = package.find('PIC')
            if tracking is None:
                continue
            else:
                tracking = tracking.text.strip()
            print tracking
            try:
                cs_id = package.find('ReferenceID').text
            except AttributeError:
                cs_id = ''
            Shipment(cs_id=cs_id, tracking=tracking).save()

if __name__ == '__main__':
    from xml.etree import ElementTree as et
    from django.conf import settings
    import sys

    settings.configure(DATABASE_ENGINE=DB_ENGINE,DATABASE_NAME=DB_NAME)
    from owney.models import Shipment

    try:
        sys.exit(main())
    except SystemExit:
        pass
    except Exception, e:
        raise
