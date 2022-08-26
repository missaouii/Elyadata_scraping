db.createUser(
    {
        user: "ramzi",
        pwd: "ramzi",
        roles: [
            {
                role: "readWrite",
                db: "Elyadata"
            }
        ]
    }
)
db.createCollection('test_webscraping', { capped: false });