from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import random
import math
import json
from Physics import Table, Coordinate, StillBall, RollingBall
from Physics import TABLE_WIDTH, BALL_DIAMETER, TABLE_LENGTH, DRAG, VEL_EPSILON
from Physics import Game, Database

def createDatabase():
    db = Database()
    db.createDB()

def nudge():
    return random.uniform( -1.5, 1.5 )

def createFullRackTable():
    table = Table()  # Create and set up your initial table
    # Position the cue ball
    pos = Coordinate(TABLE_WIDTH / 2.0 + random.uniform(-3.0, 3.0), TABLE_LENGTH - TABLE_WIDTH / 2.0)
    cue_ball = StillBall(0, pos)
    table += cue_ball

    # Define the starting position for the rack
    starting_x = TABLE_WIDTH / 2.0
    starting_y = TABLE_WIDTH / 2.0
    ball_offset = BALL_DIAMETER + 4.0  # Slight offset between the balls

    # Triangular rack: 1 + 2 + 3 + 4 + 5 balls
    ball_number = 1  # Start with ball 1 (after the cue ball)
    for row in range(1, 6):  # 5 rows in a standard rack
        for ball_in_row in range(row):
            x_pos = starting_x - (ball_offset / 2.0) * (row - 1) + ball_in_row * ball_offset + nudge()
            y_pos = starting_y - math.sqrt(3.0) / 2.0 * ball_offset * (row - 1) + nudge()

            ball = StillBall(ball_number, Coordinate(x_pos, y_pos))
            table += ball
            ball_number += 1

    return table

