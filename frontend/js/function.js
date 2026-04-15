// 함수 (Function)
// -> 코드 재사용하기 위해 만든 구조

// 함수 선언 정의 -> "~기능을 하는 코드 덩어리를 X라는 이름으로 부르겠다"
// 함수 호출 (call) -> 함수를 사용한다
// 입력 -> 함수 동작 -> 출력
// function add(n1, n2) {
//     let result = n1 + n2;

//     // 함수 호출한 곳으로 함수의 실행 결과를 돌려줌
//     // return문 없으면 undefined로 나옴;
//     //return -> 결과값을 반환 & 함수 종료 
     
//     // console.log(result)
// }

// 함수 호출(call) -> 함수 사용
// console.log(add(1,2));

function add(n1,n2) {
    return n1 + n2
}

console.log(add(3,5))

