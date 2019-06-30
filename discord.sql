CREATE TABLE IF NOT EXISTS "clean_message" (
	"id"	INTEGER,
	"timestamp"	TEXT,
	"user"	TEXT,
	"content"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "raw_message" (
	"id"	INTEGER,
	"timestamp"	TEXT,
	"user"	TEXT,
	"content"	TEXT,
	PRIMARY KEY("id")
);
