// // 지금까지 배운 JS 문법을 활용하는 실습

// function getAverage(scores) {
//     // 예외처리
//     if (scores.length ===0) {
//         return 0;
//     };

//     let sum=0;
//     for (const score of scores) {
//         sum += score
//     };
//     return sum / scores.length;
//     };


function getAverage(scores){
    let sum = 0;
    for (const score of scores) {
        sum += score
    };

    return sum / scores.length;

};




const scores = [80, 85, 92, 97];
const average = getAverage(scores)
console.log(average)



