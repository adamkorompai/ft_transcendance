// debut du chrono
let elapsedTime = 0;

// Define canvas and context
const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');

// Define game elements
let ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: 2, // Ball speed in the x direction
    dy: 2, // Ball speed in the y direction
    radius: 5,
};

let leftPaddle = {
    x: 10,
    y: canvas.height / 2 - 25, // Center the paddle vertically
    width: 10,
    height: 50,
    dy: 0, // Paddle speed
    score: 0,
    defense: 0,
};

let rightPaddle = {
    x: canvas.width - 20,
    y: canvas.height / 2 - 25, // Center the paddle vertically
    width: 10,
    height: 50,
    dy: 0, // Paddle speed
    score: 0,
    defense: 0,
};

let goalScored = false; // Variable to track if a goal has been scored
let goalTime = 2000; // 2 seconds in milliseconds


function drawScores() {
    ctx.font = "20px Arial";
    ctx.fillStyle = "white";
    ctx.fillText(leftPaddle.score.toString(), canvas.width / 2 - 50, 30);
    ctx.fillText(rightPaddle.score.toString(), canvas.width / 2 + 30, 30);
}

// Define game constants
const paddleSpeed = 4;

// Event listeners for paddle movement
document.addEventListener('keydown', keyDownHandler);
document.addEventListener('keyup', keyUpHandler);

let zPressed = false;
let sPressed = false;
let upPressed = false;
let downPressed = false;

function startTimer() {
    gameTimer = setInterval(function() {
        elapsedTime++;
    }, 1000);
}

function stopTimer() {
    clearInterval(gameTimer);
}

function keyDownHandler(e) {
    if (e.key === 'z') {
        zPressed = true;
    } else if (e.key === 's') {
        sPressed = true;
    } else if (e.key === 'ArrowUp') {
        upPressed = true;
    } else if (e.key === 'ArrowDown') {
        downPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === 'z') {
        zPressed = false;
    } else if (e.key === 's') {
        sPressed = false;
    } else if (e.key === 'ArrowUp') {
        upPressed = false;
    } else if (e.key === 'ArrowDown') {
        downPressed = false;
    }
}

// Draw the paddles
function drawPaddles() {
    ctx.fillStyle = 'white';
    // Left paddle
    ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
    // Right paddle
    ctx.fillRect(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height);
}

// Draw the ball
function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = 'white';
    ctx.fill();
    ctx.closePath();
}

// Update game elements
function update() {
    // Move the paddles
    if (zPressed && leftPaddle.y > 0) {
        leftPaddle.y -= paddleSpeed;
    } else if (sPressed && leftPaddle.y < canvas.height - leftPaddle.height) {
        leftPaddle.y += paddleSpeed;
    }
    if (upPressed && rightPaddle.y > 0) {
        rightPaddle.y -= paddleSpeed;
    } else if (downPressed && rightPaddle.y < canvas.height - rightPaddle.height) {
        rightPaddle.y += paddleSpeed;
    }

    // Move the ball
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Collision detection with top and bottom walls
    if (ball.y + ball.dy > canvas.height - ball.radius || ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    }

    // Collision detection with paddles
    if (
        ball.x + ball.dx > rightPaddle.x &&
        ball.x + ball.dx < rightPaddle.x + rightPaddle.width &&
        ball.y > rightPaddle.y &&
        ball.y < rightPaddle.y + rightPaddle.height &&
        ball.x + ball.radius > rightPaddle.x
    ) {
        ball.dx = -ball.dx;
        ball.dy = (Math.random() - 0.5) * 6;
        rightPaddle.defense++;
    } else if (
        ball.x + ball.dx < leftPaddle.x + leftPaddle.width &&
        ball.x + ball.dx > leftPaddle.x &&
        ball.y > leftPaddle.y &&
        ball.y < leftPaddle.y + leftPaddle.height &&
        ball.x - ball.radius < leftPaddle.x + leftPaddle.width
    ) {
        ball.dx = -ball.dx;
        ball.dy = (Math.random() - 0.5) * 6;
        leftPaddle.defense++;
    }

    // Check for scoring (ball past the paddles)
    if (ball.x + ball.radius > canvas.width) {
        // Player 1 (left) scores
        if (!goalScored) {
            goalScored = true; // Set goal scored flag
            leftPaddle.score++;
            if (leftPaddle.score >= 3) {
                endGame(player1Username);
            } else {
                setTimeout(function() {
                    resetBall();
                    goalScored = false; // Reset goal scored flag after 2 seconds
                }, goalTime);
            }
        }
    } else if (ball.x - ball.radius < 0) {
        // Player 2 (right) scores
        if (!goalScored) {
            goalScored = true; // Set goal scored flag
            rightPaddle.score++;
            if (rightPaddle.score >= 3) {
                endGame(player2Username);
            } else {
                setTimeout(function() {
                    resetBall();
                    goalScored = false; // Reset goal scored flag after 2 seconds
                }, goalTime);
            }
        }
    }
}

// Function to end the game
function endGame(winner) {
    stopTimer();
    clearInterval(gameLoop);

    alert(`Game Over! ${winner} wins!`);

    // Save des stats du jeu
    fetch("/play/save-game-stats/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, 
        },
        body: JSON.stringify({
            player1: player1Username,
            player2: player2Username,
            player1_score: leftPaddle.score,
            player2_score: rightPaddle.score,
            time_played: elapsedTime,
            player1_nb_defense: leftPaddle.defense,
            player2_nb_defense: rightPaddle.defense,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur lors de la sauvegarde des statistiques du jeu');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}


function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.dx = -ball.dx; // Reverse ball direction
    ball.dy = Math.random() > 0.5 ? 2 : -2; // Randomize ball vertical direction
}

function drawMiddleLine() {
    ctx.beginPath();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 2;
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
}

// Clear canvas and redraw game elements
function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
     // Draw middle line
     drawMiddleLine();
    // Draw paddles
    drawPaddles();
    // Draw ball
    drawBall();
    // Draw scores
    drawScores();
}

// Main game loop
function gameLoop() {
    update();
    draw();
}

// Start the game loop
startTimer();
setInterval(gameLoop, 10); // Run the game loop every 10 milliseconds