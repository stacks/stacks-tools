CREATE TABLE "changes" (
  "tag" VARCHAR NOT NULL,
  "commit" VARCHAR NOT NULL,
  "file" VARCHAR NOT NULL,
  "begin" INTEGER,
  "end" INTEGER,
  "type" VARCHAR
);
