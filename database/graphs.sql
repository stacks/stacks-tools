CREATE TABLE "graphs" (
  "tag" VARCHAR PRIMARY KEY NOT NULL,
  "node_count" INTEGER,
  "edge_count" INTEGER,
  "total_edge_count" INTEGER,
  "chapter_count" INTEGER,
  "section_count" INTEGER,
  "use_count" INTEGER,
  "indirect_use_count" INTEGER
)
