// 객체 (object)
// 여러 값에 대해 이름(key)로 묶어서 관리하는 자료구조 
// python의 딕셔너리랑 유사

let user = {
    name: "alex",
    age: 40
}

console.log(user.name);
console.log(user["age"])
console.log(user.age)

user.name = "bob";
console.log(user.name)

for (const key in user) {
    console.log(key, user[key]);
}

console.log(user);
