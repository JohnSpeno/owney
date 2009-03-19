Description
-----------

Owney (rhymes with Poney) is a tool to track United States Postal Service (USPS) packages. It is written
in Python and uses the USPS webtools API. It also uses Django.

In order to use Owney, you must first register with the USPS to obtain access to their webtools API. You can find details on that process and other "useful" documentation at [USPS Web Tools](http://www.usps.com/webtools/).

Owney is comprised of several parts. They are:

1. database - The Shipments database. Contains data about each of your shipments. 

1. loader - a tool to load shipments into your database.

1. poller - a tool to periodically update the status of each of your shipments. 

1. A Django web interface to view and manage your shipments.

Owney is named in honor of the [famous dog](http://www.postalmuseum.si.edu/exhibits/2c1f_owney.html). Woof!

Usage
-----

1. Edit settings
        USPS web tools api username
        customer serivce url

1. Load your packages data into the database.

1. Periodically poll the delivery status of each undelivered package in the database and update as needed.

Observations
------------

The status of a typical shipment normally happens like this:

1. First the shipment is *new* which means that you've told Owney about a tracking
number but the USPS won't have a record for it.

1. After some time, your shipment may become *acknowledged* which means that the USPS
has the electronic record of your tracking number.

1. If your physical shipment is scanned either individually or via inclusion of a SCAN
form, then the next status you can expect to see is *accepted*. This indicates that
your local USPS office took possesion of the shipment. It's in their hands now.

1. Your package may now be *processed* at one or more USPS facilities as it travels
towards (hopefully) its destination.

1. The next status that may happen is *arrival*. This is a good sign that your
shipment is at the USPS office which will perform the final delivery.

1. And then, fingers crossed, your package will become *delivered*. If may also be
*forwarded*, which might start the cycle over again.

And of course, sometimes things do not go as they should. Your package may encounter
what I call an exception. Owney recognizes the following exception types:

* Notice Left - this is the most common exception. A notice of the attempted delivery is
supposed to be left with the recipient. Many times they aren't left or get lost
(they are quite small and easy to overlook). The recipient may need to contact their
local USPS office to arrange redelivery or pick-up.
* No Such Number
* Undeliverable as Addressed
* Return to Sender
* Missent - this one is the fault of the USPS. They sent your shipment someplace it
should not have gone and they noticed their mistake and re-routed the shipment.

Of course, not every package goes through every status. Also, for whatever reason,
sometimes the status changes of your shipments are not updated in a timely fashion.
E.g. you may see a shipment arrive and yet you may not get a notice of its delivery
until days later, even if the shipment was delivered on the same day as the arrival
notice.

Author
------
John P. Speno speno@macspeno.com

[http://macspeno.com/jps/](http://macspeno.com/jps/)
