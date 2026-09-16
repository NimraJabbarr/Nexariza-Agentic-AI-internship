"""
utils.py
--------
Small helpers shared by crew.py / app.py.
"""

import time
import functools


def retry_on_failure(max_attempts: int = 3, delay_seconds: int = 5):
    """Decorator: retries a function on exception (e.g. transient Groq/
    Tavily rate-limit or network errors) with a fixed delay between
    attempts. Re-raises the last exception if all attempts fail, so
    the caller (the Streamlit UI) can still show a real error message."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001 - intentional broad catch for retry
                    last_exc = exc
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
            raise last_exc

        return wrapper

    return decorator


def count_words(text: str) -> int:
    return len(text.split())


def count_numbered_insights(analysis_text: str) -> int:
    """Counts numbered-list items (1. / 1) / etc) in the Analyst's output.
    Falls back to counting markdown bullet lines if no numbered list found."""
    import re
    numbered = re.findall(r"^\s*\d+[\.\)]\s+", analysis_text, flags=re.MULTILINE)
    if numbered:
        return len(numbered)
    bullets = re.findall(r"^\s*[-*]\s+", analysis_text, flags=re.MULTILINE)
    return len(bullets)


def extract_pull_quote(report_text: str, max_words: int = 32) -> str:
    """Pulls one notable sentence from the Executive Summary (or the
    first substantial sentence if no such section) to use as a
    pull-quote under the headline. Best-effort — not guaranteed to be
    the 'most important' sentence, just a readable highlight."""
    import re
    lower = report_text.lower()
    idx = lower.find("executive summary")
    search_zone = report_text[idx:] if idx != -1 else report_text

    # drop markdown heading lines entirely before sentence-splitting. The
    # slice above can start mid-heading-line (since idx points at the word,
    # not the line start), so also drop the first line unconditionally when
    # we sliced mid-document.
    lines = search_zone.splitlines()
    if idx != -1 and lines:
        lines = lines[1:]  # remainder of the "Executive Summary" heading line itself
    body_lines = [ln for ln in lines if not ln.strip().startswith("#")]
    body = " ".join(body_lines)

    sentences = re.split(r"(?<=[.!?])\s+", body)
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        words = s.split()
        if 8 <= len(words) <= max_words:
            return s
    # fallback: first non-empty sentence anywhere (already heading-stripped above)
    for s in sentences:
        s = s.strip()
        if len(s.split()) >= 6:
            return " ".join(s.split()[:max_words])
    return ""


# Domains that usually indicate an academic/scholarly source
_ACADEMIC_HINTS = (".edu", "arxiv.org", "doi.org", "ncbi.nlm.nih.gov",
                    "scholar.google", "researchgate.net", "springer.com",
                    "sciencedirect.com", "nature.com", "ieee.org")
# Domains that usually indicate a mainstream news outlet
_NEWS_HINTS = ("reuters.com", "apnews.com", "bbc.", "cnn.com", "nytimes.com",
               "wsj.com", "bloomberg.com", "theguardian.com", "forbes.com",
               "techcrunch.com", "theverge.com", "wired.com", "finance.yahoo.com",
               "cnbc.com", "axios.com")


def classify_sources(research_text: str) -> list[dict]:
    """Extracts URLs from the Research Desk's output and tags each one
    Academic / News / Primary using a domain-keyword heuristic. This is
    explicitly a heuristic, not a verified classification — matches the
    disclaimer used in the reference UI."""
    import re
    urls = re.findall(r"https?://[^\s\)\]\"'>]+", research_text)
    seen, results = set(), []
    for url in urls:
        domain = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
        if domain in seen:
            continue
        seen.add(domain)
        if any(h in domain for h in _ACADEMIC_HINTS):
            tag = "ACADEMIC"
        elif any(h in domain for h in _NEWS_HINTS):
            tag = "NEWS"
        else:
            tag = "PRIMARY"
        results.append({"url": url, "domain": domain, "tag": tag})
    return results


def split_editions(published_markdown: str) -> dict:
    """Splits the Publisher's combined markdown output into
    {'linkedin': str, 'medium': str} using the '## LinkedIn Edition' /
    '## Medium Edition' headings the publishing task was told to use.
    Falls back gracefully if headings are missing/renamed."""
    linkedin, medium = "", ""
    lower = published_markdown.lower()
    # search for the heading marker itself (including "## ") so the split
    # point doesn't leave a stray "##" at the end of the first section
    li_idx = lower.find("## linkedin edition")
    md_idx = lower.find("## medium edition")
    if li_idx == -1:
        li_idx = lower.find("linkedin edition")
    if md_idx == -1:
        md_idx = lower.find("medium edition")

    if li_idx != -1 and md_idx != -1:
        if li_idx < md_idx:
            linkedin = published_markdown[li_idx:md_idx]
            medium = published_markdown[md_idx:]
        else:
            medium = published_markdown[md_idx:li_idx]
            linkedin = published_markdown[li_idx:]
    else:
        # Fallback: couldn't find clear headings, show everything as one block
        linkedin = published_markdown
        medium = published_markdown

    return {"linkedin": linkedin.strip(), "medium": medium.strip()}
