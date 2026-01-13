<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Stopwatch</title>
    <style>
        body {
            background-color: black;
            color: #00ffcc;
            font-family: 'Courier New', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        #stopwatch {
            font-size: 2.5rem;
            text-align: center;
        }
        #time {
            background: linear-gradient(to right, #00ff00, #00ffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
        #controls {
            margin-top: 20px;
        }
        button {
            background-color: #004d4d;
            color: #00ffcc;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            cursor: pointer;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>
    <div id="stopwatch">
        <div id="time">
            <span id="century">00</span>:<span id="decade">00</span>:<span id="year">00</span>:<span id="month">00</span>:<span id="week">00</span>:<span id="day">00</span>:<span id="hour">00</span>:<span id="minute">00</span>:<span id="second">00</span>:<span id="millisecond">000</span>:<span id="microsecond">000</span>
        </div>
        <div id="controls">
            <button id="startStop">Start</button>
            <button id="reset">Reset</button>
        </div>
    </div>
    <script>
        let startTime;
        let elapsedTime = 0;
        let timerInterval;
        let isRunning = false;

        const timeElements = {
            century: document.getElementById('century'),
            decade: document.getElementById('decade'),
            year: document.getElementById('year'),
            month: document.getElementById('month'),
            week: document.getElementById('week'),
            day: document.getElementById('day'),
            hour: document.getElementById('hour'),
            minute: document.getElementById('minute'),
            second: document.getElementById('second'),
            millisecond: document.getElementById('millisecond'),
            microsecond: document.getElementById('microsecond')
        };

        const startStopButton = document.getElementById('startStop');
        const resetButton = document.getElementById('reset');

        function startStop() {
            if (isRunning) {
                clearInterval(timerInterval);
                startStopButton.textContent = 'Start';
                isRunning = false;
            } else {
                startTime = performance.now() - elapsedTime;
                timerInterval = setInterval(updateTime, 1);
                startStopButton.textContent = 'Stop';
                isRunning = true;
            }
        }

        function reset() {
            clearInterval(timerInterval);
            elapsedTime = 0;
            updateDisplay();
            startStopButton.textContent = 'Start';
            isRunning = false;
        }

        function updateTime() {
            elapsedTime = performance.now() - startTime;
            updateDisplay();
        }

        function updateDisplay() {
            const microseconds = Math.floor(elapsedTime * 1000) % 1000;
            const milliseconds = Math.floor(elapsedTime) % 1000;
            const seconds = Math.floor(elapsedTime / 1000) % 60;
            const minutes = Math.floor(elapsedTime / (1000 * 60)) % 60;
            const hours = Math.floor(elapsedTime / (1000 * 60 * 60)) % 24;
            const days = Math.floor(elapsedTime / (1000 * 60 * 60 * 24)) % 7;
            const weeks = Math.floor(elapsedTime / (1000 * 60 * 60 * 24 * 7)) % 4;
            const months = Math.floor(elapsedTime / (1000 * 60 * 60 * 24 * 30.44)) % 12;
            const years = Math.floor(elapsedTime / (1000 * 60 * 60 * 24 * 365.25)) % 10;
            const decades = Math.floor(elapsedTime / (1000 * 60 * 60 * 24 * 365.25 * 10)) % 10;
            const centuries = Math.floor(elapsedTime / (1000 * 60 * 60 * 24 * 365.25 * 100));

            timeElements.century.textContent = pad(centuries, 2);
            timeElements.decade.textContent = pad(decades, 2);
            timeElements.year.textContent = pad(years, 2);
            timeElements.month.textContent = pad(months, 2);
            timeElements.week.textContent = pad(weeks, 2);
            timeElements.day.textContent = pad(days, 2);
            timeElements.hour.textContent = pad(hours, 2);
            timeElements.minute.textContent = pad(minutes, 2);
            timeElements.second.textContent = pad(seconds, 2);
            timeElements.millisecond.textContent = pad(milliseconds, 3);
            timeElements.microsecond.textContent = pad(microseconds, 3);
        }

        function pad(number, length) {
            return number.toString().padStart(length, '0');
        }

        startStopButton.addEventListener('click', startStop);
        resetButton.addEventListener('click', reset);
    </script>
</body>
</html>