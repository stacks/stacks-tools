CREATE VIRTUAL TABLE "tags_search" USING fts3(tag, text, text_without_proofs)
