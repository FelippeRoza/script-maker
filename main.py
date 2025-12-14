import os
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config_loader import load_config
from app.llm_factory import get_llm
from app.pipeline import generate_scripts



def build_chains_and_config():
    config = load_config()
    # --- LLM config ---
    summarizer_llm = get_llm(config)
    writer_llm = get_llm(config)

    # --- summarize prompt setup ---
    summary_prompt_path = config['templates'].get('summary_prompt_path')
    summary_template = Path(summary_prompt_path).read_text()
    summary_prompt = ChatPromptTemplate.from_template(summary_template)
    summary_chain = summary_prompt | summarizer_llm | StrOutputParser()

    # --- writer prompt setup ---
    script_prompt_path = config['templates'].get('script_prompt_path')
    script_template = Path(script_prompt_path).read_text()
    script_prompt = ChatPromptTemplate.from_template(script_template)
    script_chain = script_prompt | writer_llm | StrOutputParser()

    return config, summary_chain, script_chain


def main():
    Path("scripts").mkdir(exist_ok=True)

    config, summary_chain, script_chain = build_chains_and_config()

    print("Crawling blog - generating scripts...")
    scripts = generate_scripts(config, summary_chain, script_chain)

    for s in scripts:
        title = s.get("title", f"post_{s['index']:02d}")
        safe_title = title[:30].replace(" ", "_")
        filename = f"scripts/script_{s['index']:02d}_{safe_title}.txt"

        with open(filename, "w") as f:
            f.write(f"Source: {s['url']}\n\n{s['script']}")

        print(f"Finished {filename}")

    print(f"Generated {len(scripts)} video scripts!")


if __name__ == "__main__":
    main()
