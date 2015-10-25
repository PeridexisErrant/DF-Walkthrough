################
Use of Minecarts
################

This masterclass on Minecarts, containing significant original
research,
was written by Larix.  :forums:`See the original here <144328>`, or
check out :wiki:`the wiki on minecarts <Minecarts>`.

The wiki article contains a lot of varied information, but i've
delved quite a bit into minecart pathing; i.e. where a minecart goes
when you let it run free, how its paths change and so on. There's
almost no in-depth information on all this stuff on the wikI and it
seems to me that much of it isn't well understood.

I encourage all readers to replicate my designs and experiments and
offer corrections or alternative interpretations. In order to
properly trace what's going on, you will need to look at events
closely and that means (unless you have an infallible hack script to
do it for you) you'll need to pause the game, advance by single steps
and count the steps exactly. You can't just eyeball the speed as
"pretty fast" or "sort of sluggish", you'll have to e.g. count out a
hundred steps and look how far a cart travels in that time, so you
can definitely tell whether a cart moves at 45000 or 55000 speed.


.. contents::


Let's start simple.


Lesson One: Track on flat floor
===============================

In short, the only type of track that matters to a free-running cart
are corners. All other types are irrelevant.

A sweeping statement, sure, but I found it to be perfectly true. The
basic rule is that a minecart will move in a straight line. The only
exception is when it encounters a track corner (the two-connection
type, not T-junctions) that's connected to the direction the cart is
coming from. Let's take an example::

    a═══════╗   b═════╝

Cart gets pushed east from a/b, moves east until the corner and turns
south/north there.
::

    a║╚╔╣╩╦╠╗    b╬╥╨╞╡╝

Cart gets pushed and *behaves exactly the same as above.*

The cart incidentally also behaves like that when the route before
the corner is entirely non-tracked floor, it'll path just the same,
it will only slow down more thanks to higher friction.

Why is this so? As far as I can tell, the game doesn't calculate any
sort of "heading" for the cart, it just keeps track of the velocity,
probably split between x- and y- axis. When the cart moves over flat
floor, all that'll happen on "direction-neutral" track is
deceleration. When the cart is re-pathed by a legal corner, the whole
input speed is taken and turned into speed in the exit direction of
the corner.

"Straight" tracks have no pathing power over minecarts, they don't
keep them "on track", because carts don't consider themselves "on
track" in the first place. They're in contact with the floor and
react to corners/constructions, or they're in flight and don't.
That's it.



Lesson Two: Ramps, basics
=========================

Of course, everyone who works with carts for a while will probably
get to love ramps. They allow carts to climb levels, they can provide
speed, they even allow perpetual motion.

First of all, what makes a ramp tick?

A ramp is only fully traversible for carts and can only provide
acceleration if it's properly connected by track. There are two
arguments that get checked, and they concern track connections and
nothing else. It doesn't matter where the cart comes from, whether it
changes level or not, it's all about how the ramp is built.

* Requirement one: the ramp must have track connection to wall. One,
  two or three connections are all acceptable.

* Requirement two: the ramp must have exactly one track connection to
  a non-wall tile. This can be an adjacent ramp on the same level, flat
  floor or a hole (e.g. containing a down ramp).

Examples of functional track ramps::

    #    #    #    #     #     #
    ║    ║    ║    ╚+   #╩+   #╬#
    +    ▲    ▼                +

All shown track engraved on up ramp.

:``▲``:     up ramp
:``▼``:     down ramp (i.e. hole containing a ramp)
:``+``:     flat floor

Examples of non-functional track ramps::

    ###   ###   ##
    +═+   +╩+   #╝

* first example: no connection to wall
* second: more than one connection to floor
* third: no connection to floor

When a ramp is properly connected, it provides acceleration towards
its "down" direction; ~5000 speed units for every step a cart moves
across it. Ten steps of acceleration give as much speed as a
highest-speed roller, but you'll need multiple ramps for that.

The important part is that the game only checks if the ramp is
properly connected, it doesn't check where the cart's coming from.
This is the foundation of the fabled impulse ramp - a cart entering
this ramp::

    ###
    +╚+

from the west will be accelerated towards the east, the same as a
cart going down a level down such a ramp::

    #═+

