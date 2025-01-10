const fs = require('fs');

// Step 1: Read the JSON file
fs.readFile('apps.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading the file:', err);
        return;
    }

    // Step 2: Parse the JSON data
    let jsonData;
    try {
        jsonData = JSON.parse(data);
    } catch (parseErr) {
        console.error('Error parsing the JSON data:', parseErr);
        return;
    }

    // Step 3: Remove duplicates based on the "Id" field
    const uniqueData = [];
    const seenIds = new Set();

    jsonData.forEach(item => {
        const trimmedId = item.Id.trim();  // Remove leading/trailing spaces from the "Id"
        if (!seenIds.has(trimmedId)) {
            seenIds.add(trimmedId);  // Mark this Id as seen
            uniqueData.push(item);    // Add the item to the result array
        }
    });

    // Step 4: Write the unique data back to the file
    fs.writeFile('apps.json', JSON.stringify(uniqueData, null, 2), (writeErr) => {
        if (writeErr) {
            console.error('Error writing to the file:', writeErr);
            return;
        }
        console.log('File updated successfully with unique entries.');
    });
});
