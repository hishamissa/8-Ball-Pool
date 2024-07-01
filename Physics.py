import phylib;
import os;
import sqlite3;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
                      "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """</svg>\n"""

FRAME_INTERVAL = 0.01 # NEW FOR A3

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    # add an svg method here
    def svg(self):
        ball_colors_new = {
        0: "WHITE",      # Cue ball
        1: "YELLOW",     # 1-ball
        2: "BLUE",       # 2-ball
        3: "RED",        # 3-ball
        4: "PURPLE",     # 4-ball
        5: "BLACK",     # 5-ball
        6: "GREEN",      # 6-ball
        7: "BROWN",      # 7-ball
        8: "ORANGE",      # 8-ball
        9: "LIGHTYELLOW",     # 9-ball
        10: "LIGHTBLUE",      # 10-ball
        11: "PINK",       # 11-ball
        12: "MEDIUMPURPLE",    # 12-ball
        13: "LIGHTSALMON",    # 13-ball
        14: "LIGHTGREEN",     # 14-ball
        15: "SANDYBROWN",     # 15-ball
        }
        color = ball_colors_new[self.obj.still_ball.number]
        # Using the ball number to choose a color, modulo ensures it wraps around if more than 16 balls
        # color = BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)]
        # Generating SVG string for a still ball
        if self.obj.still_ball.number == 0:
            return f'<circle id="cue-ball" cx="{int(self.obj.still_ball.pos.x)}" cy="{int(self.obj.still_ball.pos.y)}" r="{int(BALL_RADIUS)}" fill="{color}" />\n'
        else:
            return f'<circle cx="{self.obj.still_ball.pos.x}" cy="{self.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="{color}" />\n'

################################################################################

class RollingBall( phylib.phylib_object ):
    def __init__( self, number, pos, vel, acc):
        phylib.phylib_object.__init__( self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0)
        self.__class__ = RollingBall

    def svg(self):
        color = BALL_COLOURS[self.obj.rolling_ball.number] # % len(BALL_COLOURS)]
        # Generating SVG string for a rolling ball
        return f'<circle cx="{self.obj.rolling_ball.pos.x}" cy="{self.obj.rolling_ball.pos.y}" r="{BALL_RADIUS}" fill="{color}" />\n'

################################################################################
        
class Hole( phylib.phylib_object ):
    def __init__( self, pos):
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HOLE, 0, pos, None, None, pos.x, pos.y)
        self.__class__ = Hole

    def svg(self):
        # Generating SVG string for a hole, which is always black
        return f'<circle cx="{self.obj.hole.pos.x}" cy="{self.obj.hole.pos.y}" r="{HOLE_RADIUS}" fill="black" />\n'

################################################################################
        
class HCushion( phylib.phylib_object ):
    def __init__( self, y):
        phylib.phylib_object.__init__( self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y)
        self.__class__ = HCushion

    def svg(self):
        # Y position adjustment based on the cushion's Y position
        y = -25 if self.obj.hcushion.y == 0 else 2700
        return f'<rect width="1400" height="25" x="-25" y="{y}" fill="darkgreen" />\n'

################################################################################
        
class VCushion( phylib.phylib_object ):
    def __init__( self, x):
        phylib.phylib_object.__init__( self, phylib.PHYLIB_VCUSHION, 0, None, None, None, x, 0.0)
        self.__class__ = VCushion

    def svg(self):
        # X position adjustment based on the cushion's X position
        x = -25 if self.obj.vcushion.x == 0 else 1350
        return f'<rect width="25" height="2750" x="{x}" y="-25" fill="darkgreen" />\n'

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        """
        Generates an SVG representation of the pool table and its objects.
        """
        svg_elements = [HEADER]  # Start with the HEADER

        for obj in self:  # Iterate over all objects in the table
            if obj is not None:
                svg_elements.append(obj.svg())  # Append the SVG string from each object

        svg_elements.append(FOOTER)  # Finish with the FOOTER

        # Concatenate all SVG elements into a single string and return
        return ''.join(svg_elements)
    
    # START OF A3:
    # SQL for storing tables, games, shots, players, etc
    # Written by Hisham Issa (hissa01@uoguelph.ca | 1194466)
    # Started March 4, 2023

    # New roll() function in Table class for A3 (given in A3 description)
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                        Coordinate( ball.obj.still_ball.pos.x,
                                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    # This helper method finds and returns the cue ball, which is the ball with number 0.
    def cueBall(self):
        for ball in self:
            if isinstance(ball, (StillBall, RollingBall)) and ball.obj.still_ball.number == 0:
                return ball
        return None  # If the cue ball is not found

#######################################################################################################

# A class representing a connection to a database that stores table information and tables
class Database:

    # Initialize a new Database instance.
    def __init__(self, reset=False):

        # Set the name of the database file to match phylib
        self.databaseName = 'phylib.db'
        
        # Check if the database reset clause is true and if the database exists
        if reset and os.path.isfile(self.databaseName):
            # If so, remove the current database
            os.remove(self.databaseName)

        # Establish connection to the database file. 'conn' short for connection
        self.conn = sqlite3.connect(self.databaseName)
        # Establish cursor to interact with the database
        self.cursor = self.conn.cursor() # Cursor

    # Creates the database with all the necessary tables to store information about the game if they don't exist
    def createDB(self):

        # Each row in this table represents a Ball at a specific instance in time. The same Ball at different points in time, 
        # and during different games will have multiple rows in this table.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS BALL ( 
                                    BALLID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    BALLNO  INTEGER NOT NULL,
                                    XPOS    FLOAT   NOT NULL,
                                    YPOS    FLOAT   NOT NULL,
                                    XVEL    FLOAT,
                                    YVEL    FLOAT 
                                );
                            """ )
        
        # Each row in this table represents a Table at a specific instance in time. The same Table at different points in time, 
        # during different shots and games will have multiple rows in this table.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TTable (
                                    TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    TIME    FLOAT   NOT NULL 
                                );
                            """ )

        # This table connects balls to their tables by joining the TABLEID of TTable with the BALLID of Ball
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS BallTable (
                                    BALLID  INTEGER NOT NULL,
                                    TABLEID INTEGER NOT NULL,
                                    FOREIGN KEY (BALLID) REFERENCES Ball,
                                    FOREIGN KEY (TABLEID) REFERENCES TTable 
                                );
                            """ )
        
        # Each row in this table represents a shot in a game of pool. Shots in order of increasing SHOTID
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Shot (
                                    SHOTID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    PLAYERID INTEGER NOT NULL,
                                    GAMEID   INTEGER NOT NULL,
                                    FOREIGN KEY (PLAYERID) REFERENCES Player,
                                    FOREIGN KEY (GAMEID) REFERENCES Game 
                                );
                            """ )

        # This table connects table snapshots to tables by joining the TABLEID of TTable with the SHOTID of Shot. 
        # TABLEIDs are assumed to be in chronological order of TABLEID's
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TableShot (
                                    TABLEID INTEGER NOT NULL,
                                    SHOTID  INTEGER NOT NULL,
                                    FOREIGN KEY (TABLEID) REFERENCES TTable,
                                    FOREIGN KEY (SHOTID) REFERENCES Shot 
                                );
                            """ )
        
        # Connects GAMEID's to GAMENAME's 
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Game (
                                    GAMEID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    GAMENAME VARCHAR(64) NOT NULL
                                );
                            """ )
        
        # This table connects PLAYERID's to GAMEID's and PLAYERNAME's
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Player (
                                    PLAYERID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    GAMEID     INTEGER NOT NULL,
                                    PLAYERNAME VARCHAR(64) NOT NULL,
                                    FOREIGN KEY (GAMEID) REFERENCES Game
                                );
                            """ )

        # Commit changes made by SQLite3 execution statements
        self.conn.commit()

    # This method queries the database for a table snapshot and all associated balls, 
    # then constructs a Table object with the state of the pool table at the given ID.
    def readTable(self, tableID):

        try:
            # Retrieve the time for the specified table ID, offset by 1 because SQL autoincrement
            # starts at 1 but tableID starts at 0.
            self.cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,))
            time = self.cursor.fetchone()
            
            # If theres no entry for the tableID, return None
            if not time:
                return None
            
            # Extract the time from the first column of the result
            time = time[0]

            # Create a new Table object and set its time that we just retrieved
            table = Table()
            table.time = time

            # Retrieve all balls from the given tableID
            self.cursor.execute("""
                SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                FROM Ball
                INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                WHERE BallTable.TABLEID = ?
                """, (tableID,))

            # Iterate through all the ball rows and create Ball objects
            for row in self.cursor.fetchall():
                ball_no, x, y, x_vel, y_vel = row

                # Determine if the ball is still or rolling based on velocity
                if x_vel is None and y_vel is None:
                    # Still balls have no velocity
                    pos = Coordinate(x, y)
                    ball = StillBall(ball_no, pos)
                else:
                    # Rolling balls DO have velocity
                    pos = Coordinate(x, y)
                    vel = Coordinate(x_vel, y_vel)

                    # Calculate the acceleration of the rolling ball the exact way as in A2
                    speed = (x_vel**2 + y_vel**2)**0.5
                    if speed > VEL_EPSILON:
                        acc_x = -(x_vel / speed) * DRAG
                        acc_y = -(y_vel / speed) * DRAG
                    else:
                        acc_x = acc_y = 0

                    acc = Coordinate(acc_x, acc_y)
                    ball = RollingBall(ball_no, pos, vel, acc)

                # Add the ball object to the table
                table += ball

            # Commit
            self.conn.commit()
            # Return the newly constructed table object
            return table
        
        except sqlite3.Error as error:
            # Safety net to catch SQL errors. Mainly for testing/debugging reasons
            print(f"An error occurred: {error.args[0]}")
            return None

    # This method inserts the current state of the table, including time and all ball positions and velocities,
    # into the database's TTable and Ball tables. It automatically generates IDs for the new table
    # and ball states and links them together in the BallTable relation.    
    def writeTable(self, table):
        # Insert the tables time into TTable and get the generated ID
        self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        tableID = self.cursor.lastrowid
        # print(tableID)

        # Iterate over all balls in the table
        for obj in table:
            # Check if the object is a StillBall or RollingBall
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                # Get ball number and position
                ballID = obj.obj.still_ball.number
                x_pos, y_pos = obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y
                
                # Get the velocity only from RollingBall's. StillBall velocity is None since they do not have one
                x_vel, y_vel = (None, None) if isinstance(obj, StillBall) else (obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y)

                # Insert the ball into the Ball table
                self.cursor.execute("""
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?)
                """, (ballID, x_pos, y_pos, x_vel, y_vel))

                # Get the generated ID for the new ball
                ballRowID = self.cursor.lastrowid
                # print(ballRowID)

                # Link the new ball with the new table in BallTable
                self.cursor.execute("""
                    INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?)
                """, (ballRowID, tableID-1))

        # Commit
        self.conn.commit()
        # Return the SQL adjusted table ID
        return tableID - 1

    # Method to simply commit the database connection and close it
    def close(self):
        self.conn.commit()
        self.conn.close()

    # Retrieves the game name and player names for a specific game ID.
    def getGame(self, gameID):
        try:
            # Retrieve the game name and player names using joins to link the game with players
            self.cursor.execute("""
                SELECT g.GAMENAME, p1.PLAYERNAME as player1, p2.PLAYERNAME as player2
                FROM Game g
                JOIN Player p1 ON g.GAMEID = p1.GAMEID
                JOIN Player p2 ON g.GAMEID = p2.GAMEID AND p2.PLAYERID > p1.PLAYERID
                WHERE g.GAMEID = ?
                """, (gameID-1,))
            gameIdentifier = self.cursor.fetchone()
            self.conn.commit()

            # Check if the game exists and return its details. If not, return None
            if gameIdentifier:
                # This will return a tuple with (gameName, player1Name, player2Name)
                return gameIdentifier
            return None
        
        except sqlite3.Error as error:
            # Safety net to catch SQL errors. Mainly for testing/debugging reasons
            print(f"An error occurred: {error.args[0]}")
            return None

    # Creates a new game entry in the Game table and player entries in the Player table
    def setGame(self, gameName, player1Name, player2Name):
        try:
            # Insert the game name into the Game table and get the new gameID
            self.cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
            gameID = self.cursor.lastrowid

            # Insert both plauers into the Player table with the new gameID    
            self.cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
            self.cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))

            # Commit
            self.conn.commit()

            # Return the new gameID
            return gameID
        
        except sqlite3.Error as error:
            # Safety net to catch SQL errors. Mainly for testing/debugging reasons
            print(f"An error occurred: {error.args[0]}")
            return None
        
    # Inserts a new shot entry into the Shot table for a given game and player.
    def newShot(self, gameName, playerName):
        # Lookup the gameID based on the gameName
        self.cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?", (gameName,))
        game_row = self.cursor.fetchone()
        # If no game exists, send an error.
        if not game_row:
            raise ValueError(f"No game found with name: {gameName}")
        
        # Extract the gameID from the first column
        gameID = game_row[0]

        # Lookup the playerID based on the playerName
        self.cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?", (playerName,))
        player_row = self.cursor.fetchone()
        # If no game exists, send an error.
        if not player_row:
            raise ValueError(f"No player found with name: {playerName}")
        
        # Extract the playerID from the first columm
        playerID = player_row[0]

        # Insert a new shot for the player in the current game
        self.cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID, gameID))
        # Commit
        self.conn.commit()

        return self.cursor.lastrowid
    
    # Records the association between a table and a shot in the TableShot table.
    def recordTableShot(self, tableID, shotID):
        # SQL command to insert a new row into TableShot
        try:
            # Execute the SQL command with the provided IDs to insert a new row into TableShot
            self.cursor.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)""", (tableID, shotID))
            # Commit the changes to the database
            self.conn.commit()

        except sqlite3.Error as error:
            # Safety net to catch SQL errors. Mainly for testing/debugging reasons
            print(f"An error occurred while recording TableShot: {error}")
        
class Game:
    # Class variable to connect to the Database class
    db = Database()

    #  Initializes the Game object either by loading an existing game using its ID
    # or by creating a new game with names for the game and players
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        # Validate the input according to the specified rules
        if (gameID is not None and isinstance(gameID, int) and gameName is player1Name is player2Name is None):
            # Existing game to we load it with the gameID
            self.gameID = gameID + 1 # Adjust for SQL's 1-indexing
            self.loadGame() # Calls helper method to load the game details

        elif (gameID is None and all(isinstance(name, str) for name in [gameName, player1Name, player2Name])):
            # New game so we create it with the provided names
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.createNewGame() # Calls helper function to create the game

    # Helper method to load game details from the database into this Game object.
    # It assumes the gameID has already been set for this Game instance
    def loadGame(self):
        # Assuming db is an instance of the Database class
        db = Database()
        self.gameName, self.player1Name, self.player2Name = db.getGame(self.gameID)

    # Helper method to create a new game in the database with the provided names.
    # It assumes the gameName, player1Name, and player2Name have been set for this Game instance.
    def createNewGame(self):
        # Assuming db is an instance of the Database class
        db = Database()
        # Create the game in the database and get the new game ID
        self.gameID = db.setGame(self.gameName, self.player1Name, self.player2Name)

    def shoot(self, gameName, playerName, table, xvel, yvel):
        svgString = ""
        # Create a new shot and get its ID
        shotID = self.db.newShot(gameName, playerName)

        # Find the cue ball
        for ball in table:
            if isinstance(ball, (StillBall, RollingBall)) and ball.obj.still_ball.number == 0:
                cueBall = ball

        # Store the current position of the cue ball
        xpos, ypos = cueBall.obj.still_ball.pos.x, cueBall.obj.still_ball.pos.y

        # Change the type to RollingBall
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.number = 0
        cueBall.obj.rolling_ball.pos.x = xpos
        cueBall.obj.rolling_ball.pos.y = ypos
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel

        # Calculate the acceleration based on velocity and DRAG. Exact same way as A2 and in readTable
        speed = (xvel**2 + yvel**2)**0.5
        if speed > VEL_EPSILON:
            cueBall.obj.rolling_ball.acc.x = -(xvel / speed) * DRAG
            cueBall.obj.rolling_ball.acc.y = -(yvel / speed) * DRAG
        else:
            cueBall.obj.rolling_ball.acc.x = 0
            cueBall.obj.rolling_ball.acc.y = 0

        # Set the start time to the current time on the table passed before segment
        startTime = table.time
        lastTable = table
        # Call segment on the table passed and set the new table to a temporary table
        tempTable = table.segment()

        # Now, repeatedly call the segment method and handle each frame   
        while tempTable:
            lastTable = tempTable
            # Set the end time to the time after segment at the end of the while loop is called
            endTime = tempTable.time
            # Calculate the number of frames in this segment by subtracting start time from end time
            segmentTime = endTime - startTime
            # Calculate the frames by dividing segments time by the frame rate (0.01) and rounds to integer
            frames = int(segmentTime / FRAME_INTERVAL)
           
            # Loop over each frame, ensuring they are all non-negative.
            if frames >= 0:
                for frame in range(frames):
                    # Calculate the time passed for this frame
                    frameTime = frame * FRAME_INTERVAL

                    # Roll the table for this frame
                    newTable = table.roll(frameTime)
                    svgFrame = newTable.svg()
                    svgString += svgFrame

                    # Set the time for the new table
                    newTable.time = startTime + frameTime

                    # Save the new table state to the database
                    tableID = self.db.writeTable(newTable)
            
                    # Record this frame in TableShot
                    self.db.recordTableShot(tableID, shotID)
            else:
                print("Error: Negative frame found!")

            # Set the start time again for the next loop
            startTime = tempTable.time
            # Set the table to the new table
            table = tempTable
            # Call segment for the next loop
            tempTable = tempTable.segment()

        if svgFrame:
            svgString += svgFrame # Add the last frame to prevent balls from stopping just before the hole
            
        return svgString, lastTable
