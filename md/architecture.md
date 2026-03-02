Aidan Orion 23 Feb 2026

# Front End Styling:
## Web pages: Landing Page, Login, Wiki, Forum, Game Page.
### Landing Page: 
Basic story intro, basic rundown of things you can do in the game/pitch.
### Login:
self explanitory
### Wiki:
detailed info on the game.
### Forum:
a place for players to talk about the game
### Game page:
where the game is played. Three screen interface, leftmost panel is a menu, middle pannel is a clickable section with all the things you can select, right panel is a details and actions panel, where you can choose what to do.

# Front end functionality:
### Game page:
Every 5 seconds, a tick in game happens, which means the server passes back info to every connected player and in between those ticks players choose what to do in the actions panel, which sends the request to the server, which responds to the request in particular ways.
### Wiki page:
A simple server that is litterally just POST/GET 
### Forum:
Similar to wiki page, but has comments and stuff, perhaps each faction can have their own section too. (though I would imagine they might use a third party app like discord a lot)

# Back end functionality:
### Game API:
Actions are Posted, giving a 200 okay if the server successfully gets the request and stores it. There is also an endpoint to get the situation at the current location. And another endpoint that acts as a ping-pong between the server and the client where the client is saying to the server: hey! give me the next update! that sits in the server until the server finishes the tick and then passes the new info back to each ping. Also there needs to be an enpoint to get details on different objects, ships, players, etc.
### Persisence:
The skeleton of the project. We're using JSON right now. Potential upgrade to an ultra simple database in the future if it starts getting above 10GB memory.