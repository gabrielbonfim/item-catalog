from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Category Soccer and Items
catSoccer = Category(name="Soccer")

session.add(catSoccer)
session.commit()

catSoccerItem1 = Item(name="Socks", description="""
The main job of socks is to support the shin guards. Staying in place is the
 most important element of any good-fitting sock. They should neither slip
 down, nor impede circulation. You generally get what you pair for, so buy the
 best pair your budget can afford.
""", category=catSoccer)

session.add(catSoccerItem1)
session.commit()

catSoccerItem2 = Item(name="Shirt", description="""
You might even say the goalkeeper is the distinguished member of the team. His
 or her shirt is going to look different from that of teammates. Usually it's
 a different color, and is long-sleeved to prevent injury.
""", category=catSoccer)

session.add(catSoccerItem2)
session.commit()

catSoccerItem3 = Item(name="Gloves", description="""
Padded gloves prevent injury resulting from catching the ball. It's best to
 choose a pair that is durable and flexible. Today's gloves are designed a
 little stiff for added protection to the fingers. Parents of children in the
 goalkeeper position should be looking for a glove that offers maximum
 protection from finger injury. And as the game is often played in wet
 conditions, look for a durable pair of protective, water-resistant gloves.
 Goalkeeper gloves should be comfortable, good-fitting, and offer great grip.
""", category=catSoccer)

session.add(catSoccerItem3)
session.commit()

# Category Basketball and Items
catBasketball = Category(name="Basketball")

session.add(catBasketball)
session.commit()

catBasketballItem1 = Item(name="Shoes", description="""
One needs specialized shoes when playing basketball. It should be able to give
 better support to the ankle as compared to running shoes. The basketball
 shoes should be high-tipped shoes and provide extra comfort during a game.
 These shoes are specially designed to maintain high traction on the
 basketball court.
""", category=catBasketball)

session.add(catBasketballItem1)
session.commit()

catBasketballItem2 = Item(name="Backboard", description="""
The backboard is the rectangular board that is placed behind the rim. It helps
 give better rebound to the ball. The backboard is about 1800mm in size
 horizontally and 1050mm vertically. Many times, backboards are made of
 acrylic, aluminum, steel or glass.
""", category=catBasketball)

session.add(catBasketballItem2)
session.commit()

catBasketballItem3 = Item(name="Uniforms", description="""
When one starts coaching a basketball team, the most important requirement for
 a team is to have a uniform. This helps one differentiate teams from one
 another. A uniform consists of a jersey (shirt), shorts, numbers on the front
 and back of the shirts for identification.
""", category=catBasketball)

session.add(catBasketballItem3)
session.commit()

# Category Baseball and Items
catBaseball = Category(name="Baseball")

session.add(catBaseball)
session.commit()

catBaseballItem1 = Item(name="Bat", description="""
A rounded, solid wooden or hollow aluminum bat. Wooden bats are traditionally
 made from ash wood, though maple and bamboo is also sometimes used. Aluminum
 bats are not permitted in professional leagues, but are frequently used in
 amateur leagues. Composite bats are also available, essentially wooden bats
 with a metal rod inside. Bamboo bats are also becoming popular.
""", category=catBaseball)

session.add(catBaseballItem1)
session.commit()

catBaseballItem2 = Item(name="Batting gloves", description="""
Gloves often worn on one or both hands by the batter. They offer additional
 grip and eliminate some of the shock when making contact with the ball.
""", category=catBaseball)

session.add(catBaseballItem2)
session.commit()

catBaseballItem3 = Item(name="Batting helmet", description="""
Helmet worn by batter to protect the head and the ear facing the pitcher from
 the ball. Professional models have only one ear protector (left ear for
 right-handed batters, right ear for lefties), amateur and junior helmets
 usually have ear protectors on both sides, for better protection from loose
 balls, and to reduce costs to teams (all players can use the same style of
 helmet).
""", category=catBaseball)

session.add(catBaseballItem3)
session.commit()

# Category Frisbee and Items
catFrisbee = Category(name="Frisbee")

session.add(catFrisbee)
session.commit()

catFrisbeeItem1 = Item(name="Discs", description="""
In order to play ultimate frisbee you a need a frisbee (makes sense). The
 regulation size for a frisbee is 175 gram disc.
""", category=catFrisbee)

