import React from "react";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { memoMarkdown } from "../data/memoContent";

// The write-up lives in ai-scenarios-memo.md; src/data/memoContent.js is
// generated from it by `bun run build:memo`. This view only renders it.
function BudgetLabMemo() {
  return (
    <div className="section">
      <article className="memo-page">
        <nav className="memo-page-nav">
          <Link to="/income-shift">Interactive version of this analysis</Link>
        </nav>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {memoMarkdown}
        </ReactMarkdown>
      </article>
    </div>
  );
}

export default BudgetLabMemo;
