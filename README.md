feature_flipper
===============

hack week at Top Hat with Stevo!

server side Django. Tastypie REST, Waffle feature flipping.


todo:
vote model: timestamp, user id, answer-id

REST API endpoints
------------------
Create a user	         example.com/api/user/ POST
Get a list of users	     example.com/api/user/ GET
Get a user	             example.com/api/user/[id] GET
Create a question	     example.com/api/question/ POST
Get a list of questions	 example.com/api/question/ GET
Get a question	         example.com/api/question/[id] GET
Create an answer	     example.com/api/answer/ POST
Get a list of answers    example.com/api/answer/GET
Query: list of answers   example.com/api/answer/?question=[id] GET
Get an answer	         example.com/api/answer/[id] GET


caveats
-------

waffle requires flag name as identifier
database - wrapping models


commands
--------

load fixtures: python manage.py loaddata initial_data.json


filtering 

get question ?=id