(cart's coming from track or a ramp on the level above). Impulse
ramps thus grant speed without needing to sacrifice height, no more.
They do not provide more or a different acceleration, just the exact
same amount (which is quite a lot considering it means perpetual
motion at practically any speed up to ~250.000 that you desire).

If a cart moves onto a ramp from the ramp's down direction, it'll be
accelerated in the direction it was coming from, i.e. it decelerates
(at the normal ramp rate). Excepting a rather powerful bug that'll
come up later, this deceleration will stop carts that are moving at
the speed of a medium-speed roller or less before they reach a ramp's
top, whereupon they'll roll back down from the place they've reached.
The resulting speed when leaving the ramp again will be less than the
speed the cart entered with, a cart bouncing between two ramps
separated by one tile of level floor.
::

    #####       #####        #####
    #▲═▲#       #═══#        #╚═╝#
    ramps         track variants

will after about a dozen bounces stop on the flat middle tile.
There's no observable difference between the two ramp layouts.


I built a fifteen-level straight ramp slope to measure the speeds
different numbers of ramps will give to a cart. While the speeds
found were just as expected and only of minor practical use (as
reference to "generate" carts of specific speeds), the experiment
provided a few valuable pointers, stuff that has been worked out by
others before but doesn't seem to be widely known:

* a dropped cart (I always dropped it off a hatch) will land in the
  middle of the tile below and only roll down _half_ the ramp it lands
  on.
* the speed rises with the number of turns the cart spends on the
  ramps (just under 5000 speed for every turn, ~130 000 for a cart sent
  down a fifteen-level ramp), but one turn is subtracted from the
  count; i.e. the cart is charged ~5000 speed for leaving the ramps in
  the end.
* the "length" of a ramp is bigger than that of a flat tile. Since I
  only had full steps to calculate with, the numbers aren't
  super-precise, but it appears to be sqrt 2  times the length of a
  flat tile (the "lost" acceleration step mentioned above actually is
  needed for the length calculation to best fit the results).

Out of curiosity, I checked "catching" a cart falling down a vertical
shaft with a track ramp since i've seen reports that paying attention
to the exact level and different designs were required. I drilled
down a 40-z shaft and built a ramp at the bottom of it (ordinary EW
ramp with wall to the west and floor to the east). The cart fell
down, landed half-way up the ramp and rolled off at the usual
half-ramp speed of ~20.000. I tried it at different adjacent levels,
and the result was always the same: none of the vertical speed was
preserved (over 1 zlevel per step), the cart never failed to be
accelerated. If you got different results, i'd like to hear how you
got them. I dropped the cart via hatch, which afaik is the easiest
way to guarantee a clean drop without colliding with the shaft's walls.

Enough for now, more to follow.

As a sum of lesson two, i'd offer:

Ramps' main parameter is the direction they accelerate to. The exact
track engraved on them and where a cart enters the ramp is secondary.
If there's a corner engraved on the ramp and the cart actually moves
following that corner, the corner is respected (and things get
weird), otherwise exact track is just as irrelevant as on level floor.


Lesson Three: rollers and guided carts
======================================

Rollers are the powered means of providing speed to a cart. As has
been widely observed

* for practical purposes, it's easiest to assume that rollers simply
  *set* the cart's speed to a fixed value.
  *see below, "Late P.S." - I found that rollers really provide
  acceleration, it's just a very large amount and the acceleration
  gets capped at the roller's set speed. The effect rarely
  materialises, only when working with high-speed carts and only when
  speed and attitude are just "right".*
* rollers will not slow down a cart moving faster than the roller's
  set speed; they will "brake" and turn around a cart moving in the
  opposite direction
* rollers working laterally to a cart's current movement direction
  result in *diagonal* movement
* rollers only affect free-running carts (not guided carts) and only
  when they are on top of track. Rollers on ordinary floor are ignored.
* rollers which are not powered are completely ignored, you just get
  the effects of the tile underneath.

The "braking" power of rollers is impressive: each step spent on an
opposing roller slows down a cart by 100 000 speed units. The
strongest track stops slow a cart by 50.000 per step. You need a very
speedy cart to keep moving past a single-tile roller. A cart moving
more than one tile per step will, however, not be affected by the
friction of tiles it "skips" over during its turns; only the tiles
it's in at the end of a step do count. Two rollers (of any speed) in
the correct spots are enough to stop and turn around a cart moving at
maximum ramp speed (~270.000, that's eight tiles in three steps on
average).

Since non-corner track doesn't matter, it also doesn't matter much
what kind of track you build a roller on. A west-pushing roller on an
E-W track tile works the same way as a west-pushing roller on N-S
track, an E "track end" or a NSE t-junction.

Corners do affect the way rollers work, however:

a) a roller pushing "from" a connection of a track corner results in
movement towards the corner's exit direction, *not* towards the
roller's push direction.
b) a roller on a track corner pushing from a direction the corner
does *not* connect to pushes to its normal direction (of necessity
one of the track corner's connections) and may cause diagonal movement.

a)::

    .║      ║
    ═╗═    ═╢═
     ║      ║

:``╢``:     Roller pushing east

No matter where the cart comes from, it exits to the south as long as
the roller is powered (and the cart isn't super-fast). The most
evidently useful application is with a cart coming from the east,
because that allows a simple powered switch: when the roller is off,
the cart moves off to the west, if the roller is on, the cart goes
south.

Still, it's interesting to see that carts coming from the north or
south are not thrown into a diagonal, although the roller's nominal
push direction is lateral to their movement. It looks like the corner
sort of turns the roller's effect around.

b)::

    .║      ║
    ═╗═    ═╟═
     ║      ║

:``╟``:     Roller pushing west

Results: when the cart comes from the east or west, it moves west.
Carts coming from the north go on a diagonal heading southwest.
Carts coming from the south go on a diagonal heading northwest.

Since the roller's "push from" direction is not in line with the
corner, it keeps its "push to" direction *and causes the cart coming
from the south to ignore the corner track*. The latter isn't some
kind of cumulative speed derailing, it happens when combining two
low-speed effects which even theoretically can't add up to more than
40.000 (50.000+ is the derail threshold). The only rationale I can
find for it is that the roller indeed "overrules" the corner when
active.

More likely, however, the laterally-working roller just "adds" its
movement speed to the cart's velocity and leaves it to the corner to
sort things out. The observation remains valid that a roller pushing
"into" a corner is less likely to cause wild diagonal movement even
when working laterally, while a roller working towards a corner's
exit often causes trouble. On the whole, however, cart motion is most
predictable and controllable when working with rollers in line or
opposed to cart direction, not with lateral rollers. Corners appear
to apply at the end of a turn, after all speed changes on the tile
are done with, so in the example above, the "bend the cart to the
south" effect of the corner happens after the last "set speed towards
east" effect of the roller and the leaving cart goes off with
southward-only speed and no eastward component.

**A cart encountering a laterally-working roller which does not sit
on a corner will generally be thrown off onto a diagonal
trajectory.** Diagonally-moving carts are great fun, because (Lesson
One) only corners matter, so the carts'll merrily barrel all across
your carefully laid-out track, smacking into walls and stopping or
going places you don't want them (most cases of unexplicably-stopping
carts are due to diagonal movement and wall collisions). Unless you
manage to thread them through track corners, that is, because a cart
properly taking a corner will move precisely in its exit direction
and will not retain any diagonal movement component. More on that
later.

