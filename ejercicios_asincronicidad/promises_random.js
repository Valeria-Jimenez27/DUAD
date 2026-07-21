const words = ["very", "dogs", "cute", "are"];

const delays = {
    "dogs": 100,
    "are": 200,
    "very": 300,
    "cute": 400
};

const result = [];

const promises = words.map(word => {
    return new Promise(resolve => {
        setTimeout(() => {
            result.push(word);
            resolve();
        }, delays[word]);
    });
});

Promise.all(promises).then(() => {
    console.log(result.join(" ").replace(/^\w/, c => c.toUpperCase()));
});