db = connect("mongodb://localhost:27017/jespy");

db.createCollection("stats");
db.createCollection("common");

db.common.insertOne({
    enabled: true,
    reply_text: "Your default reply text"
});

print("Initialization script completed.");
print("Hello from init.js");