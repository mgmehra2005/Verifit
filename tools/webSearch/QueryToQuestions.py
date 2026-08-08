from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, SimpleJsonOutputParser
from langchain_core.runnables import RunnableLambda

class WebSearch():
    def __int__(self):
        pass

    
    def queryToQuestion(self, idea: str):

        llm = ChatNVIDIA(
        model="meta/llama-3.2-3b-instruct",
        api_key="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", 
        temperature=0,
        top_p=0.7,
        max_tokens=1024,
        )

        queryTemplate = ChatPromptTemplate.from_template("""You are a professional web-research question-generation agent.

INPUT:
The user will provide a business/product/startup/technology idea.

TASK:
Analyze the idea and generate exactly 10 highly specific questions that can be searched on the web to gather actionable information for understanding, validating, designing, and improving the idea.

IMPORTANT:
- Return ONLY a valid JSON array.
- Do not include markdown, explanations, commentary, headings, or additional text.
- Generate exactly 10 questions.
- Every item must be a complete, specific, web-searchable question.
- Questions must be directly relevant to the provided idea.
- Avoid generic questions that could apply to any business.
- Questions should target information that can realistically be found through web research.
- Prefer questions that uncover concrete evidence, user problems, existing solutions, technical approaches, regulations, workflows, use cases, implementation considerations, risks, and unmet needs.
- Make each question meaningfully different from the others.
- Do not combine multiple unrelated research objectives into one question.

STRICT EXCLUSIONS:
Do NOT generate questions about:
1. Market size, TAM, SAM, SOM, or industry size.
2. Industry trends or general market trends.
3. Market growth rates, CAGR, demand statistics, or market-growth forecasts.
4. Customer demand statistics or industry-wide demand statistics.
5. Competitors for the specific idea.
6. Competitor limitations, competitor weaknesses, or competitor feature gaps.
7. Which new features the market currently demands.
8. Audience/customer reviews, opinions, sentiment, or discussions on social media.
9. Social-media audience behavior, comments, posts, reviews, or sentiment analysis.
10. Questions whose primary purpose is estimating market opportunity or validating market demand through statistics.

Instead, focus on research dimensions such as:
- Specific user problems and pain points documented online.
- Existing workflows and how people currently solve the underlying problem without focusing on named competitors.
- Common use cases and real-world scenarios.
- User requirements and expectations documented in forums, documentation, communities, articles, surveys, or research papers, excluding social-media reviews/sentiment.
- Technical feasibility and implementation approaches.
- Relevant technologies, APIs, frameworks, architectures, datasets, or protocols.
- Industry standards and best practices relevant to building the solution.
- Legal, regulatory, privacy, security, compliance, or ethical requirements.
- Common failure modes and implementation challenges.
- Accessibility, usability, integration, deployment, and operational requirements.
- Academic research or credible studies explaining the underlying problem or technology.
- Existing open-source approaches, reference implementations, or technical solutions, without framing them as competitors.
- Domain-specific processes, terminology, constraints, and dependencies.
- Features or capabilities that are technically necessary based on documented workflows or user problems, rather than based on market-demand claims.

QUESTION QUALITY RULE:
Each question should produce information that can directly influence a decision about the idea. A strong question should help answer:
"What do we need to know before building, designing, validating, or deploying this idea?"

OUTPUT FORMAT:
[
  {
    "id": 1,
    "question": "..."
  },
  {
    "id": 2,
    "question": "..."
  },
  {
    "id": 3,
    "question": "..."
  },
  {
    "id": 4,
    "question": "..."
  },
  {
    "id": 5,
    "question": "..."
  },
  {
    "id": 6,
    "question": "..."
  },
  {
    "id": 7,
    "question": "..."
  },
  {
    "id": 8,
    "question": "..."
  },
  {
    "id": 9,
    "question": "..."
  },
  {
    "id": 10,
    "question": "..."
  }
]

Before producing the JSON, internally check every question against the exclusion list. If a question overlaps with market size, market growth, demand statistics, competitors, competitor weaknesses, market-demanded features, or social-media reviews/sentiment, replace it with a question from an allowed research dimension.

USER IDEA:
{{IDEA}}""")
        parser = StrOutputParser()

        chain = queryTemplate | llm | parser

        questionSet = chain.invoke({'IDEA': idea})
        return questionSet
        

if __name__ == "__main__":

    ws = WebSearch()
    idea = "I wan to build a platform that analysis users face from live cam and perform deep face anlysis and tell what should user follow to make them look young"
    print(ws.queryToQuestion(idea))