Late PS: rather confusing results of a recent roller-based device
show that rollers indeed accelerate carts, at 100.000 subtiles/step²
in their given direction, *but capped at roller's set speed*. When a
cart moves from roller to roller, this won't matter: since the
highest speed that can be imparted by a roller is 50.000, the 100.000
acceleration is enough to neutralise the speed of a cart incoming at
max. roller speed *and* impart max speed, all in a single step.
However, if the cart moves at higher speeds, one step of acceleration
may only change it from, say, -70.000 to +30.000 and when the cart
leaves the roller's tile on the following turn, it will move at the
received 30.000 speed, even if it was affected by a highest-speed
roller with a set speed of 50.000. In addition, the cart actually
calculates the distances it moves on the roller's tile, so the right
combination of cart speed and "offset" can result in very irregular
speeds. A rather bare-bones test allowed achieving different non-max
speeds from a highest-speed roller by slightly varying input speed -
from 12.000 to 22.000, both from a "highest" roller.


I'll make **guided carts** short, because there's not much about
them: guided carts ignore special track buildings like rollers or
track stops, the pushing dwarf just moves them at their walking
speed, much like a wheelbarrow. Track must be "connected" for dwarfs
to actually guide a cart. If they find no connection, they'll lug the
cart by hand, which ranges from much slower to abysmally slow.
"Connectivity" is quite lenient, however - in most cases, a tile only
needs one track connection in the correct direction, and bridges are
accepted as track, too. It's best to just engrave/build an
identifiable unbroken track, though. Guided track can go up/down
ramps without trouble, all at the normal dwarven walking speed.


Lesson Four: Flight
===================

Carts can be sent over ramps or over the lips of cliffs, and the game
will trace a ballistic trajectory. Carts in flight are not subject to
air friction (according to hack scripts), but they are subject to
gravity. Someone did the calculation, I forget. Anyway, observation
tells us that a free-falling cart takes as long to reach the bottom
of a shaft as one rolling down a flight of ramps. Thus, the
acceleration is the same - corrected for the greater length of ramps
(sqrt 2 times length of a flat tile), we get something just under
0,035 zlevels/step². (Which shows that dwarven physics are screwy,
acceleration on a ramp should be lower than free-fall acceleration.)

A cart released by a hatch takes six steps before it's displayed on
the next level down, which suggests - hm, that the cart is considered
to start falling about 2/3 up the current level? There's some tricky
stuff going on with the decision whether a cart's actually in contact
with the floor (and thus subject to corners, rollers and track
stops): carts can make small jumps in some cases which don't move
them to a different level, and in those cases it seems to take ~those
six steps before they start registering as "on floor" again.

A cart pushed off a cliff follows an ordinary downward curve. It
keeps its horizontal velocity and will keep moving at the same speed
when it lands, while vertical speed will build up during the fall and
will completely disappear when it hits the ground.

If a cart is sent over an upward ramp into the open sky, it can go up
several levels, depending on its speed. A highest-speed roller will
barely manage a hop, the cart won't even reach the level above the
ramp, but it'll be in flight for a few steps. A cart accelerated by a
long downward slope or an impulse ramp array can go over the ramp at
much higher speeds and can reach heights of up to 26 z-levels (or
more with added trickery). The "launch ramp" converts the horizontal
speed of the incoming cart into ramped-upward velocity, and the
upward component will grant height while gravity nibbles away at it.

Counting steps and trying to calculate out the results, my best
estimation for ramp launches is as follows:
The baseline is the speed on horizontal track. This speed is
converted into speed calculated for ramps. When released, the cart
moves vertically at 1/2 the original speed and horizontally at ~70%
of the original speed. Assuming this is all ramp stuff, it's likely
sqrt 1/2 the original speed horizontally. As per usual, vertical
speed disappears upon landing and if the cart is launched off a ramp
again, its horizontal speed will be 1/2 the original, vertical speed
sqrt 1/8 (ca. 35%) and the height reached will only be about one half
of what the first jump achieved (a bit less because of ramping speed
costs).

Standard design for a launch ramp::

    .
    ____/#

Fast cart comes from the west, goes over the ramp, flight happens. It
must be a proper track ramp :P

Carts that fail to enter a hole in the floor "jump" over it, and this
also seems to count as flight: speedy carts will not follow a track
going down a ramp when coming from level track, and they will ignore
corners directly behind the hole because they haven't touched floor
again.

The peculiar feature of speed supercharging still exists in 0.40.11:
if two carts of similar speed collide frontally and the "pushing"
cart is between 1 and 100% heavier than the "pushed" cart, momentum
of the pusher will be conserved. That's to say, the pushed cart will
move off at a speed higher than what the pushing cart brought to the
collision. This allows breaking the speed limit on ramp and gravity
acceleration (270.000 reportedly). Carts moving that fast are subject
to an exceptional friction of 10.000 per step, all the time, thus
only very short bursts of extreme speed are possible and since
high-speed collisions are required, no cargo can be transported. In a
quick-and-dirty test for 40.11, I just smashed two hazel wood carts
together, one loaded to double weight, and right enough, the pushed
cart moved 29 tiles in six steps. In .34.11, I managed burst speeds
of up to 17 tiles/step through tiered collisions and ramped jumps of
45 z-levels. The latter was what I meant with "added trickery" above.

Bodycount: 6 dogs (+1 since last update), one mangled dwarf (survived
and is fine, but keeps cleaning himself).



Lesson Five: diagonal movement and how to fix it
================================================

Diagonal movement, on the face of it just means that a cart is not
moving in a cardinal direction and will eventually move off the
"straight line" or bump into a wall, stopping dead.

I admit that this is just interpretation, but i'm reasonably certain
that diagonal movement is not handled as a "heading" like "fifteen
marks east off north" but rather as a combination of movement on the
two flat axes.

Laborious example: A cart pushed north by one highest-speed roller,
then east by a lowest-speed roller doesn't move "north by northeast"
but rather "50.000 north and 10.000 east" and each of these
components is separately subject to floor friction. Letting the cart
roll over higher-friction floor (like non-track floor) shows that the
cart will only take five steps (and three tiles) to move the first
step to the east (since its eastward movement started in the middle
of the tile, it only needs to move half a tile to switch over to the
next), twelve steps and six tiles for the next, 22 steps and nine
tiles for the third, and it won't make a fourth step to the east:
after fifty steps, the eastward component of the cart's movement
should be entirely gone. (It would take a rather unfeasible 1000
steps on track-engraved floor.)

