const student = {
    name: "John Doe",
    grades: [
        { name: "math", grade: 80 },
        { name: "science", grade: 100 },
        { name: "history", grade: 60 },
        { name: "PE", grade: 90 },
        { name: "music", grade: 98 }
    ]
}
const total = student.grades.reduce((accumulator, subject) => accumulator + subject.grade, 0);
const gradeAvg = total / student.grades.length;

const highest = student.grades.reduce((best, subject) =>
    subject.grade > best.grade ? subject : best
);

const lowest = student.grades.reduce((worst, subject) =>
    subject.grade < worst.grade ? subject : worst
);

const result = {
    name: student.name,
    gradeAvg: gradeAvg,
    highestGrade: highest.name,
    lowestGrade: lowest.name
}

console.log(result);