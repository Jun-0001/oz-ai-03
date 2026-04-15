const timeInput = document.querySelector("#time-input");
const startBtn = document.querySelector("#start-timer");
const stopBtn = document.querySelector("#stop-timer");
const display = document.querySelector("#timer-display")

let timerId = null;
let remainingSeconds = 0;

// 현재 남은 시간(초)를 {분:초} 형태로 출력
function updateDisplay() {
    const min = Math.floor(remainingSeconds/60);
    const sec = remainingSeconds % 60;

    // min = 1 & sec = 9 => 01:09
    display.textContent = 
        String(min).padStart(2, "0") + ":" + String(sec).padStart(2,"0");
    display.className = "fs-3";
}
// Timer 시작
startBtn.addEventListener("click", () => {
    // 1. 이미 동작 중인지 체크 (이제 정상 작동함)
    if (timerId !== null) {
        alert("이미 동작 중인 타이머가 있습니다!");
        return;
    }

    const minutes = Number(timeInput.value);
    if (!minutes || isNaN(minutes) || minutes <= 0) {
        alert("시간을 분 단위(숫자)로 입력하세요.");
        return;
    }

    remainingSeconds = minutes * 60;
    updateDisplay(); // 시작하자마자 화면 업데이트

    // 2. setInterval의 리턴값을 timerId에 저장! (핵심)
    timerId = setInterval(() => { 
        remainingSeconds--;

        // 3. 0초가 되면 타이머 종료 로직
        if (remainingSeconds <= 0) {
            resetTimer(); // 아래 종료 함수 정리
            alert("타이머가 종료되었습니다!");
        } else {
            updateDisplay();
        };
    }, 1000);
});

// 타이머 동작 멈춤
stopBtn. addEventListener("click", ()=> {
    clearInterval(timerId);
    timerId = null;
})

function resetTimer() {
    clearInterval(timerId);
    timerId = null;
}
