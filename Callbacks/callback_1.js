const evaluateNumber = (num, evenCallback, oddCallback) => {
    if (num % 2 === 0) {
        evenCallback();
    } else {
        oddCallback();
    }
};


evaluateNumber(5,
    () => console.log("The number is even!"),
    () => console.log("The number is odd!")
);