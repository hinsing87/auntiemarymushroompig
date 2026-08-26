import streamlit as st

st.set_page_config(
    page_title="Auntie Mary 接蘑菇豬", page_icon="🍄", layout="centered"
)

html_code = """
<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Auntie Mary 接蘑菇豬</title>
    <style>
        body {
            background-color: #f7f1e3;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 5px;
            touch-action: manipulation;
            user-select: none;
        }
        h1 {
            color: #ff4757;
            font-size: 22px;
            margin: 5px 0;
        }
        #score-board {
            font-size: 18px;
            color: #2e86de;
            font-weight: bold;
            margin-bottom: 5px;
        }
        canvas {
            background-color: #ffffff;
            border: 4px solid #ff4757;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            max-width: 100%;
            height: auto;
            cursor: pointer;
        }
        .controls {
            margin-top: 10px;
            display: flex;
            justify-content: center;
            gap: 15px;
        }
        .ctrl-btn {
            background-color: #ff9f43;
            color: white !important;
            font-size: 26px;
            font-weight: bold;
            width: 130px;
            height: 70px;
            border: none;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: pointer;
        }
        .ctrl-btn:active {
            background-color: #ee5253;
            transform: scale(0.95);
        }
        #start-btn {
            background-color: #2ed573;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 8px 20px;
            border: none;
            border-radius: 15px;
            margin-bottom: 5px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            cursor: pointer;
        }
    </style>
</head>
<body>

    <h1>👩‍🍳 Auntie Mary 接蘑菇豬 🐷</h1>
    <div id="score-board">分數: 0 | 狀態: 正常 👩‍🍳</div>
    
    <div>
        <button id="start-btn" onclick="startGame()">開始 / 重新開始遊戲</button>
    </div>

    <canvas id="gameCanvas" width="340" height="380"></canvas>

    <!-- 修正後清晰見到字嘅左右大按鈕 -->
    <div class="controls">
        <button class="ctrl-btn" ontouchstart="moveLeft()" onclick="moveLeft()">⬅️ 左</button>
        <button class="ctrl-btn" ontouchstart="moveRight()" onclick="moveRight()">右 ➡️</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let playerX = 140;
        let playerY = 310;
        let playerWidth = 60;
        let playerHeight = 60;
        let playerSpeed = 40;

        let items = [];
        let score = 0;
        let isPig = false;
        let pigTimer = 0;
        let gameInterval = null;
        let gameRunning = false;

        function startGame() {
            playerX = 140;
            score = 0;
            isPig = false;
            pigTimer = 0;
            items = [];
            gameRunning = true;
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(gameLoop, 30);
        }

        function moveLeft() {
            if (!gameRunning) return;
            playerX -= playerSpeed;
            if (playerX < 0) playerX = 0;
        }

        function moveRight() {
            if (!gameRunning) return;
            playerX += playerSpeed;
            if (playerX > canvas.width - playerWidth) playerX = canvas.width - playerWidth;
        }

        canvas.addEventListener('click', function(e) {
            if (!gameRunning) return;
            const rect = canvas.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            if (clickX < canvas.width / 2) {
                moveLeft();
            } else {
                moveRight();
            }
        });

        function spawnItem() {
            if (Math.random() < 0.08) {
                let type = Math.random() < 0.5 ? 'candy' : 'mushroom';
                let x = Math.random() * (canvas.width - 40);
                items.push({x: x, y: 0, type: type, size: 40, speed: 4 + Math.random() * 3});
            }
        }

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (gameRunning) {
                spawnItem();

                for (let i = items.length - 1; i >= 0; i--) {
                    items[i].y += items[i].speed;

                    if (
                        items[i].y + items[i].size >= playerY &&
                        items[i].y <= playerY + playerHeight &&
                        items[i].x + items[i].size >= playerX &&
                        items[i].x <= playerX + playerWidth
                    ) {
                        if (items[i].type === 'candy') {
                            score += 10;
                        } else {
                            isPig = true;
                            pigTimer = 45;
                            score += 5;
                        }
                        items.splice(i, 1);
                        continue;
                    }

                    if (items[i].y > canvas.height) {
                        items.splice(i, 1);
                    }
                }

                if (isPig) {
                    pigTimer--;
                    if (pigTimer <= 0) isPig = false;
                }
            }

            ctx.font = "30px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            for (let item of items) {
                let icon = item.type === 'candy' ? '🍬' : '🍄';
                ctx.fillText(icon, item.x + item.size/2, item.y + item.size/2);
            }

            let playerIcon = isPig ? "🐷" : "👩‍🍳";
            ctx.font = "46px Arial";
            ctx.fillText(playerIcon, playerX + playerWidth/2, playerY + playerHeight/2);

            let statusText = isPig ? "🐷 變咗蘑菇豬！" : "👩‍🍳 正常 Auntie Mary";
            document.getElementById("score-board").innerText = `分數: ${score} | 狀態: ${statusText}`;
        }

        startGame();
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=550)
