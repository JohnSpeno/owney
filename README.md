Description
-----------

Owney is a tool to track United States Postal Service (USPS) packages. It is written in Python and uses the USPS webtools API.

In order to use Owney, you must first register with the USPS to obtain access to their webtools API. You can find details on that
process and other "useful" documentation at [USPS Web Tools](http://www.usps.com/webtools/).

Owney is comprised of several parts. They are:

1. database - The Shipments database. Contains data about each of your packages. 

1. loader - a tool to load packages into your database. 

1. poller - a tool to periodically update the status of each of your packages. 

1. A Django web interface to view your undelivered packages.

Owney is named in honor of the [famous dog](http://www.postalmuseum.si.edu/exhibits/2c1f_owney.html). Woof!

Usage
-----

1. Edit settings
        USPS web tools api username
        helpspot url

1. Load your packages data into the database.

1. Periodically poll the delivery status of each undelivered package in the database and update as needed.

Author
------
John P. Speno speno@macspeno.com

[http://macspeno.com/jps/](http://macspeno.com/jps/)
