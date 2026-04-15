// 배열 (Array)
// Python: 리스트(list)


// index: 배열의 순서
// let numbers = [10, 20, 30];
// console.log(numbers[0]);
// console.log(numbers[1]);
// console.log(numbers[2]);

let numbers = [15, 20, 30];


// console.log(numbers.at(-1));

// 배열 원소 갯수
// 3 - 1 = 2 -> numbers[2]
console.log(numbers[numbers.length -1])

// console.log(numbers[3])

console.log("==========")

let scores = [82, 95, 77]
// 배열의 데이터를 [인덱스, 값] 형태의 꾸러미(객체)로 변환해주는 함수
// index: value -> 0: 82 / 1: 95 / 2:77
for (const [i,score] of scores.entries()) {
    console.log(i + "번째 요소의 값:" + score);
};

// let data = ["hello", 100, true];
