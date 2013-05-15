feature_flipper
===============

hack week at Top Hat with Stevo!

server side Django. Tastypie REST, Waffle feature flipping.

todo:
wrap q, a, v, n in waffle for tastypie
- ask anson: where are the tastypie views?

REST API endpoints
------------------
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


example POST json
{
	"id": 5,
	"question": "when is the right time",
	"answer": "now",
	"timestamp": "2013-01-01 00-00-00",
	"user": {"pk" : 1}
}

caveats
-------

waffle requires flag name as identifier
database - changes to model are one-way

next steps
----------
ab-testing: tracking data for users based on features active


commands
--------

load fixtures: python manage.py loaddata initial_data.json


demo
----

1. turning something off in critical error
2. 



showing some users (randomize) - (still working on authentication)
