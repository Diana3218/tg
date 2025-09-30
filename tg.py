import os
import webbrowser
from pathlib import Path

def create_2048_game():
    html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2048 Game</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 3em;
            color: #776e65;
            margin-bottom: 10px;
        }

        .user-section {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            align-items: center;
        }

        .user-section input {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }

        .user-section button {
            padding: 10px 15px;
            background: #8f7a66;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }

        .user-section button:hover {
            background: #7f6a56;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            background: #bbada0;
            padding: 15px;
            border-radius: 10px;
            color: white;
        }

        .stat-item {
            text-align: center;
        }

        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
        }

        .game-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            background: #bbada0;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .cell {
            width: 100%;
            aspect-ratio: 1;
            background: rgba(238, 228, 218, 0.35);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2em;
            font-weight: bold;
            transition: all 0.2s ease;
        }

        /* Цвета для плиток */
        .tile-2 { background: #eee4da; color: #776e65; }
        .tile-4 { background: #ede0c8; color: #776e65; }
        .tile-8 { background: #f2b179; color: #f9f6f2; }
        .tile-16 { background: #f59563; color: #f9f6f2; }
        .tile-32 { background: #f67c5f; color: #f9f6f2; }
        .tile-64 { background: #f65e3b; color: #f9f6f2; }
        .tile-128 { background: #edcf72; color: #f9f6f2; font-size: 1.5em; }
        .tile-256 { background: #edcc61; color: #f9f6f2; font-size: 1.5em; }
        .tile-512 { background: #edc850; color: #f9f6f2; font-size: 1.5em; }
        .tile-1024 { background: #edc53f; color: #f9f6f2; font-size: 1.2em; }
        .tile-2048 { background: #edc22e; color: #f9f6f2; font-size: 1.2em; }

        .controls {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }

        .control-row {
            display: flex;
            gap: 10px;
        }

        .controls button {
            padding: 15px 20px;
            background: #8f7a66;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.2em;
            min-width: 80px;
            transition: background 0.2s;
        }

        .controls button:hover {
            background: #7f6a56;
        }

        .actions {
            display: flex;
            gap: 10px;
            justify-content: center;
        }

        .actions button {
            padding: 12px 20px;
            background: #8f7a66;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
        }

        .actions button:hover {
            background: #7f6a56;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
        }

        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 400px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }

        .leaderboard-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        .leaderboard-table th,
        .leaderboard-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        .leaderboard-table th {
            background: #f5f5f5;
            font-weight: bold;
        }

        .close-btn {
            float: right;
            cursor: pointer;
            font-size: 1.5em;
            margin-top: -10px;
        }

        @media (max-width: 500px) {
            .container {
                padding: 15px;
            }
            
            .controls button {
                padding: 12px 15px;
                min-width: 60px;
                font-size: 1em;
            }
            
            .cell {
                font-size: 1.5em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 2048</h1>
        </div>

        <div class="user-section">
            <input type="text" id="username" placeholder="Введите имя игрока" value="Player">
            <button onclick="saveUser()">Сохранить</button>
        </div>

        <div class="stats">
            <div class="stat-item">
                <div>Очки</div>
                <div class="stat-value" id="current-score">0</div>
            </div>
            <div class="stat-item">
                <div>Лучший</div>
                <div class="stat-value" id="best-score">0</div>
            </div>
        </div>

        <div class="game-grid" id="game-grid">
            <!-- Игровое поле будет заполнено JavaScript -->
        </div>

        <div class="controls">
            <div class="control-row">
                <button onclick="makeMove('up')">⬆️ Вверх</button>
            </div>
            <div class="control-row">
                <button onclick="makeMove('left')">⬅️ Влево</button>
                <button onclick="makeMove('down')">⬇️ Вниз</button>
                <button onclick="makeMove('right')">➡️ Вправо</button>
            </div>
        </div>

        <div class="actions">
            <button onclick="newGame()">🔄 Новая игра</button>
            <button onclick="showLeaderboard()">🏆 Таблица лидеров</button>
            <button onclick="showStats()">📊 Моя статистика</button>
        </div>
    </div>

    <!-- Модальное окно для таблицы лидеров -->
    <div id="leaderboard-modal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('leaderboard-modal')">&times;</span>
            <h2>🏆 Таблица лидеров</h2>
            <table class="leaderboard-table" id="leaderboard-table">
                <thead>
                    <tr>
                        <th>Место</th>
                        <th>Игрок</th>
                        <th>Рекорд</th>
                        <th>Игр</th>
                    </tr>
                </thead>
                <tbody id="leaderboard-body">
                    <!-- Данные будут заполнены JavaScript -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- Модальное окно для статистики -->
    <div id="stats-modal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('stats-modal')">&times;</span>
            <h2>📊 Моя статистика</h2>
            <div id="stats-content">
                <!-- Данные будут заполнены JavaScript -->
            </div>
        </div>
    </div>

    <script>
        class Game2048 {
            constructor() {
                this.size = 4;
                this.grid = Array(this.size).fill().map(() => Array(this.size).fill(0));
                this.score = 0;
                this.addNewTile();
                this.addNewTile();
            }

            addNewTile() {
                const emptyCells = [];
                for (let i = 0; i < this.size; i++) {
                    for (let j = 0; j < this.size; j++) {
                        if (this.grid[i][j] === 0) {
                            emptyCells.push([i, j]);
                        }
                    }
                }
                
                if (emptyCells.length > 0) {
                    const [i, j] = emptyCells[Math.floor(Math.random() * emptyCells.length)];
                    this.grid[i][j] = Math.random() < 0.9 ? 2 : 4;
                }
            }

            moveLeft() {
                let moved = false;
                for (let i = 0; i < this.size; i++) {
                    let row = this.grid[i].filter(cell => cell !== 0);
                    
                    for (let j = 0; j < row.length - 1; j++) {
                        if (row[j] === row[j + 1]) {
                            row[j] *= 2;
                            this.score += row[j];
                            row.splice(j + 1, 1);
                            row.push(0);
                            moved = true;
                        }
                    }
                    
                    row = row.filter(cell => cell !== 0);
                    while (row.length < this.size) row.push(0);
                    
                    if (JSON.stringify(this.grid[i]) !== JSON.stringify(row)) {
                        moved = true;
                    }
                    this.grid[i] = row;
                }
                return moved;
            }

            moveRight() {
                this.grid = this.grid.map(row => row.reverse());
                const moved = this.moveLeft();
                this.grid = this.grid.map(row => row.reverse());
                return moved;
            }

            moveUp() {
                this.grid = this.grid[0].map((_, i) => this.grid.map(row => row[i]));
                const moved = this.moveLeft();
                this.grid = this.grid[0].map((_, i) => this.grid.map(row => row[i]));
                return moved;
            }

            moveDown() {
                this.grid = this.grid[0].map((_, i) => this.grid.map(row => row[i]));
                const moved = this.moveRight();
                this.grid = this.grid[0].map((_, i) => this.grid.map(row => row[i]));
                return moved;
            }

            isGameOver() {
                for (let i = 0; i < this.size; i++) {
                    for (let j = 0; j < this.size; j++) {
                        if (this.grid[i][j] === 0) return false;
                        if (j < this.size - 1 && this.grid[i][j] === this.grid[i][j + 1]) return false;
                        if (i < this.size - 1 && this.grid[i][j] === this.grid[i + 1][j]) return false;
                    }
                }
                return true;
            }
        }

        class Database {
            constructor() {
                this.initDB();
            }

            initDB() {
                if (!localStorage.getItem('2048_users')) {
                    localStorage.setItem('2048_users', JSON.stringify([]));
                }
            }

            getUsers() {
                return JSON.parse(localStorage.getItem('2048_users') || '[]');
            }

            saveUsers(users) {
                localStorage.setItem('2048_users', JSON.stringify(users));
            }

            getUser(username) {
                const users = this.getUsers();
                return users.find(user => user.username === username);
            }

            createUser(username) {
                const users = this.getUsers();
                const newUser = {
                    username,
                    bestScore: 0,
                    gamesPlayed: 0,
                    createdAt: new Date().toISOString()
                };
                users.push(newUser);
                this.saveUsers(users);
                return newUser;
            }

            updateUserScore(username, score) {
                const users = this.getUsers();
                const userIndex = users.findIndex(user => user.username === username);
                
                if (userIndex === -1) {
                    return this.createUser(username).bestScore;
                }

                const user = users[userIndex];
                if (score > user.bestScore) {
                    user.bestScore = score;
                }
                user.gamesPlayed++;
                this.saveUsers(users);
                return user.bestScore;
            }

            getLeaderboard(limit = 10) {
                const users = this.getUsers();
                return users
                    .sort((a, b) => b.bestScore - a.bestScore)
                    .slice(0, limit);
            }
        }

        // Глобальные переменные
        let game = null;
        let db = null;
        let currentUser = "Player";

        // Инициализация
        function init() {
            db = new Database();
            currentUser = localStorage.getItem('2048_currentUser') || "Player";
            document.getElementById('username').value = currentUser;
            updateStats();
            createGameGrid();
            newGame();
            
            // Привязка клавиш
            document.addEventListener('keydown', handleKeyPress);
        }

        function handleKeyPress(event) {
            switch(event.key) {
                case 'ArrowLeft': makeMove('left'); break;
                case 'ArrowRight': makeMove('right'); break;
                case 'ArrowUp': makeMove('up'); break;
                case 'ArrowDown': makeMove('down'); break;
                case 'n': case 'N': newGame(); break;
            }
        }

        function createGameGrid() {
            const grid = document.getElementById('game-grid');
            grid.innerHTML = '';
            
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    cell.id = `cell-${i}-${j}`;
                    grid.appendChild(cell);
                }
            }
        }

        function updateGrid() {
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    const cell = document.getElementById(`cell-${i}-${j}`);
                    const value = game.grid[i][j];
                    
                    cell.textContent = value !== 0 ? value : '';
                    cell.className = 'cell';
                    if (value !== 0) {
                        cell.classList.add(`tile-${value}`);
                    }
                }
            }
            
            document.getElementById('current-score').textContent = game.score;
        }

        function newGame() {
            game = new Game2048();
            updateGrid();
        }

        function makeMove(direction) {
            if (!game) return;
            
            let moved = false;
            switch(direction) {
                case 'left': moved = game.moveLeft(); break;
                case 'right': moved = game.moveRight(); break;
                case 'up': moved = game.moveUp(); break;
                case 'down': moved = game.moveDown(); break;
            }
            
            if (moved) {
                game.addNewTile();
                updateGrid();
                
                if (game.isGameOver()) {
                    const bestScore = db.updateUserScore(currentUser, game.score);
                    updateStats();
                    setTimeout(() => {
                        alert(`💀 Игра окончена!\\n🏆 Ваш результат: ${game.score}\\n🎯 Лучший результат: ${bestScore}`);
                    }, 100);
                }
            }
        }

        function saveUser() {
            const newUser = document.getElementById('username').value.trim();
            if (newUser) {
                currentUser = newUser;
                localStorage.setItem('2048_currentUser', currentUser);
                
                if (!db.getUser(currentUser)) {
                    db.createUser(currentUser);
                }
                
                updateStats();
                alert(`Игрок изменен на: ${currentUser}`);
            }
        }

        function updateStats() {
            const user = db.getUser(currentUser);
            if (user) {
                document.getElementById('best-score').textContent = user.bestScore;
            }
        }

        function showLeaderboard() {
            const leaderboard = db.getLeaderboard();
            const tbody = document.getElementById('leaderboard-body');
            tbody.innerHTML = '';
            
            leaderboard.forEach((user, index) => {
                const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}`;
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${medal}</td>
                    <td>${user.username}</td>
                    <td>${user.bestScore}</td>
                    <td>${user.gamesPlayed}</td>
                `;
                tbody.appendChild(row);
            });
            
            document.getElementById('leaderboard-modal').style.display = 'flex';
        }

        function showStats() {
            const user = db.getUser(currentUser);
            const content = document.getElementById('stats-content');
            
            if (user) {
                const date = new Date(user.createdAt).toLocaleDateString('ru-RU');
                content.innerHTML = `
                    <p><strong>Игрок:</strong> ${user.username}</p>
                    <p><strong>Лучший результат:</strong> ${user.bestScore}</p>
                    <p><strong>Сыграно игр:</strong> ${user.gamesPlayed}</p>
                    <p><strong>Играет с:</strong> ${date}</p>
                `;
            } else {
                content.innerHTML = '<p>Статистика не найдена!</p>';
            }
            
            document.getElementById('stats-modal').style.display = 'flex';
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // Запуск при загрузке страницы
        window.onload = init;
    </script>
</body>
</html>"""

    # Создаем файл
    file_path = Path("2048_game.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Получаем абсолютный путь к файлу
    absolute_path = file_path.absolute()
    
    # Открываем в браузере
    webbrowser.open(f"file://{absolute_path}")
    
    print(f"Игра 2048 создана и открыта в браузере!")
    print(f"Файл сохранен как: {absolute_path}")
    return absolute_path

def main():
    print("Создание игры 2048...")
    file_path = create_2048_game()
    
    print("\nИнструкция:")
    print("1. Игра откроется автоматически в вашем браузере")
    print("2. Управление:")
    print("   - Кнопки на экране")
    print("   - Стрелки на клавиатуре")
    print("   - Клавиша 'N' для новой игры")
    print("3. Сохраните файл '2048_game.html' чтобы играть позже")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()