// Regenerate src/data/memoContent.js from ai-scenarios-memo.md.
// The memo markdown is the single source; the internal HELD banner is
// replaced with the publication byline. Run: bun run build:memo
import { readFileSync, writeFileSync } from "node:fs";

const src = readFileSync("ai-scenarios-memo.md", "utf8").replace(
  `*Draft — HELD, not sent.*

*PolicyEngine · prepared with the AV Tax Policy Roundtable of 30 July 2026 in mind*`,
  "*July 30, 2026 · Max Ghenis*",
);

const banner =
  "// GENERATED from ai-scenarios-memo.md by scripts/build-memo-content.mjs — do not edit.\n";
const body = `export const memoMarkdown = ${JSON.stringify(src)};\n`;
writeFileSync("src/data/memoContent.js", banner + body);
console.log("src/data/memoContent.js written,", src.length, "chars");
