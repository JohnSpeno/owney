Description
-----------
Owney (rhymes with Pony) is a tool to track United States Postal Service
(USPS) shipments. It is written in Python and uses the USPS webtools API. It
also uses Django, mainly for its database ORM.

Owney is a work in progress. In fact, the current public release has not
been tested by its author and there's lots of room for improvement.

Owney is named in honor of the [famous
dog](http://www.postalmuseum.si.edu/exhibits/2c1f_owney.html). Woof!


Owney is comprised of several parts. They are:

1. database - The Shipments database. Contains data about each of your
shipments. This is defined using django's ORM in the owney directory of
this project.

1. add_shipments.py - a tool to load shipments into your database from an
Endicia XML output file. This is in the tools directory.

1. watch_shipments.py - a tool to periodically update the status of each of
your shipments. It needs to be run periodically. This is also in the tools
directory.

1. A Django web interface to view and manage your shipments. This also lives in
the owney subdirectory.

Usage
-----
In order to use Owney, you must first register with the USPS to obtain access
to their webtools API. You can find details on that process and other "useful"
documentation at [USPS Web Tools](http://www.usps.com/webtools/).

It's probably also helpful to use Endicia to generate the shipping labels
for your shipments as Owney currently only knows how to import its
shipments from Endicia's output files. Learn more about Endicia's XML
formats here: <http://mac.endicia.com/extras/xml/>

1. Edit owney.conf.settings to set the name of your USPS web tools API
Username and set the base URL for your Customer Service application. You
may not have one of those. I like this one:
<http://www.userscape.com/products/helpspot/>. You can also set these in
your django project's settings module in which case the names are OWNEY_USPS_API_USERID
and OWNEY_TRACKING_CS_URL.

1. Load your packages data into the database using add_shipments.py.

1. Periodically run watch_shipments.py to poll and update the delivery status of each undelivered package in the database.


The Life Cycle of a Shipment
----------------------------
These are my notes from observing thousands of packages. I don't have any
special knowledge of the internals of the USPS. The status of a typical
shipment may happen like this:

1. First the shipment is *new* which means that you've told Owney about a
tracking number but the USPS does not yet have a record of it.

1. After some time, your shipment may become *acknowledged* which means that
the USPS has the electronic record of your tracking number.

1. If your physical shipment is scanned either individually or via inclusion on
a SCAN form, then the next status you can expect to see is *accepted*. This
indicates that your local USPS office took possesion of the shipment. It's in
their hands now.

1. Your package may now be *processed* at one or more USPS sorting facilities as it travels towards its destination.

1. The next status that may happen is *arrival*. This is a good sign that your
shipment is at the USPS office which will perform its final delivery.

1. And then, fingers crossed, your package will become *delivered*. If may also
be *forwarded*, which might start the cycle over again.

And of course, sometimes things do not go as they should. Your package may
encounter what I call exceptions. Owney recognizes the following exception
types:

* Notice Left - this is the most common exception. A notice of the attempted
delivery should have been left with the recipient. Many times they aren't left
or get lost (they are quite small and easy to overlook). The recipient may need
to contact their local USPS office to arrange redelivery or pick-up.

* Missent - this one is the fault of the USPS. They sent your shipment
someplace it should not have gone, noticed their mistake and re-routed
the shipment.

And these three exceptions usually mean your shipment is being returned to you.

* No Such Number  

* Undeliverable as Addressed

* Return to Sender

Of course, not every package goes through every status. Also, for whatever
reason, sometimes the status changes of your shipments are not updated in a
timely fashion. For example, you may see a shipment arrive and yet you may not
get a notice of its delivery until days later, even if the shipment was
delivered on the same day as it arrived.

Shipments to US Military Bases (APO addresses) often won't get marked
as *delivered* so you'll want to do that by hand.

Another issue that can confuse Owney is when there is a difference between the
results of a TrackRequest and TrackFieldRequest API calls. Owney uses
TrackFieldRequest exclusively. You may notice that sometimes the USPS online
tracking page shows different results than Owney. In those cases, a
TrackRequest API call would probably show more up to date data, but Owney won't
know about it unless you edit the shipment by hand.


Author
------
John P. Speno john@macspeno.com

Thanks
------
aaron tuller and the endicia mac team
