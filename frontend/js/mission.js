// 과제 1. 콘솔 계산기
console.log("과제 1. 콘솔 계산기")

// 1. 덧셈
function add(n1, n2) { 
    let result = n1 + n2;
    console.log(result)
}

// 2. 뺄셈
function subtract(n1, n2) {
    let result = n1 - n2;
    console.log(result)
}

// 3. 곱셈
function multiply(n1, n2) { 
    let result = n1 * n2;
    console.log(result)
}

// 4. 나눗셈
function divide(n1, n2) { 
    if (n2 === 0) return "0으로 나눌 수 없습니다."; // 예외 처리
    let result = n1 / n2;
    console.log(result)
}

add(10, 5);      
subtract(10, 5); 
multiply(10, 5); 
divide(10, 5);   

console.log("---------------")
console.log("과제 2. 합격 여부 판별기")

// 과제 2. 합격 여부 판별기
function checkPass(score) {
    if (score>=60) {
        return console.log("합격입니다!");
    }else {
        return console.log("불합격입니다ㅠㅠ");
    };

}

checkPass(75);
checkPass(50);
