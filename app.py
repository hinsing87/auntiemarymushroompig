import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="Auntie Mary 貪食蛇大冒險", page_icon="🐍", layout="centered"
)

# 嵌入完整嘅 HTML5 + JavaScript 貪食蛇遊戲
html_code = """
<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Auntie Mary 貪食蛇</title>
    <style>
        body {
            background-color: #f7f1e3;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 10px;
            touch-action: manipulation;
        }
        h1 {
            color: #ff4757;
            font-size: 24px;
            margin: 5px 0;
        }
        #score-board {
            font-size: 20px;
            color: #2e86de;
            font-weight: bold;
            margin-bottom: 10px;
        }
        canvas {
            background-color: #ffffff;
            border: 4px solid #ff4757;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            max-width: 100%;
            height: auto;
        }
        .controls {
            margin-top: 15px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            max-width: 280px;
            margin-left: auto;
            margin-right: auto;
        }
        .ctrl-btn {
            background-color: #ff9f43;
            color: white;
            font-size: 28px;
            padding: 20px 0;
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            cursor: pointer;
            user-select: none;
        }
        .ctrl-btn:active {
            background-color: #ee5253;
            transform: scale(0.95);
        }
        .empty { visibility: hidden; }
        #start-btn {
            background-color: #2ed573;
            color: white;
            font-size: 22px;
            font-weight: bold;
            padding: 12px 30px;
            border: none;
            border-radius: 20px;
            margin-top: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            cursor: pointer;
        }
    </style>
</head>
<body>

    <h1>👩‍🍳 Auntie Mary 貪食大冒險 🐷</h1>
    <div id="score-board">分數: 0 | 狀態: 正常 👩‍🍳</div>
    
    <canvas id="gameCanvas" width="360" height="360"></canvas>
    
    <div>
        <button id="start-btn" onclick="startGame()">開始 / 重新開始遊戲</button>
    </div>

    <!-- 專為 iPad 觸控而設嘅方向掣 -->
    <div class="controls">
        <div class="empty"></div>
        <button class="ctrl-btn" onclick="setDir(0, -1)">⬆️</button>
        <div class="empty"></div>
        <button class="ctrl-btn" onclick="setDir(-1, 0)">⬅️</button>
        <button class="ctrl-btn" onclick="setDir(0, 1)">⬇️</button>
        <button class="ctrl-btn" onclick="setDir(1, 0)">➡️</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const gridSize = 20;
        const tileCount = 18;

        let snake = [];
        let dx = 1;
        let dy = 0;
        let candy = {x: 5, y: 5};
        let mushroom = {x: 10, y: 10};
        let score = 0;
        let isPig = false;
        let pigTimer = 0;
        let gameInterval = null;
        let gameRunning = false;

        function startGame() {
            snake = [
                {x: 8, y: 8},
                {x: 7, y: 8},
                {x: 6, y: 8}
            ];
            dx = 1;
            dy = 0;
            score = 0;
            isPig = false;
            pigTimer = 0;
            spawnCandy();
            spawnMushroom();
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(gameLoop, 150);
            gameRunning = true;
        }

        function setDir(newDx, newDy) {
            // 避免原地掉頭
            if (newDx !== -0 && dx !== -newDx) {
                dx = newDx;
                dy = newDy;
            }
            if (newDy !== -0 && dy !== -newDy) {
                dx = newDx;
                dy = newDy;
            }
        }

        function spawnCandy() {
            candy.x = Math.floor(Math.random() * tileCount);
            candy.y = Math.floor(Math.random() * tileCount);
        }

        function spawnMushroom() {
            mushroom.x = Math.floor(Math.random() * tileCount);
            mushroom.y = Math.floor(Math.random() * tileCount);
        }

        function gameLoop() {
            update();
            draw();
        }

        function update() {
            let head = {x: snake[0].x + dx, y: snake[0].y + dy};

            // 撞牆穿牆或 Game Over 設定（對4歲小朋友友善：撞牆會由另一邊出返黎）
            if (head.x < 0) head.x = tileCount - 1;
            if (head.x >= tileCount) head.x = 0;
            if (head.y < 0) head.y = tileCount - 1;
            if (head.y >= tileCount) head.y = 0;

            // 撞到自己
            for (let i = 0; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    gameOver();
                    return;
                }
            }

            snake.unshift(head);

            // 食到糖果 🍬
            if (head.x === candy.x && head.y === candy.y) {
                score += 10;
                spawnCandy();
            } else {
                snake.pop();
            }

            // 食到蘑菇 🍄 -> 變身成豬 🐷！
            if (head.x === mushroom.x && head.y === mushroom.y) {
                isPig = true;
                pigTimer = 15; // 維持 15 個影格係豬嘅狀態
                score += 5;
                spawnMushroom();
            }

            if (isPig) {
                pigTimer--;
                if (pigTimer <= 0) {
                    isPig = false;
                }
            }

            updateScoreBoard();
        }

        function draw() {
            // 清空畫面
            ctx.fillStyle = "#fdfbf7";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 畫格線（淡淡的）
            ctx.strokeStyle = "#f1f2f6";
            for (let i = 0; i < tileCount; i++) {
                ctx.beginPath();
                ctx.moveTo(i * gridSize, 0);
                ctx.lineTo(i * gridSize, canvas.height);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(0, i * gridSize);
                ctx.lineTo(canvas.width, i * gridSize);
                ctx.stroke();
            }

            // 畫糖果 🍬
            ctx.font = "20px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText("🍬", candy.x * gridSize + gridSize/2, candy.y * gridSize + gridSize/2);

            // 畫蘑菇 🍄
            ctx.fillText("🍄", mushroom.x * gridSize + gridSize/2, mushroom.y * gridSize + gridSize/2);

            // 畫貪食蛇（Auntie Mary 👩‍🍳 或 豬 🐷）
            for (let i = 0; i < snake.length; i++) {
                let icon = "👩‍🍳";
                if (isPig) {
                    icon = "🐷";
                } else if (i > 0) {
                    icon = "💖"; // 身體變成心心
                }
                ctx.fillText(icon, snake[i].x * gridSize + gridSize/2, snake[i].y * gridSize + gridSize/2);
            }
        }

        function updateScoreBoard() {
            let statusText = isPig ? "🐷 變咗蘑菇豬啦！" : "👩‍🍳 正常 Auntie Mary";
            document.getElementById("score-board").innerText = `分數: ${score} | 狀態: ${statusText}`;
        }

        function gameOver() {
            clearInterval(gameInterval);
            gameRunning = false;
            alert("哎呀！撞到自己啦！禁「開始」再玩過啦！");
        }

        // 初始畫一次畫面
        spawnCandy();
        spawnMushroom();
        draw();
    </script>
</body>
</html>
"""

# 用 Streamlit 嘅 components 將 HTML 嵌入去
st.components.v1.html(html_code, height=620)