Admittedly, accepting the sideways aberration and trying to remove it
by floor friction is rarely an option.

Diagonal movement commonly occurs *when a cart moves up a corner
ramp*. Since minecarts don't care about flat-floor track apart from
corners, a long straight track line will do nothing to rule in a
diagonally-moving cart, it'll just move along and take its sideways
step when it's time. And if there's a wall next to the track (e.g.
because you're trying to keep accelerating the cart via impulse
ramps) it'll just hit the wall and stop, at least temporarily. If it
stops on flat track, it'll stop for good, if it stops on a ramp,
it'll start moving again, but it may lose its load. As far as I can
tell, that was the problem encountered in `this water gun design
<http://mkv25.net/dfma/movie-2507-strange>`_. Thanks to uncorrected
truetype font turning all text into garbage, I can only guess (and
you better ramp speed up to 1000+ and "step" the thing yourself by
hitting forward/pause repeatedly).

Note: in my experience, a cart always gets one ramp-step's speed
(i.e. about 5000, 1/20 tile/step) to the "outside" of the curve on
the corner ramp. It will step off the straight path on the eleventh
step after the corner, i.e. after this lateral speed component has
accumulated half a tile of distance. This holds both for a cart
propelled by a highest-speed roller (50.000 speed) and a
maximum-speed cyclotron (265.000); both will stop/go off the straight
path after ten steps.

I've re-built WanderingKid's impulse/something elevator and found the
problem he faced (:forums:`reported here <129453.msg4461651#msg4461651>`)
was also nothing fancier than diagonal movement: sending the
output of a corner ramp onto a straight (i.e. inconsequential) track.
In my re-build, the cart would move off the straight line on the
eleventh step after the corner.

So how to avoid diagonal-movement troubles?

The easiest option is not to generate diagonal movement in the first
place: don't use corner ramps to move carts up levels. For moving
carts up levels, straight ramps work just as well as corner ramps;
better in fact, since they don't cause the added 1000 speed loss from
the corner (and don't cause diagonal movement). There are some
special cases of upward movement over multiple levels which require
corner ramps, but if you only want to go up a single level, just use
a straight ramp.

The other option, when corner ramps are used, is to use the one track
type carts care about: corners.

If a cart tries to leave a corner tile, the game checks whether the
border the cart tries to leave over is "blocked" by the corner: on a
NW corner, those will be the E and S borders. If a cart tries to
leave to the south, it's treated as coming from the north, and it
leaves towards the west. This rule appears to only care for the tile
border the cart tries to leave over. A diagonally-moving cart is also
subject to these checks: let's assume a cart moving from the
northwest towards the southeast: if the tile the cart'd leave to
would be the one directly south of the corner, the cart will turn
around to the west and will move west only. Notably, the resulting
speed is the cart's previous N->S velocity, the W->E velocity will
disappear. If the cart would have left to the eastern tile, it'll
turn north (moving at the previous W->E velocity). If the cart's
go-to tile is the exact southeastern one, the corner will not affect
it. Which of the two axial speeds is higher doesn't matter.
A cart moving from northeast to southwest will only be affected by
the corner if its go-to tile is the southern one. If it tries to
leave to the western (or southwestern) tile, it'll stay on its
diagonal course, because the border over which it attempts to leave
isn't blocked.

My standard approach to the output of corner ramps is to just put a
corner on the tile immediately behind the ramp, like this::

    z+0       z+1
    ####      ══╗
    ══▲#      ++▼

    ####
    ══╝#
    track on ramp

I've yet to see a case where this doesn't work (if necessary propped
up by a wall behind the corner above when working with fast carts).

PS: my best interpretation is that a corner "sets" the cart's speed
in the exit direction to its previous value in the "input" direction.
Since the diagonal component is actually velocity on the corner's
exit axis, that part of the cart's movement speed just gets
overwritten. Result in any case: successfully rounded corners fix
diagonal movement.

Example of weird behaviour::

    ╔═╧#
    ╚═╝

:``╧``:     roller pushing south, medium speed (I didn't check all
            speeds, but highest is too fast).
            Track under the roller - doesn't matter, something
            inconsequential like NS or EW.

Upon first being pushed, the cart goes around the circuit normally.
But when it then reaches the roller again, it will move south into
the corner after two steps, then north after one to two steps, then
south again and then once more through the loop. Interpretation: the
cart is pushed into a southeasternish course, which is recognised as
coming from the west by the corner, so it gets bent around to the
north, reflected by the roller and then goes through the corner
normally, entering from the north and leaving to the west this time.


Lesson Six: False ramps
=======================

In the ramps section, I mentioned ramps which don't accelerate carts.
Those may seem kind of pointless for building tracks, but the lack of
acceleration can actually be a benefit.

If a ramp connecting levels doesn't cause friction, you can change
level without losing/gaining speed (apart from ordinary floor
friction). It's decidedly weird - my constructions only work when the
cart enters at very low speed - around that of a dwarven push - but a
single push can move a cart up/down 40+ levels without notably
changing the cart's speed.
(`example <http://mkv25.net/dfma/movie-2653-minecartescalator>`_
(o hey, it was 47
z. You can safely speed past the end, I just showed that each ramp
was a non-functional E-only one.) It's of course also possible to do
this without dwarven labour, you just need sufficiently regulated
cart speeds from proper ramps or rollers, if needed combined with a
few track stops. A super-low-tech and low-risk way of lifting a cart
up a huge number of levels.

Another application of false ramps is to make the loading of liquids
into carts easier :forums:`pioneered by flameaway.
<120435.msg3873427#msg3873427>`
I found it to be an impressively fast,
fully-automatable loading mechanism for waterguns allowing cadences
of up to one shot per ten steps (using multiple carts in one barrel).
It works so well because it *doesn't accelerate/decelerate the
carts*. The loader simply consists of a single channelled-out tile
containing a track ramp with no actual down direction. Its track
connections only go to wall,  therefore it is treated as ordinary
flat floor by the game. The cart is never at the "bottom" of the
"ramp", because as far as the minecart engine is concerned, there's
no ramp here. Thus, the cart also doesn't need to "climb" out of the
hole, it just needs enough forward motion to roll to the next tile.

A cart moving slowly enough will pick up water/magma from a 7/7 tile;
the speed imparted by a high-speed roller is just low enough. Dwarven
pushes have the advantage that they "teleport" the cart to the middle
of the first pushed-to tile, which makes them the fastest loading
event. They're decidedly less automatable, though. There's no need to
engrave a corner into the pond tile, a straight fake ramp works better.

Bodycount: nothing new! Well, one diagonal vs. roller test ended up
giving a dog a bruised stomach. Big deal, I don't really count dogs
if they don't end up in multiple parts, like the puppy that during
the last round teleported its torso through a wall while leaving all
its limbs on the other side. The highly irresponsible flying minecart
test, however, didn't cause any harm at all.



Lesson Seven: Pathing across levels
===================================

Pathing on flat floor is easy enough: only corners matter. It's not
quite so easy when minecart paths go to different z-levels, either up
or down.

Getting a cart to move upwards is easy enough - just offer it a track
ramp. Carts will not go up ramps without engraved track, and they
will not reliably go up "false" ramps (i.e. ramps which don't
accelerate/decelerate carts). You'll eventually want the cart to stop
going up, and there things can go awry. A cart moving up a ramp with
no closed ceiling (or building) immediately above the exit tile may
get airborne. The speed from a highest-speed roller is enough for
this, but high-speed rollers or equivalent speeds like the
acceleration from a single down ramp can suffice, too. An airborne
cart will not be in contact with the floor underneath it and will
thus not care about track corners, rollers or track stops on that tile.

A closed ceiling or building (bridge, hatch cover etc.) above the
exit tile will make the cart behave and stick to the floor,
regardless of its speed - a high-speed roller cart will be reined in
by a ceiling just the same as a highest-ramped-speed cart or a
supercharged cart.

If there's open ceiling above the exit tile, a cart can still be
ruled in by a *functional ramp* on the exit tile.
::

    z+0              z+1, a)    b)    c)    d)
    ######                 #     #     #     #
    ▲▲▲▲▲▲▲#▲══           ▼═▼   ▼▲▼   ▼▲▼   ▼▲▼

    ######                 #     #     #     #
    ╚╚╚╚╚╚═#═══           ▼═▼   ▼╚▼   ▼║▼   ▼╝▼

