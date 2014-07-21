CREATE TABLE "slogans" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
  "slogan" TEXT NOT NULL,
  "tag" VARCHAR NOT NULL,
  "author" VARCHAR NOT NULL,
  "email" VARCHAR NOT NULL,
  "date" DATETIME DEFAULT CURRENT_TIMESTAMP
);
