// 함수를 값처럼 다루기

// y = 2x + 1 -> 함수 정의 -> function sayHello() {}
// f(x) = 2x + 1 -> 함수 -> sayHello
// f(5) = 11 -> 함수 호출 -> sayHello()

// 함수를 정의
function sayHello() {
    console.log("Hello");
};

// 함수를 호출 (기능 실제로 사용) 
//sayHello()

// 1) 함수를 변수에 할당할 수 있다
const f = sayHello;
f();

// 2) 함수를 다른 함수의 인자로 전달 가능

function run(fn){
    console.log("start function run...")
    fn();
    console.log("end function run...")

}

// (기본) 함수를 선언한 곳에서 직접 호출
// (응용) 함수를 선언한 곳과 호출하는 곳이 달라짐


// 만약 run(sayHello()); 이렇게 하면?
run(sayHello());
// run(sayHello()) -> run(undefined); -> 에러 발생
