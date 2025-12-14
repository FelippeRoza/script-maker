from .crawler import load_posts


def generate_scripts(config, summary_chain, script_chain):
    """Pipeline:
        Load posts
        Summarize with summarizer LLM
        Write script with writer LLM
    """
    topic = config['pipeline']['topic']
    start_url = config['pipeline']['start_url']
    max_posts = config['pipeline']['max_posts']

    docs = load_posts(start_url, max_posts)
    scripts = []

    for i, doc in enumerate(docs):
        # --- Step 1: Summarize blog post ---
        summary_input = {"topic": topic, "content": doc.page_content[:4000]}
        summary_text = summary_chain.invoke(summary_input)

        # --- Step 2: Generate video script ---
        script_input = {
            "topic": topic,
            "summary": summary_text,
            "source_url": doc.metadata.get("source_url", "unknown")
        }
        script_text = script_chain.invoke(script_input)

        scripts.append({
            "index": i,
            "url": script_input["source_url"],
            "summary": summary_text.strip(),
            "script": script_text.strip(),
        })

    return scripts