Cart comes from the west, accelerated by a series of impulse ramps,
then goes over an up ramp.
a) - no ramp (can be smoothed floor instead of straight track): cart
goes into flight, several z-levels up.
b), c), d): cart goes down the ramp to the east and follows the track.
Notably, the orientation of the ramp on the top tile doesn't matter,
it just needs to be a legal ramp. Carts can be made to "level out"
via ramp, but as seen here, they can also be forced down an adjacent
ramp this way.

So, if you send a cart up several levels to the surface and don't
want it to go flying, put a ramp on the exit tile.

When you want a cart to enter a downward path, there are a few issues
and solutions, as well:

A cart coming upon a hole in the ground will by default just jump
across it. If the cart moves at a speed of at least 1/5th of a tile
per step, it can jump over one tile of open space and continue moving
on flat floor on the other side. A dwarven push or low-speed roller
are enough for this purpose. A peculiar issue was found with dwarven
pushes: a dwarf pushing a cart from right next to a hole in the floor
cannot move the cart across. It will collide with the hole's edge and
fall down into the pit. This seems to happen because the push
"teleports" the cart to the middle of the adjacent tile, without
giving it the "lift" gained by a jump. If there's one tile of
"buffer" between the dwarf and the hole, the cart jumps just fine.

If there is a ramp in a hole (ordinary floor ramp or track ramp, both
are recognised), a cart will treat the hole as an appropriate pathing
destination and will directly move into it (i.e. without spending
time in the "open space" above the hole) *as though it were rounding
a "downward" track corner*. Carts moving at derail-capable speeds
will not enter a downward ramp, they'll jump over the tile and
continue beyond it. In addition, the tile before the ramp must be a
"track" tile - either engraved track or a bridge. Carts coming from
ordinary floor will jump, regardless of their speed.

As noted above, however, a cart coming *from* a legal track ramp (any
orientation!) will enter a downward track ramp just fine. This allows
sending very fast carts down ramps simply by putting an impulse ramp
before the actual ramp entrance::

    . #        #
    ══▲▼     ══╚▼

Other ramp orientations seem to work just the same, as long as
they're legal and don't open a diverging path. Ramps will *not* send
a cart into a hole that doesn't contain a ramp.


Lesson Eight: Meet the checkpoint bug
=====================================

Let's face the possibly most powerful feature/bug of minecarting.
Nope, not impulse ramps. For demonstration purpose, let's take two
sets of opposed ramps::

    a)        b)
    #▲═▲#     #▲▲#

    #═══#     #══#

Offer open floor above and to the sides.

Drop a cart onto one of the ramps via hatch. In each case, the cart
will start out by rolling along a ramp for five steps.

In a), the cart will then pass over the flat tile *in a single step*,
spends eight steps on the opposing ramp, rolls across the middle tile
in a single step again, spends seven steps on the first-touched ramp,
then across in a single step etc., until after a few iterations it
sits still in the middle tile.

In b), the cart goes onto the opposing ramp, passes over it *in a
single step*, goes to the tile above and to the side, passes over
that tile in a single step again and then moves off at about 1/5 tile
per step (~19 000 speed). If you offer no exit, the cart will bounce
between the two ramps forever, spending eight steps on each. You can
temporarily stop it by blocking the opposite ramp with another
minecart, but as soon as one cart is removed, the remaining cart
starts bouncing again.

What we're seeing is an artefact of the game having to switch
distance calculations as soon as ramps get involved. The upshot is that

