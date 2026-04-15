// python: if xxx : else:
// JS: if / else if / else

// let age = 20;

// if (age>=19) {
//     console.log("성인");
// } else if (age >=8) {
//     console.log("학생");
// }else {
//     console.log("어린이");
// };

// let age = 29;

// if (age<=19) {
//     console.log("10대");
// } else if (age <=29) {
//     console.log("20대");
// } else if (age <=39) {
//     console.log("30대")
// } else {}

// true: 50, 1, -1, "100", "0"
// false: false, 0, "", null, undefined, NaN -> 타입 다 다름
let score = "0";

if (score) {
    console.log("점수: " + score)
} else {
    console.log("점수 없음");
}