class RequestHandler(BaseHTTPRequestHandler):
    createDatabase()
    current_table = createFullRackTable()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>8-Ball Pool Game</title>
                <style>
                    body {
                        font-family: 'Calibri', sans-serif;
                        background-color: #f4f4f4;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        position: relative;
                    }

                    h1 {
                        text-align: center;
                        color: #333;
                    }

                    form {
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }

                    label {
                        display: block;
                        margin-bottom: 5px;
                        color: #333;
                    }

                    input[type="text"] {
                        width: 100%;
                        padding: 10px;
                        margin-bottom: 20px;
                        border-radius: 5px;
                        border: 1px solid #ddd;
                        box-sizing: border-box; /* Added for consistent sizing */
                    }

                    input[type="submit"] {
                        width: 100%;
                        background-color: #4CAF50;
                        color: white;
                        padding: 15px 20px;
                        margin: 10px 0;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }

                    input[type="submit"]:hover {
                        background-color: #45a049;
                    }
                    footer {
                        position: absolute;
                        bottom: 10px;
                        left: 10px;
                        color: #333;
                        font-size: 14px;
                    }
                </style>
            </head>
            <body>
                <form id="start-form" action="start" method="post">
                    <h1>Welcome to the 8-Ball Pool Game</h1>
                    <label for="game-name">Game Name:</label>
                    <input type="text" id="game-name" name="gameName" required>
                    <label for="player1-name">Player 1:</label>
                    <input type="text" id="player1-name" name="player1" required>
                    <label for="player2-name">Player 2:</label>
                    <input type="text" id="player2-name" name="player2" required>
                    <input type="submit" value="Start Game">
                </form>
                <footer>
                    Written and Developed by Hisham Issa (hissa01@uoguelph.ca). March 2024.
                </footer>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode())
        elif self.path.startswith('/game'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            query = parse_qs(urlparse(self.path).query)
            gameName = query.get("gameName", [""])[0]
            player1 = query.get("player1", [""])[0]
            player2 = query.get("player2", [""])[0]
            initial_turn = random.choice([player1, player2])

            svgTable = RequestHandler.current_table.svg()

            game_content = f"""
            <html>
            <head>
                <title>Pool Table</title>
                <style>
                    body {{
                        font-family: 'Calibri', sans-serif;
                        background-color: #f4f4f4;
                        text-align: center;
                        margin: 0;
                        position: relative;
                    }}
                    h1 {{
                        color: #333;
                        margin: 20px 0;
                    }}
                    .player-name {{
                        position: absolute;
                        top: 50%;
                        transform: translateY(-50%);
                        font-size: 24px;
                        color: #333;
                    }}
                    .player1-desc, .player2-desc {{
                        position: absolute;
                        top: 60%; /* Slightly below the player name */
                        font-size: 16px; /* Smaller font size for the description */
                        color: #555;
                    }}
                     .player1-desc {{
                        left: 10px;
                    }}
                    .player2-desc {{
                        right: 10px;
                    }}
                    .player1 {{
                        left: 10px;
                    }}
                    .player2 {{
                        right: 10px;
                    }}
                    .svg-container {{
                        width: 33%;
                        height: auto;
                        margin: 0 auto; 
                        margin-left: 560px;
                    }}
                    .svg-container svg {{
                        width: 66%;
                        height: auto;
                        display: block;
                    }}
                    #cue-ball {{
                        stroke: white;
                        stroke-width: 1;
                    }}
                    footer {{
                        position: absolute;
                        bottom: 0px;
                        left: 10px;
                        color: #333;
                        font-size: 8px;
                    }}
                    .turn-indicator {{
                        font-size: 18px;
                        color: #333;
                        margin: 20px 0;
                    }}
                </style>
            </head>
            <body>
                <h1>Pool Table</h1>
                <input type="hidden" id="game-name" value="{gameName}">
                <input type="hidden" id="player1-name" value="{player1}">
                <div class="player-name player1">Player 1: {player1}</div>
                <div class="player1-desc">Low Balls</div>
                <input type="hidden" id="player2-name" value="{player2}">
                <div class="player-name player2">Player 2: {player2}</div>
                <div class="player2-desc">High Balls</div>
                <div id="svg-container" class="svg-container">
                    {svgTable}
                </div>
                <div class="turn-indicator" id="turn-indicator">Turn: {initial_turn}</div>
                <footer>
                    Written and Developed by Hisham Issa (hissa01@uoguelph.ca). March 2024.
                </footer>
                <script>
                    let isDragging = false;
                    let line = null; 
                    
                    let startX, startY;
                    const VEL_EPSILON = 0.01;
                    const DRAG = 150.0;

                    const svgContainer = document.getElementById('svg-container');
                    const cueBall = document.getElementById('cue-ball');

                    document.addEventListener('DOMContentLoaded', initializeCueBallInteraction);

                    function initializeCueBallInteraction() {{
                        const svg = document.querySelector('svg');
                        let isDragging = false;
                        let line = null;
                        let animationComplete = true;

                        const cueBall = document.getElementById('cue-ball');
                        const svgContainer = document.getElementById('svg-container');

                        let gameName = document.getElementById('game-name').value;
                        let player1Name = document.getElementById('player1-name').value;
                        let player2Name = document.getElementById('player2-name').value;
                        let currentTurn = document.getElementById("turn-indicator").textContent.split(": ")[1].trim();

                        if (!cueBall) {{
                            console.error("No Cue Ball")
                            return;
                        }}

                        function getMousePosition(evt) {{
                            let CTM = svg.getScreenCTM();
                            return {{
                                x: (evt.clientX - CTM.e) / CTM.a,
                                y: (evt.clientY - CTM.f) / CTM.d
                                }};
                            }}

                        function createLine(x1, y1, x2, y2) {{
                            let line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            line.setAttribute('x1', x1);
                            line.setAttribute('y1', y1);
                            line.setAttribute('x2', x2);
                            line.setAttribute('y2', y2);
                            line.style.stroke = 'black';
                            line.style.strokeWidth = '12';
                            svg.appendChild(line);
                            return line;
                        }}

                        function finalizeShot(vx, vy) {{
                            fetch('/shoot', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ 
                                    gameName: gameName, 
                                    player1Name: player1Name,
                                    player2Name: player2Name,
                                    vx: vx, 
                                    vy: vy 
                                }})
                            }})
                            .then(response => response.json())
                            .then(svgFrames => {{
                                // Handle the SVG frames here, e.g., animate them
                                let currentFrame = 0;
                                function displayNextFrame() {{
                                    if (currentFrame < svgFrames.length) {{
                                        svgContainer.innerHTML = svgFrames[currentFrame];
                                        currentFrame++;
                                        setTimeout(displayNextFrame, 2);
                                    }} else {{
                                        animationComplete = true;
                                        currentTurn = (currentTurn === player1Name) ? player2Name : player1Name;
                                        document.getElementById("turn-indicator").textContent = "Turn: " + currentTurn;
                                        // Reinitialize the cue ball interaction after the shot animation is complete
                                        initializeCueBallInteraction();
                                    }}
                                }}
                                animationComplete = false;
                                displayNextFrame();
                            }});
                        }}

                        cueBall.addEventListener('mousedown', function(evt) {{
                            isDragging = true;
                            const pos = getMousePosition(evt);
                            startX = pos.x
                            startY = pos.y
                            line = createLine(startX, startY, startX, startY);
                        }});

                        svgContainer.addEventListener('mousemove', function(evt) {{
                            if (isDragging && line) {{
                                const pos = getMousePosition(evt);
                                line.setAttribute('x2', pos.x);
                                line.setAttribute('y2', pos.y);
                            }}
                        }});

                        window.addEventListener('mouseup', function(evt) {{
                            if (isDragging) {{
                                isDragging = false;
                                let pt = svg.createSVGPoint();
                                pt.x = evt.clientX;
                                pt.y = evt.clientY;
                                let cursorPoint = pt.matrixTransform(svg.getScreenCTM().inverse());

                                let vx = -(cursorPoint.x - startX) * 3;
                                let vy = -(cursorPoint.y - startY) * 3;
                                if (line) svg.removeChild(line);
                                finalizeShot(vx, vy);
                            }}
                        }});
                    }};
                </script>
            </body>
            </html>
            """
            self.wfile.write(game_content.encode())
            # self.wfile.write(table.svg().encode())

    def do_POST(self):
        if self.path == '/start':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data = parse_qs(post_data)

            player1 = post_data["player1"][0]
            player2 = post_data["player2"][0]

            first_player = random.choice([player1, player2])

            # Redirect to the game page with the first player's name as a query parameter
            self.send_response(303)
            self.send_header('Location', f'/game?player1={player1}&player2={player2}&first_player={first_player}')
            self.end_headers()

        if self.path == '/shoot':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            gameName = post_data['gameName']
            player1Name = post_data['player1Name']
            player2Name = post_data['player2Name']
            xvel = float(post_data.get('vx', 0) or 0)
            yvel = float(post_data.get('vy', 0) or 0)
            print(gameName, player1Name, player2Name, xvel, yvel)

            game = Game(gameName=gameName, player1Name=player1Name, player2Name=player2Name)

            AllSVGs, RequestHandler.current_table = game.shoot(gameName, player1Name, RequestHandler.current_table, xvel, yvel)
            
            svg_Frames = AllSVGs.split('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')[1:]
            svg_Frames = [f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>{frame}' for frame in svg_Frames if frame.strip()]

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            response = json.dumps(svg_Frames)
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=54466):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
