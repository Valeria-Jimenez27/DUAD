const fs = require("fs");

const findRepeatedWords = (file1, file2, callback) => {

    fs.readFile(file1, "utf8", (err, data1) => {
        if (err) return callback(err);
        fs.readFile(file2, "utf8", (err, data2) => {
            if (err) return callback(err);
            const words1 = data1.split("\n").map(w => w.trim()).filter(w => w);
            const words2 = data2.split("\n").map(w => w.trim()).filter(w => w);

            const repeated = words1.filter(word => words2.includes(word));
            callback(null, repeated);
        });
    });
};

findRepeatedWords("file1.txt", "file2.txt", (err, repeated) => {
    if (err) return console.log("Error:", err.message);
    console.log("Hidden message:", repeated.join(" "));
});