a) if track changes from flat track to a ramp, the cart *must* step
onto the new ramp tile. No matter how fast the cart is, the tile
cannot be skipped. I'll call this a "half checkpoint".
b) if track changes from a type of ramp to *anything else*, the
"changed" tile cannot be skipped and the cart will spend *exactly*
one step on it, regardless of its speed (as long as speed is above
zero). Finally, the last speed increment the cart received on the
ramp is erased, presumably by applying equivalent acceleration in the
opposite direction. I'll call this a "full checkpoint".

"Anything else" notably means that checkpoints happen whenever the
cart passes from a ramp to a *different* ramp, i.e. a ramp with a
different slant (accelerate-to direction), and when passing to a
non-ramp tile, preferably flat track.

The biggest effect here is that **checkpoints effectively divorce the
rate of movement from internal speed of the cart.**

Cart propelled by a single ramp (about 1/3 tile per step) going over
checkpoint? Spends exactly one step there. Cart propelled by maximum
number of ramps (about 2,5 tiles per step) crossing checkpoint?
Spends exactly one step there. In fact, if a cart is moving along a
ramp- and corner-heavy track and crosses one tile each step, it's
almost a given that you're dealing with chained-up checkpoints.

Simple example::

    ##########      ##########
    ═▲═▲═▲═▲═▲      ═╚═╚═╚═╚═╚

A cart going in at sufficient speed (must be ~72 000+) will cross
this track spending one step on each tile and will come out on the
east at almost exactly the speed it went in. This holds both for a 72
000 speed and a 265 000 speed cart, they'll move at the same rate
through this track, they'll only lose the speed for normal track
friction but the slower cart will also not accelerate. Their actual
internal speeds will only again assert themselves after the cart left
this track section.

This happens because each impulse ramp is a half and each flat tile a
full checkpoint. The slower cart is just fast enough to make it off
the ramp in a single step (apparently a cart moves its full movement
rate "into" a half-checkpoint (but not past it when moving faster
than one full tile per step): a fast-enough cart makes it to just
past the half-way point of the ramp upon entering, and just past the
tile's "exit" on the very next turn). PS: I haven't checked this
exact design, but as long as incoming speed is at least 80.000, this
thing should work the same way *in both directions* - carts going
"with" the impulse ramps won't accelerate, and those going "against"
them won't slow down.

Let's look at the first example with the double-ramp again and see
what happens by checkpoint rules, dropping the cart onto the western
ramp:

-cart goes "down" ramp to the east, picks up 25 000 speed.
-cart enters ramp slanting west - checkpoint: accelerate 5000 to the
west (compensating for last step of acceleration), go to end of tile
-cart "accelerates" west by 5000 on the west-slanting ramp, has 15
000 speed left to cross the threshold to the next tile, thus reaches
flat tile above and to the east - checkpoint: accelerate 5000 east
(compensating for westward acceleration), go to end of tile
- cart keeps moving on flat track to the east, now with normal
distance calculations so it takes five steps per tile again.

Why the weird "accelerate backwards on the checkpoint" thing? Because
in example a), the cart actually stops. It also explains why the
highest speed i've got through ramps (measuring actual track covered)
is not 270.000 but 265.000.

For a clearer example::

    #▲+ ═     #═══

:``+``:     lever-operated door

Station a cart on the ramp, then open the door. The cart instantly
rolls onto the flat tile *and stops there*. This is, it picked up
speed from the ramp, used that speed to pass over to the flat ground,
but had no speed left thereafter (or it'd have moved to the next tile
east on the next step). I interpret this so that the cart actually
loses its speed after taking the move. Other evidence supports the
interpretation.

This bug allows deriving speed from pits in the floor and moving
carts up levels with ease. It's the actual power behind the "impulse
elevator" shown on the wiki. WanderingKid's elevator uses impulse
ramps to gain speed, but checkpoints to go up levels.

I'll leave you with this for now. More to come.

Bodycount: kitty!

Someone's pet cat wandered into the cyclotron. It's the only
contraption that has caused any real damage so far, and the only
dwarf who was hurt remains the spinner/leatherworker who tried to
"clean" puppy blood out of it while it was spinning.



Lesson Nine: Practical implications of the checkpoint bug
=========================================================

The checkpoint bug affects all manner of minecart constructions, as
soon as ramps get involved. For a start, let's look at the lowly
single-ramp cyclotron::

    #####      #####
    #╔═╗#      #╔═╗#
    #╚▲╝#      #╚╔╝#
    #####      #####

Cart cycles counter-clockwise and its speed oscillates somewhere
between 70,000 and 80,000.

It won't go any faster, ever, although one step of ramp acceleration
gives 4900 speed while four corners and, say, seven steps of movement
cost no more than 4070. Evidently, if the cart spends only one step
on the ramp, this acceleration is eaten up by the checkpoint
compensation when moving off the ramp to level floor. It'll only
really pick up speed when it spends at least two steps on the ramp
and it must be slower than ~72.000 for this to happen.

Indeed, the cart cycles at an oscillating speed: it goes five rounds
at eight steps each (spending two steps on the ramp each time) and
seven steps in the sixth round (spending only one step on the ramp).

For speed to keep building up, you need an unbroken stretch of three
impulse ramps: due to the greater length of ramp tiles, the maximum
speed available through ramps (270.000) is just less than two ramp
tiles per step, so a cart will always spend at least two consecutive
steps on the three-ramp stretch. Such a three-ramp cyclotron is
enough to achieve maximum ramp speed.

When moving a cart laterally onto an impulse ramp track, the
checkpoint effect can be used to prevent diagonal movement.

Throwing a cart directly into a sideways impulse ramp::

    a)                   b)
    ####      ####      ####      ####
    ▲▲▲▲      ╝╝╝╝      ▲▲▲▲      ╝╝╝╝
       ║         ║         ▲#        ╚#

from the south like in a) will have the cart accelerate to the west
on top of a pre-existing and lingering northward speed. It'll either
bump into the wall and temporarily stop or exit the impulse stretch
on a diagonal trajectory. Sending it through an immediately adjacent
impulse ramp lets it pass right through the first ramp of the
acceleration stretch via checkpoint effect, stopping it against the
wall and cancelling the northward speed instantly, so that it can
accelerate west on a straight course.

