// Import sql.js library
importScripts('https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.7.3/sql-wasm.js');

let db = null; // Initialize SQLite database variable

// Function to create SQLite database and table
function createDatabase() {
    // Initialize SQLite database
    db = new SQL.Database();

    // Create a table named 'user_feedbacks'
    db.run(`
        CREATE TABLE IF NOT EXISTS user_feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback TEXT
        )
    `);
}

// Function to insert feedback into the SQLite database
function insertFeedback(feedback) {
    // Ensure database is initialized
    if (!db) {
        console.error("Database is not initialized!");
        return;
    }

    // Insert feedback into 'user_feedbacks' table
    db.run('INSERT INTO user_feedbacks (feedback) VALUES (?)', [feedback]);
}

// Create SQLite database on extension start
createDatabase();

// Listen for messages from your extension
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action == "insert_feedback") {
        // Insert feedback into the SQLite database
        insertFeedback(message.feedback);
        console.log("Feedback inserted into the database:", message.feedback);
    }
});
