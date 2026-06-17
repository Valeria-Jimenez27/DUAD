const celcius = [25, 32, 54, 70, 98, 100];
const fahrenheit = celcius.map(temp => (temp * 9/5) + 32);

console.log(fahrenheit);