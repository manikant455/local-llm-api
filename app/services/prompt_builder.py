class PromptBuilder:
    @staticmethod
    def seo_analysis(url: str) -> str:
        return f"""Analyze the SEO of this website: {url}

Provide:
1. Score out of 100
2. Top 3 issues
3. Top 3 improvements

Keep it short and actionable."""

    @staticmethod
    def code_review(code: str, language: str = "python") -> str:
        return f"""Review this {language} code and provide:
1. Bugs or issues
2. Performance improvements
3. Best practices violations

Code:
{code}

Keep response under 200 words."""

    @staticmethod
    def summarize(text: str) -> str:
        return f"""Summarize this text in 3 bullet points:

{text}"""

    @staticmethod
    def compare_models(prompt: str, model1: str, response1: str, model2: str, response2: str) -> str:
        return f"""Compare these two AI responses for the prompt: "{prompt}"

{model1}: {response1}

{model2}: {response2}

Which is better and why? Keep it brief."""
