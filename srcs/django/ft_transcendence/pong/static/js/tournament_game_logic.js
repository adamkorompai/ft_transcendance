let game;

class TournamentPongGame {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.elapsedTime = 0;
        this.gameTimer = null;
        this.gameLoop = null;

        this.ball = {
            x: this.canvas.width / 2,
            y: this.canvas.height / 2,
            dx: 2,
            dy: 2,
            radius: 5,
        };

        this.leftPaddle = {
            x: 10,
            y: this.canvas.height / 2 - 25,
            width: 10,
            height: 50,
            dy: 0,
            score: 0,
            defense: 0,
        };

        this.rightPaddle = {
            x: this.canvas.width - 20,
            y: this.canvas.height / 2 - 25,
            width: 10,
            height: 50,
            dy: 0,
            score: 0,
            defense: 0,
        };

        this.goalScored = false;
        this.goalTime = 2000;
        this.paddleSpeed = 4;

        this.zPressed = false;
        this.sPressed = false;
        this.upPressed = false;
        this.downPressed = false;

        this.setupEventListeners();
    }

    setupEventListeners() {
        document.addEventListener('keydown', this.keyDownHandler.bind(this));
        document.addEventListener('keyup', this.keyUpHandler.bind(this));
    }

    keyDownHandler(e) {
        if (e.key === 'z') this.zPressed = true;
        else if (e.key === 's') this.sPressed = true;
        else if (e.key === 'ArrowUp') this.upPressed = true;
        else if (e.key === 'ArrowDown') this.downPressed = true;
    }

    keyUpHandler(e) {
        if (e.key === 'z') this.zPressed = false;
        else if (e.key === 's') this.sPressed = false;
        else if (e.key === 'ArrowUp') this.upPressed = false;
        else if (e.key === 'ArrowDown') this.downPressed = false;
    }

    startTimer() {
        this.gameTimer = setInterval(() => {
            this.elapsedTime++;
        }, 1000);
    }

    stopTimer() {
        clearInterval(this.gameTimer);
    }

    drawPaddles() {
        this.ctx.fillStyle = 'white';
        this.ctx.fillRect(this.leftPaddle.x, this.leftPaddle.y, this.leftPaddle.width, this.leftPaddle.height);
        this.ctx.fillRect(this.rightPaddle.x, this.rightPaddle.y, this.rightPaddle.width, this.rightPaddle.height);
    }

    drawBall() {
        this.ctx.beginPath();
        this.ctx.arc(this.ball.x, this.ball.y, this.ball.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = 'white';
        this.ctx.fill();
        this.ctx.closePath();
    }

    drawScores() {
        this.ctx.font = "20px Arial";
        this.ctx.fillStyle = "white";
        this.ctx.fillText(this.leftPaddle.score.toString(), this.canvas.width / 2 - 50, 30);
        this.ctx.fillText(this.rightPaddle.score.toString(), this.canvas.width / 2 + 30, 30);
    }

    drawMiddleLine() {
        this.ctx.beginPath();
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 2;
        this.ctx.moveTo(this.canvas.width / 2, 0);
        this.ctx.lineTo(this.canvas.width / 2, this.canvas.height);
        this.ctx.stroke();
    }

    update() {
        // Move paddles
        if (this.sPressed && this.leftPaddle.y > 0) this.leftPaddle.y -= this.paddleSpeed;
        else if (this.zPressed && this.leftPaddle.y < this.canvas.height - this.leftPaddle.height) this.leftPaddle.y += this.paddleSpeed;
        if (this.upPressed && this.rightPaddle.y > 0) this.rightPaddle.y -= this.paddleSpeed;
        else if (this.downPressed && this.rightPaddle.y < this.canvas.height - this.rightPaddle.height) this.rightPaddle.y += this.paddleSpeed;

        // Move ball
        this.ball.x += this.ball.dx;
        this.ball.y += this.ball.dy;

        // Wall collisions
        if (this.ball.y + this.ball.dy > this.canvas.height - this.ball.radius || this.ball.y + this.ball.dy < this.ball.radius) {
            this.ball.dy = -this.ball.dy;
        }

        // Paddle collisions
        if (this.ball.x + this.ball.dx > this.rightPaddle.x && this.ball.x + this.ball.dx < this.rightPaddle.x + this.rightPaddle.width &&
            this.ball.y > this.rightPaddle.y && this.ball.y < this.rightPaddle.y + this.rightPaddle.height) {
            this.ball.dx = -this.ball.dx;
            this.ball.dy = (Math.random() - 0.5) * 6;
            this.rightPaddle.defense++;
        } else if (this.ball.x + this.ball.dx < this.leftPaddle.x + this.leftPaddle.width && this.ball.x + this.ball.dx > this.leftPaddle.x &&
            this.ball.y > this.leftPaddle.y && this.ball.y < this.leftPaddle.y + this.leftPaddle.height) {
            this.ball.dx = -this.ball.dx;
            this.ball.dy = (Math.random() - 0.5) * 6;
            this.leftPaddle.defense++;
        }

        // Scoring
        if (this.ball.x + this.ball.radius > this.canvas.width) {
            if (!this.goalScored) {
                this.goalScored = true;
                this.leftPaddle.score++;
                if (this.leftPaddle.score >= 3) {
                    this.endGame(player1Username);
                } else {
                    setTimeout(() => {
                        this.resetBall();
                        this.goalScored = false;
                    }, this.goalTime);
                }
            }
        } else if (this.ball.x - this.ball.radius < 0) {
            if (!this.goalScored) {
                this.goalScored = true;
                this.rightPaddle.score++;
                if (this.rightPaddle.score >= 3) {
                    this.endGame(player2Username);
                } else {
                    setTimeout(() => {
                        this.resetBall();
                        this.goalScored = false;
                    }, this.goalTime);
                }
            }
        }
    }

    resetBall() {
        this.ball.x = this.canvas.width / 2;
        this.ball.y = this.canvas.height / 2;
        this.ball.dx = -this.ball.dx;
        this.ball.dy = Math.random() > 0.5 ? 2 : -2;
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawMiddleLine();
        this.drawPaddles();
        this.drawBall();
        this.drawScores();
    }

    start() {
        this.startTimer();
        this.gameLoop = setInterval(() => {
            this.update();
            this.draw();
        }, 10);
    }

    endGame(winner) {
        this.stopTimer();
        clearInterval(this.gameLoop);
    
        alert(`Game Over! ${winner} wins!`);
    
        fetch("/play/save-game-stats/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                tournament_id: tournamentId,
                player1: player1Username,
                player2: player2Username,
                player1_score: this.leftPaddle.score,
                player2_score: this.rightPaddle.score,
                time_played: this.elapsedTime,
                player1_nb_defense: this.leftPaddle.defense,
                player2_nb_defense: this.rightPaddle.defense,
                winner: winner,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Game stats saved:", data);
            document.getElementById('nextGameButton').style.display = 'block';
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
    }
}

function nextGame() {
    fetch(`/play/tournaments/${tournamentId}/next-match/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            player1Username = data.player1;
            player2Username = data.player2;
            
            game = new TournamentPongGame(document.getElementById('pongCanvas'));
            
            document.getElementById('nextGameButton').style.display = 'none';
            document.getElementById('startGameButton').style.display = 'block';
            
            updatePlayerDisplay(data.player1, data.player2);
            
            // alert(`Next match: ${data.player1} vs ${data.player2}`);
        } else if (data.error === 'Tournament finished') {
            alert(`Tournament is over ! Winner is ${data.winner} !`);
            window.location.href = "/play/tournaments/";
        } else {
            alert("An error occurred while retrieving the next match.");
            window.location.href = "/play/tournaments/";
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

// Fonction pour mettre à jour l'affichage des joueurs
function updatePlayerDisplay(player1, player2) {
    const player1Element = document.querySelector('.player:nth-child(1)');
    const player2Element = document.querySelector('.player:nth-child(2)');

    player1Element.querySelector('span').textContent = player1;
    player2Element.querySelector('span').textContent = player2 || "Guest Player";

    // Mise à jour des images
    fetch(`/play/check-user/${player1}/`)
        .then(response => response.json())
        .then(data => {
            player1Element.querySelector('img').src = data.profile_image;
        });

    if (player2) {
        fetch(`/play/check-user/${player2}/`)
            .then(response => response.json())
            .then(data => {
                player2Element.querySelector('img').src = data.profile_image;
            });
    } else {
        player2Element.querySelector('img').src = "/static/../media/ia.gif";
    }
}

function initGame() {
    const canvas = document.getElementById('pongCanvas');
    game = new TournamentPongGame(canvas);
}

function startGame() {
    if (game) {
        game.start();
    }
}

function finishTournament() {
    window.location.href = "/play/tournaments/";
}

document.addEventListener('DOMContentLoaded', initGame);
