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
            padding: 10px;
            touch-action: manipulation;
            user-select: none;
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
            cursor: pointer;
        }
        .controls {
            margin-top: 15px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .ctrl-btn {
            background-color: #ff9f43;
            color: white;
            font-size: 32px;
            width: 110px;
            height: 80px;
            border: none;
            border-radius: 20px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            cursor: pointer;
        }
        .ctrl-btn:active {
            background-color: #ee5253;
            transform: scale(0.95);
        }
        #start-btn {
            background-color: #2ed573;
            color: white;
            font-size: 22px;
            font-weight: bold;
            padding: 12px 30px;
            border: none;
            border-radius: 20px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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

    <canvas id="gameCanvas" width="360" height="420"></canvas>

    <!-- 左右控制大按鈕，最適合 iPad 姆指操作 -->
    <div class="controls">
        <button class="ctrl-btn" ontouchstart="moveLeft()" onclick="moveLeft()">⬅️ 左</button>
        <button class="ctrl-btn" ontouchstart="moveRight()" onclick="moveRight()">右 ➡️</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let playerX = 150;
        let playerY = 350;
        let playerWidth = 60;
        let playerHeight = 60;
        let playerSpeed = 35;

        let items = [];
        let score = 0;
        let isPig = false;
        let pigTimer = 0;
        let gameInterval = null;
        let gameRunning = false;

        function startGame() {
            playerX = 150;
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

        // 畫面直接點擊也可以左右移動
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

                // 更新跌落物件
                for (let i = items.length - 1; i >= 0; i--) {
                    items[i].y += items[i].speed;

                    // 檢查有沒有接到
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
                            pigTimer = 45; // 變豬約 1.5 秒
                            score += 5;
                        }
                        items.splice(i, 1);
                        continue;
                    }

                    // 跌出畫面就刪除
                    if (items[i].y > canvas.height) {
                        items.splice(i, 1);
                    }
                }

                if (isPig) {
                    pigTimer--;
                    if (pigTimer <= 0) isPig = false;
                }
            }

            // 畫跌落嘅糖同蘑菇
            ctx.font = "32px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            for (let item of items) {
                let icon = item.type === 'candy' ? '🍬' : '🍄';
                ctx.fillText(icon, item.x + item.size/2, item.y + item.size/2);
            }

            // 畫主角 (Auntie Mary 👩‍🍳 或 豬 🐷)
            let playerIcon = isPig ? "🐷" : "👩‍🍳";
            ctx.font = "48px Arial";
            ctx.fillText(playerIcon, playerX + playerWidth/2, playerY + playerHeight/2);

            // 更新分數面板
            let statusText = isPig ? "🐷 變咗蘑菇豬！" : "👩‍🍳 正常 Auntie Mary";
            document.getElementById("score-board").innerText = `分數: ${score} | 狀態: ${statusText}`;
        }

        startGame();
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=640)
