// Début du chrono
let elapsedTime = 0;

// Définir le canvas et le contexte
const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');

// Définir les éléments du jeu
let ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    dx: 2,
    dy: 2,
    radius: 5,
};

let leftPaddle = {
    x: 10,
    y: canvas.height / 2 - 25, // Centrer le paddle verticalement
    width: 10,
    height: 50,
    dy: 0, // Vitesse du paddle
    score: 0,
    defense: 0,
};

let rightPaddle = {
    x: canvas.width - 20,
    y: canvas.height / 2 - 25, // Centrer le paddle verticalement
    width: 10,
    height: 50,
    dy: 0, // Vitesse du paddle
    score: 0,
    defense: 0,
};

let goalScored = false; // Variable pour suivre si un but a été marqué
let goalTime = 2000; // 2 secondes en millisecondes

// Définir le pourcentage de chance que l'IA fasse une erreur
const errorChance = 0.2; // 20%

// Constantes du jeu
const paddleSpeed = 4;
const IApaddleSpeed = 150;
const IApaddleSpeedWithError = 2; // Vitesse plus basse pour l'IA en cas d'erreur

// Variable pour suivre le temps écoulé depuis la dernière mise à jour de l'IA
let lastAIUpdate = 0;

// Écouteurs d'événements pour le mouvement des paddles
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

// Fonction pour mettre à jour le paddle de l'IA
function updateAIPaddle() {
    const currentTime = Date.now();
    const deltaTime = (currentTime - lastAIUpdate) / 1000; // Temps écoulé en secondes
    lastAIUpdate = currentTime;

    // Décider aléatoirement si l'IA fera une erreur
    const hasError = Math.random() < errorChance;

    if (hasError) {
        // Comportement erroné : l'IA se déplace de manière aléatoire ou reste immobile
        if (Math.random() < 0.5) {
            rightPaddle.y -= IApaddleSpeedWithError * deltaTime;
        } else {
            rightPaddle.y += IApaddleSpeedWithError * deltaTime;
        }
    } else {
        // Comportement correct : suivre la balle comme d'habitude
        let futureBallY = ball.y;
        let futureBallX = ball.x;
        let ballDirectionY = ball.dy;
        let ballDirectionX = ball.dx;

        // Simuler le déplacement de la balle jusqu'à ce qu'elle atteigne la position X du paddle de l'IA
        while (futureBallX < rightPaddle.x && futureBallX + ballDirectionX > rightPaddle.x) {
            futureBallY += ballDirectionY;
            futureBallX += ballDirectionX;

            // Gestion des rebonds sur les murs
            if (futureBallY + ball.radius > canvas.height || futureBallY - ball.radius < 0) {
                ballDirectionY = -ballDirectionY; // Inverser la direction de la balle en y
            }
        }

        // Vérifiez si le paddle droit est déjà aligné avec la position future de la balle
        const paddleCenter = rightPaddle.y + rightPaddle.height / 2;
        const threshold = IApaddleSpeed * deltaTime; // Marge d'erreur basée sur le temps écoulé

        if (Math.abs(paddleCenter - futureBallY) < threshold) {
            rightPaddle.dy = 0; // Arrêter le paddle
        } else if (paddleCenter > futureBallY) {
            rightPaddle.y -= IApaddleSpeed * deltaTime;
            if (rightPaddle.y < 0) rightPaddle.y = 0; // Limite supérieure
        } else {
            rightPaddle.y += IApaddleSpeed * deltaTime;
            if (rightPaddle.y + rightPaddle.height > canvas.height) {
                rightPaddle.y = canvas.height - rightPaddle.height; // Limite inférieure
            }
        }
    }

    // Assurer que le paddle reste dans les limites du canvas
    if (rightPaddle.y < 0) rightPaddle.y = 0;
    if (rightPaddle.y + rightPaddle.height > canvas.height) {
        rightPaddle.y = canvas.height - rightPaddle.height;
    }
}

// Fonction pour dessiner les paddles
function drawPaddles() {
    ctx.fillStyle = 'white';
    // Paddle gauche
    ctx.fillRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
    // Paddle droit
    ctx.fillRect(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height);
}

// Fonction pour dessiner la balle
function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = 'white';
    ctx.fill();
    ctx.closePath();
}

// Mettre à jour les éléments du jeu
function update() {
    // Déplacer les paddles des joueurs
    if (sPressed && leftPaddle.y > 0) {
        leftPaddle.y -= paddleSpeed;
    } else if (zPressed && leftPaddle.y < canvas.height - leftPaddle.height) {
        leftPaddle.y += paddleSpeed;
    }

    // Déplacer paddle de l'IA
    updateAIPaddle();

    // Déplacer la balle
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Détection de collision avec les murs haut et bas
    if (ball.y + ball.dy > canvas.height - ball.radius || ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    }

    // Détection de collision avec les paddles
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

    // Vérifier si un but a été marqué (balle passée les paddles)
    if (ball.x + ball.radius > canvas.width) {
        // Joueur 1 (gauche) marque
        if (!goalScored) {
            goalScored = true; // Définir le drapeau de but marqué
            leftPaddle.score++;
            if (leftPaddle.score >= 1) {
                endGame(player1Username);
            } else {
                setTimeout(function() {
                    resetBall();
                    goalScored = false; // Réinitialiser le drapeau de but marqué après 2 secondes
                }, goalTime);
            }
        }
    } else if (ball.x - ball.radius < 0) {
        // Joueur 2 (droit) marque
        if (!goalScored) {
            goalScored = true; // Définir le drapeau de but marqué
            rightPaddle.score++;
            if (rightPaddle.score >= 1) {
                endGame('Pong GPT');
            } else {
                setTimeout(function() {
                    resetBall();
                    goalScored = false; // Réinitialiser le drapeau de but marqué après 2 secondes
                }, goalTime);
            }
        }
    }
}

// Fonction pour terminer le jeu
function endGame(winner) {
    stopTimer();
    clearInterval(gameLoop);
    clearInterval(aiUpdateInterval); // Arrêter la mise à jour de l'IA

    alert(`Game Over! ${winner} wins!`);

    // Save des stats du jeu
    fetch('/play/save-ia-game-stats/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            player: player1Username,
            player_score: leftPaddle.score,
            ia_score: rightPaddle.score,
            time_played: elapsedTime,
            player_nb_defense: leftPaddle.defense,
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
    ball.dx = -ball.dx; // Inverser la direction de la balle
    ball.dy = Math.random() > 0.5 ? 2 : -2; // Randomiser la direction verticale de la balle
}

function drawMiddleLine() {
    ctx.beginPath();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 2;
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
}

// Effacer le canvas et redessiner les éléments du jeu
function draw() {
    // Effacer le canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Dessiner la ligne du milieu
    drawMiddleLine();
    // Dessiner les paddles
    drawPaddles();
    // Dessiner la balle
    drawBall();
    // Dessiner les scores
    drawScores();
}

// Initialiser le jeu
function initGame() {
    startTimer();
    gameLoop = setInterval(function() {
        update();
        draw();
    }, 1000 / 60); // 60 FPS

    // Mise à jour de l'IA toutes les secondes
    lastAIUpdate = Date.now();
    aiUpdateInterval = setInterval(updateAIPaddle, 1000); // Mise à jour de l'IA toutes les secondes
}

// Lancer le jeu
initGame();
