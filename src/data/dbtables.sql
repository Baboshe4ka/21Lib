CREATE TABLE IF NOT EXISTS "books" (
	"id"	INTEGER UNIQUE,
	"title"	TEXT,
	"author"	TEXT,
	"publish_date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER UNIQUE,
	"first_name"	TEXT,
	"last_name"	TEXT,
	"user_name"	TEXT,
	"role"	TEXT DEFAULT 'user'
);