Of course, others have, often unknowingly, used checkpoint effects in
their constructions. Take the "impulse elevator" on the wiki:

    ####      ##╗#      ####
    ▼╔╝#      ##╚#      ╔╝▼#
    ▼###      #▼▼#      ##▼#

All track on ramps, going up from left to right.

Looking at the thing in action, we'll see that the cart moves at a
rate of exactly one tile every step until after five levels or so it
stops, rolls back from an "up" ramp in eight turns, spends another
eight steps on the ramp behind, then starts going at the previous
rate for another five levels. Clearly, this means that the cart moves
at one ramp-length per step, i.e. 140.000 speed, right?

Haha, of course not. It's checkpoints all the way up. The cart
hiccups and stops not because it's too fast, but because it ran all
out of speed and had to checkpoint-cheat itself some new steam.

Observe the ramp slants in the example above: E, W, N, S, W, E. Slant
changes every tile, thus every tile is a full checkpoint. The
checkpoint bug runs the cart up at a rate of one ramp every step,
until speed falls to zero. At that point, the cart makes it onto the
next tile (and technically all the way "up" on it) but has no more
speed to make it to the next tile (up), so it stays on the ramp and
accelerates there for the full eight steps. This moves it back to the
last (opposing) ramp, which it again fully crosses, but here it bumps
against a wall and accelerates all the way forward again. With the
shiny new 35.000 speed, it can take the up checkpoint and have speed
leftover to keep moving.

It's peculiar that this thing loses speed so quickly - it appears to
burn through its store of ~35.000 speed points in five levels,
although it should only lose 1.000 speed per level for the corner.
It's almost as if there's something fishy with corner ramps that
enforces a higher speed loss.

Another ramp spiral was invented by WanderingKid and has the
advantage of doing without the annoying back-and-forth every few
levels. The cart in that design just keeps going. Let's check it out::

    z+0   z+0, track    z+1   z+1, track    z+2 (z+0 mirrored)
    ####      ####      ####      ####        ▲▲╗#
    ▼###      ▼###      ##▲#      ##║#        ##▼#
    ╚▲▲#      ╚╔╝#      ##▼#      ##▼#        ####
    ####      ####      ####      ####        ####

This one surprised me at first, because it "somehow" manages to send
a cart up *two* levels, seemingly with a single checkpoint. Spoiler:
of course it's two checkpoints.

The east-pointing ramp on z+0 works as a proper speed-granting
impulse ramp here, because the cart enters it from flat floor, not
from another ramp. When I tried it out, the cart spent two or three
steps (repeating pattern of different rates, like in the cyclotron
above) on the ramp each time, so there was always speed gained here.
The corner up ramp is, unsurprisingly, a checkpoint, the cart passes
it in a single step. What I hadn't fully understood yet - the next,
straight, ramp is *also* a checkpoint, because the slant of ramps
changed, from west to south. The flat corner is yet another full
checkpoint, which doesn't really matter in and of itself, but the
fact that it's normal floor and not a ramp saves the following
impulse ramp from being a full checkpoint, so it can actually do its
impulse work.

Let's crack an old puzzle next: the 2x2 ramp spiral. It's a
notoriously ill-behaved contraption, carts keep stopping on it for no
discernible reason. At the same time, it looks so simple::

    ####        ####        ####        ####        ####
    #╔╗#        #▲▼#        #▼##        ####        ##▲#
    #╚╝#        ####        #▲##        #▼▲#        ##▼#
    ####        ####        ####        ####        ####

Spread over four levels, one corner on each level, each leading into
the next. Throwing a cart down such a spiral lets the cart start
going at one ramp per step, but after five, it stops, starts again,
goes another five, stops again etc.

Ho hum. Is it picking up too much speed? I put a few stone blocks
into a cart and sent it down there. The blocks stayed in the cart.
Well, it was moving at one ramp per step, so it was probably
checkpoint-hopping again. Makes sense, of course, since ramp slant
changes on every tile. So it probably stopped simply because its
speed dropped to zero. Still, a cart going *down* a ramp spiral and
losing speed? I revved up a cart in the trusty cyclotron and sent it
down a nice long spiral. It kept going and emerged 21 z-levels below
- at 130.000 speed. The cart was definitely losing ~6.000 speed on
every ramp, a few more tests confirmed this. In fact, a downward
spiral slows down a cart exactly as much as an *upward* spiral.

Inspired by :forums:`rhesusmacabre's long table
<125679.msg4223763#msg4223763>`, I built a few simple test spirals,
and yes, I was getting checkpoint-movement up the spirals, over nice
large numbers of levels, and my eyeballed speed loss of 6.000 per
level seemed to work out.

I definitely needed to crack the puzzle of corner ramps. But first,
some light entertainment.

Since different-slant ramps work as checkpoints for each other and
the compensating speed effects cancel out their acceleration,
shouldn't it be possible to send *reallllly slow* carts along a line
of impulse ramps, bouncing one ramp per step until ramps stopped and
the actual speed reasserted itself? I built a line of 24 impulse
ramps stretching from east to west and with wall to the south,
alternating between NS and SW every step, hatch-dropped a minecart on
the easternmost (SW) ramp and watched it. Yep, cart rolled down the
usual five steps, then went forward at a rate of one ramp every step
over the whole line, and once it emerged from the ramp line, it
crawled along at the actual ~19.000 speed (five to six steps used for
every tile).

But shouldn't the northward acceleration, although it's cancelled
instantly, result in a minor northward displacement on every NS ramp
that should eventually push the cart past the northern border? I
expanded the row to ~40 ramps, and sure enough, after the thirtieth
ramp (15th NS ramp) the cart moved off the ramp-line to the north. To
make sure it's really displacement and not northward velocity, I
covered ten ramps with a bridge so that north-pointing ramps #15 to
#19 were obscured. The cart moved over this stretch without
diverting, went over the SW ramp directly behind the bridge - and
made its step to the north when it checkpoint-passed the NS ramp
behind it, the twentieth northward ramp in the line, but this time,
the fifteenth touched by the cart.

