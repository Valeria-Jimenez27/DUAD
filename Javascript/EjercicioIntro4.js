const string = "Hola, este es mi primer string en JavaScript";  
const words = [];
let currentWord = "";

for(const word of string) {
    if (word === " ") {
        if (currentWord) {
            words.push(currentWord);
            currentWord = "";
        }
    } 
    else {
        currentWord += word;
    }
}   
if (currentWord) {
    words.push(currentWord);
}

console.log(words);
