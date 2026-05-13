const fs = require('fs');
const pdf = require('pdf-parse');

let dataBuffer = fs.readFileSync('output.pdf');

pdf(dataBuffer).then(function(data) {
    if (!data.text) {
        console.error("PDF is empty or cannot be parsed!");
        process.exit(1);
    }
    
    // Check if table 1 headers exist
    if (!data.text.includes("Access Tier")) {
        console.error("Error: Could not find 'Access Tier' table in PDF");
        process.exit(1);
    }

    // Check if table 2 headers exist
    if (!data.text.includes("Movable (Banknote)") && !data.text.includes("The \"Cash\" State")) {
        console.error("Error: Could not find 'Movable Banknote' table in PDF");
        process.exit(1);
    }

    console.log("SUCCESS: PDF output parsed correctly and tables are intact.");
}).catch(function(error){
    console.error("Error parsing PDF:", error);
    process.exit(1);
});