Fifteen pushes of presumably 4900 distance units give 73500 distance
units, just over half the assumed length of a ramp (140.000 or so - I
don't know the exact number Toady uses). Enough to move over the
border to the next tile when starting in the middle of a tile. Seems
that it works out.

Of course, northward displacement can simply be compensated by
southward displacement. I dug out a track all across the embark
(normal embark, so just 190ish tiles) and carved out a nice stretch
of 160ish alternating track ramps. First ten "forward" ramps
interspersed with 10 North-slanted ramps, then (changing the adjacent
wall) 20 forward with 20 south-slanted, then another 20/20 stretch
forward/north etc.., finally a bit of flat track leading into a
little loop at the far end. The cart was dropped in via hatch as
usual and moved all across the embark without falling off the row,
passing one tile per step as long as it was bouncing over ramps,
while the flat track at the end demonstrated its internal speed
remained at the original 19.000. The loop itself contained a nice
juicy acceleration rail, increasing speed on the route back to
~120.000, and the cart went back all the way, once again at 1
tile/step externally, unfazed by the 80 "opposing" impulse ramps.


Lesson Ten: Corner ramps
========================

Corner ramps had been bugging me for a while now, so I built a simple
test rig::

    above        below
    #▼═════      ▲#
                 ║

With a SE (``╔``) track ramp.

First of all, send a cart up the ramp: no matter what I do, when
given straight track, the cart will move diagonally and the first
step aside happens after 11 steps, adequate for a lateral component
of just under 5000 speed, i.e. the acceleration gained by a single
step on a ramp. Curiosly, while the corner should convert all
south-to-north velocity of the cart into west-to-east velocity and
the ramp slants to the south, the aberration was to the north.

Unsurprisingly, the culprit is the checkpoint bug: almost always, a
corner ramp passed upward leads to a checkpoint - the ramp slants
south and the most sensible connections above are flat track or a
west-slanting ramp. Thus, the checkpoint effect is applied: a) the
next tile is crossed in a single step. b) compensative acceleration
is applied *which is opposed to the ramp's slant*. That's it - the
corner outputs the cart on a pure-eastward path but *then* the
"compensating" speed is applied and gives the much-abhorred
diagonality to the cart.

So, putting it in numbers: when a cart checkpoint-hops up a corner
ramp, it loses 5000 from its original incoming speed to ramp
acceleration, loses another 1000 for the corner, and the checkpoint
doesn't "refund" the 5000 speed but rather (since it's applied after
the corner turn) applies it as lateral/diagonal speed towards the
"outside" of the corner. **A cart going up a corner ramp at any speed
loses 5000x(time on ramp)+1000(corner penalty) speed, and gains 5000
lateral.**

That was the easy part.

Let's send a cart *down* the ramp now.

If the cart is fast enough (about 45.000 minimum), it takes the
corner and continues perfectly straight in the corner's exit
direction, with a speed loss of ca. 6000. I tried it with a
highest-speed roller, and the cart going through a corner ramp would
emerge at 44.000 speed, while a cart going down a straight ramp would
gain ca. 5000 and emerge at 55.000.
Once again, we're dealing with checkpoints and a corner, so let's
step through it:
On the corner ramp, all acceleration goes to the side, it doesn't
accelerate the cart in its original travel direction. Here, we have a
cart going west, which is accelerated south. Unsurprisingly, the
westward speed isn't increased by this event. At the *end* of the
turn on which the cart wants to leave the tile, the corner comes into
play, converts all westward to southward motion overwriting the
extant southern vector, the acceleration gained is therefore lost. On
the next step, the cart reaches a checkpoint and to compensate, it is
"accelerated" 5000 units to the north. Summa: all southward
acceleration was ignored because of the corner, but the compensative
deceleration still applies, so the cart loses 5000 speed, plus 1000
for the corner. 6000 in total.

What's that about a 45.000 minimum speed? Ah well, losing speed on a
down ramp is not the weirdest thing here. A cart moving at lower
speeds than that is liable to malfunction even more blatantly. A cart
propelled by a dwarven push emerges at a
mostly-south-and-slightly-west trajectory, going off the straight
line after two tiles. A cart entering the ramp at between 30.000 and
40.000 speed leaves at an almost-45° angle, a very sharp diagonal. It
took me quite a while to think up a solution for that one, but I
think it works out:

Corners are only checked when a cart tries to leave a tile, and they
only check whether the side opposed to the "border" over which the
cart is trying to leave is connected. In understandable: if a cart on
a southwest heading is trying to leave a tile going over the western
border of the tile, the pathing algorithm checks if the tile
underneath is a track corner with an eastern connection. If yes, the
cart is turned around towards the corner's other connection. If the
cart tries to leave over the southern border, the algorithm checks
whether the tile is a north-connected corner. If the checked border
is not connected or if the tile isn't a corner, the cart leaves
normally and its speed(s) is (are) unchanged.

So what happens with these slower carts is this: they move so slowly
to the west and thus pick up so much southward speed on the ramp,
that the cart's "exit" direction from the tile is south (or SW (??)
in the case of the somewhat-slow cart), and thus the corner has no
power over them. Consequently, they move off on their screwy diagonal
course.

**A cart going down a corner ramp, properly taking the corner, loses
5000(checkpoint compensation)+1000 (for the corner)=6000 speed,
independent of lingering time on the ramp.**

If time on the ramp is too long, the corner starts checking the wrong
(unconnected) side of the tile when the cart tries to leave and no
longer applies. In that case, the output trajectory is purely
diagonal, presumably incoming speed in the incoming direction +
5000x(lingering time minus one) lateral (towards ramp slant), no
corner penalty.

Bodycount: nothing new, no new tests required. I just wrote up what I
had worked out previously.

This concludes our course on Minecarts. Annotations, corrections,
claims of priority will be gracefully accepted and carefully
considered. Possibly. I've tried to link to sources and earlier
findings. I owe a large debt to other players for their research and
inspiring inventions.

