CREATE TABLE "tags" (
  "tag" VARCHAR PRIMARY KEY NOT NULL,
  "label" VARCHAR,
  "reference" TEXT,
  "file" VARCHAR,
  "chapter_page" INTEGER,
  "book_page" INTEGER,
  "type" VARCHAR,
  "book_id" VARCHAR,
  "value" TEXT,
  "active" BOOL NOT NULL DEFAULT TRUE,
  "name" VARCHAR,
  "position" INTEGER,
  "creation_date" DATETIME,
  "creation_commit" VARCHAR,
  "modification_date" DATETIME,
  "modification_commit" VARCHAR,
  "begin" INTEGER,
  "end" INTEGER
);

