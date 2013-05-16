feature_flipper
===============

hack week at Top Hat with Stevo!

server side Django. Tastypie REST, Waffle feature flipping.

graceful degradation

anson: thm example: api/v2/authorization

testing: advanced rest client for chrome; https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo; restforchrome.blogspot.com

authentication
http://django-tastypie.readthedocs.org/en/latest/authentication_authorization.html

REST API endpoints
------------------

Get status of a feature is on/off for user   /api/feature/[f_id]/user/[u_id]/ GET
Get status of all feature for user	         /api/feature/user/[u_id]/ GET

Create a user	               /api/user/ POST
Get a list of users	           /api/user/ GET
Get a user	                   /api/user/[id] GET

Create a question	           /api/question/ POST
Get a list of questions	       /api/question/ GET
Get a question	               /api/question/[id]/ GET

Create an answer	           /api/answer/ POST
Get a list of answers          /api/answer/ GET
Query: answers for question    /api/answer/?question=[id] GET
Get an answer	               /api/answer/[id]/ GET

Create a votes                 /api/vote/ POST
Get a list of votes            /api/vote/ GET
Query: votes for answer        /api/vote/?answer=[id] GET

Create a notification          /api/notification/ POST
Get a notification             /api/notification/[id]/ GET
Query: notifications for user  /api/notification/?user_to=[id] GET

Check session				   /api/session/ GET
Create session				   /api/session/ POST

Also works                     PUT, DELETE

json payload
------------

vote POST json payload
{
"user": {"pk":2},
"answer": {"pk":2},
"timestamp": "2013-05-15T14:24:37.521Z"
}


notification POST json payload
{
"user_from": {"pk":2},
"user_to": {"pk":3},
"message": "sup stevo",
"timestamp": "2013-05-15T14:24:37.521Z"
}


example POST json
{
	"id": 5,
	"question": "when is the right time",
	"answer": "now",
	"timestamp": "2013-01-01 00-00-00",
	"user": {"pk" : 1}
}


demo
----

1. turning something off in critical error
2. diff users, diff features (randomize)


caveats
-------

waffle requires flag name as identifier -> SOLVED use name as an identifier, use notes for text
resource featuring -> SOLVED using authentication checking whether user should have feature.
database - changes to model are one-way
critical error: web sockets for server instantly tell client

cookie - first load doesnt go so well


switches -> fixed

next steps
----------
ab-testing: tracking data for users based on features active
better interface for user groups


commands
--------

pip install django-waffle
load fixtures: python manage.py loaddata initial_data.json


notes
-----
cookie names - spaces not allowed