session.add(catFrisbeeItem1)
session.commit()

catFrisbeeItem2 = Item(name="Cones", description="""
In order to properly play ultimte frisbee you need to label the endzones.
 The endzones are exactly. If you don't have cones, you can use shoes if
 you don't have cones with you.
""", category=catFrisbee)

session.add(catFrisbeeItem2)
session.commit()

catFrisbeeItem3 = Item(name="Shoes", description="""
this one is a matter of personal preferance. some people like to play ultimate
 in running shoes, cleats, or play barefoot. i like to play barefoot. I know
 that most people perfer to play in shoes, but no matter how you play, you
 want some sort of protection on your feet.
""", category=catFrisbee)

session.add(catFrisbeeItem3)
session.commit()

# Category Snowboarding and Items
catSnowboarding = Category(name="Snowboarding")

session.add(catSnowboarding)
session.commit()

catSnowboardingItem1 = Item(name="Snowboards", description="""
The boards used in freestyle events (halfpipe, slopestyle, big air) are short
 to allow for tricks, wide to increase balance, and flexible to allow the
 boarder to ride in either direction. The nose and tail of the board are both
 curved upwards to allow take-off and landing in both directions.

Parallel giant slalom boards are stuff and narrow, making them ideal for
 maneuvering through gates at high speeds. They are generally longer than a
 normal snowboard and feature a square back and low nose.

The boards used in snowboard cross are somewhat of a mix between the freestyle
 and alpine snowboards described above, though they usually look more like
 freestyle boards. Snowboard cross boards are long for carving and stiff for
 stability.
""", category=catSnowboarding)

session.add(catSnowboardingItem1)
session.commit()

catSnowboardingItem2 = Item(name="Boots", description="""
Most freestyle snowboarders use soft boots, which allow a large range of
 motion and offer foot and ankle support. Alpine snowboard boots also provide
 foot and ankle support, but have a hard plastic exterior.

Boots used in snowboard cross tend to be more of a hybrid - they are stiffer
 than freestyle boots, but not as hard as alpine boots. Some snowboard cross
 racers do opt to wear hard racing boots though.
""", category=catSnowboarding)

session.add(catSnowboardingItem2)
session.commit()

catSnowboardingItem3 = Item(name="Bindings", description="""
Freestyle snowboarders use flexible bindings to attach their feet to their
 board. In this scenario, the rider is using straps to secure their boots.
 Alpine snowboard bindings are similar to those used in Alpine skiing - the
 hard boot is firmly locked to the board.

In snowboard cross, the type of bindings used depends on the boot. A racer
 who uses soft boots would use flexible bindings, while a racer with hard
 boots would use bindings that secure them firmly to the board.
""", category=catSnowboarding)

session.add(catSnowboardingItem3)
session.commit()

# Category Rock Climbing and Items
catRockClimbing = Category(name="Rock Climbing")

session.add(catRockClimbing)
session.commit()

catRockClimbingItem1 = Item(name="Climbing Helmet", description="""
When climbing outdoors, you should always wear a helmet made specifically for
 climbing. Climbing helmets are designed to cushion your head from falling
 rock and debris, and some (though not all) are designed to provide protection
 in the case of a fall. They are generally not worn in a climbing gym since
 it's a controlled environment.

A helmet should feel comfortable, fit snugly but not too tight and sit flat on
 your head. Helmets usually have a hard protective shell and an internal
 strapping system.
""", category=catRockClimbing)

session.add(catRockClimbingItem1)
session.commit()

catRockClimbingItem2 = Item(name="Climbing Harness", description="""
Your harness allows you to tie into the rope securely and efficiently. All
 harnesses have two front tie-in points designed specifically for threading
 the rope and tying in, one at the waist and one at the leg loops. Generally
 the tie-in points are different than the dedicated belay loop. Buckling your
 harness correctly is essential for safety.
""", category=catRockClimbing)

session.add(catRockClimbingItem2)
session.commit()

