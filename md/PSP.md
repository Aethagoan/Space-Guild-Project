Think. Write. Segment. Do. Ensure.

<hr>

## Think:
I want the backend to collect requests to do over one tick.

I am planning to do this by making a dictionary that maps object token to action.
Every tick, the dictionary will sort all requests into different lists of different actions.

There is a bit of time dependency, requests that come in first need to happen first-for example, if two people are trying to grab an item on the same tick, only one person should get the item, and perhaps the server should return to the player a list of actions that happened in their location in the tick so they can see who picked up the item before them.

Similarly, certain actions should run first for balance reasons. I would rather that people are able to move before damage is applied. So If someone wants to escape a fight, they can move right out. This seems to create some interesting problems like when two players try to grab the same item and the other jumps away, there is just no catching them. But conversely, a system without this mechanic could also be abused. If it takes multiple cycles to jump to a new location, a big enough group (or botnet) could target a single player and blow them up instantly without provokation.

I realize I should start making a list of problems that could make the game unstable.
- Running with no risk
- Dying instantly in innapropriate manners due to the actions of other players or in game NPCs



I wonder if this means that I should do a two-step tick mechanism where actions are declared. I think that would be cool, the only problem currently would be that with the current setup I have is that there would be no way to bind subscribers to these events. I don't hold connections between server and client, I can't just send info to the client whenever. For now, the cost of a feature like this is too high.

This still leaves me with some options. These things could be limited in some way, for instance, maybe we have movement happen last--but limit incoming attacks, maybe there's a limit to how many times one can be hit in a tick.

~~Now that I think about it, there might be a problem with the game I hadn't thought of. One can declare an action by sending a request to the server. The server should then respond~~

I thought of a solution...? Each time someone sends a request, they are sending more than one. So for example, you want to declare that you'll do something-You send the request for doing that thing, and you send a request to be updated when that action finishes. This way-the server can respond instantly with 'you can do that' or 'you can't do that' or whatever else, and then when the tick finishes (up to five seconds later) the second request will come back to update what the user can see (and give them a log of what happened.) We might optimize this by keeping track of if the user has sent this request--and sending one if it hasn't been sent, and maybe there could also be an endpoint that just returns the state of affairs quickly.

## Write:
ENDPOINTS:
Actions
UpdateMe
RespondWhenNewTick

## Segment:
Actions - These are somewhat complete. 
 - I need to make a dictionary that maps object token -> action verb.
 - I need to make a function that takes all of the key-value pairs of the dictionary and sorts them into action lists.
 - I need to create the login that fires certain actions first, and limits other actions in different ways.

 UpdateMe - Incomplete
 - I need to make an endpoint that gets the current state of a location. Who is there, what is there - and returns it immediately.

RespondWhenNewTick - The difficult one
When we get this request we need the token of the player. This function should then wait for the rollover of the tick, find where this token is located, and return the state.

A new idea - I should have thought of this before, but I may need to keep track of what happened in the last tick. This probably means I'll make something like a dictionary of location -> list that each action appends to that list. All of the keys in the dictionary clear/reset at the start/execution of the next tick. The state of a place is what is located there and what happened last tick.
- WhathappenedDictionary

