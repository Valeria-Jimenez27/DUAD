const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const evenNumbers = [];

for (const number of numbers) {
    if (number % 2 === 0) {
        evenNumbers.push(number);
    }
}
console.log(evenNumbers);