catRockClimbingItem3 = Item(name="Carabiners", description="""
These strong, light metal rings with spring-loaded gates connect the climbing
 rope to pieces of climbing protection such as bolts, nuts and camming
 devices. They are also used to make quickdraws (used in lead climbing) and to
 rack (attach) your gear to the gear loops on your harness.

For most beginners, the first carabiner you'll buy is a locking 'biner
 designed to be used with a belay device.
""", category=catRockClimbing)

session.add(catRockClimbingItem3)
session.commit()

# Category Foosball and Items
catFoosball = Category(name="Foosball")

session.add(catFoosball)
session.commit()

catFoosballItem1 = Item(name="Foosball Rods", description="""
Rods have a huge impact on the speed of the game. Foosball rods are an
 expensive part of the table and some manufacturers try to cut corners on
 their rods because it can be easily overlooked by rookie foosball players.
 Some tables come with heavy rods that make the game slow and sluggish. This
 will hinder your ability to perform shots because it will be hard to maneuver
 the rods laterally. All quality tables are made with hollow light-weight,
 chrome rods that provide a smooth glide back and forth between the bearings
 so you can obtain maximum ball control and shot performance.
""", category=catFoosball)

session.add(catFoosballItem1)
session.commit()

catFoosballItem2 = Item(name="Foosball Bearings", description="""
Foosball bearings are the part of the table where the rods go through the
 holes in the table. Bearings allow for less friction when moving the rods
 in and out in order to slide the rods in and out of the table with ease. This
 is a part overlooked by many players when shopping for a table. Quality
 bearing parts allow for a smoother gliding of the rods.
""", category=catFoosball)

session.add(catFoosballItem2)
session.commit()

catFoosballItem3 = Item(name="Foosball Bumpers", description="""
Foosball bumpers are a part typically made of black rubber and they provide a
 barrier or a cushion between the wall of the table and the man. However,
 there are some lower-end tables that are made with spring bumpers that allow
 you to move the man closer to the wall. Rubber bumpers provide the proper
 spacing for the movement of the foosball men on the table.
""", category=catFoosball)

session.add(catFoosballItem3)
session.commit()

# Category Skating and Items
catSkating = Category(name="Skating")

session.add(catSkating)
session.commit()

catSkatingItem1 = Item(name="Shock Pads", description="""
Shock pads are made of polyurethane and rubber. They are very similar to
 risers but vary in the fact that their sole purpose is to cushion the board
 from the trucks. Since the trucks are metal and the board wood, whenever the
 board hits the ground after doing a trick, the energy goes through the truck
 to the board this has caused boards to crack split or even break in half
 and shock pads were created to prevent this.
""", category=catSkating)

session.add(catSkatingItem1)
session.commit()

catSkatingItem2 = Item(name="Sliptape", description="""
Sliptape is a clear piece of self-adhesive plastic that sticks to the
 underside of a deck. It helps protect the board's graphics and allows the
 board to slide more easily. Another name for this is everslick.
""", category=catSkating)

session.add(catSkatingItem2)
session.commit()

catSkatingItem3 = Item(name="Lapper", description="""
A lapper is a plastic cover that is fastened to the rear truck and serves to
 protect the kingpin when grinding. It also prevents hang-ups by providing a
 smoother transition for the truck when it hits an obstacle or a metal pipe or
 round bar.
""", category=catSkating)

session.add(catSkatingItem3)
session.commit()

# Category Hockey and Items
catHockey = Category(name="Hockey")

session.add(catHockey)
session.commit()

catHockeyItem1 = Item(name="Stick", description="""
Your hockey stick is like your weapon on the battlefield. After choosing the
 most suitable hockey stick for yourself, you will learn to use it and after a
 while, be so comfortable with it that it becomes a part of you.
""", category=catHockey)

session.add(catHockeyItem1)
session.commit()

catHockeyItem2 = Item(name="Mouth Guard", description="""
Investing in a mouth guard is a good idea because you wouldn't want to burn a
 hole in your wallet, paying for your dental treatment should a ball hit you
 in the face.
""", category=catHockey)

session.add(catHockeyItem2)
session.commit()

catHockeyItem3 = Item(name="Shin Guards", description="""
When you play field hockey, your shins take the most beating from balls and
 sticks. It is thus important for you to protect your shins from getting
 bruised.
""", category=catHockey)

session.add(catHockeyItem3)
session.commit()
