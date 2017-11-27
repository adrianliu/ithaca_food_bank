from foodbank import app

#every time DB schema changes: python|from foodbank import db|db.create_all()|exit()|sqlite3 database.db to check


if __name__ == '__main__':
    app.run(debug=True)
