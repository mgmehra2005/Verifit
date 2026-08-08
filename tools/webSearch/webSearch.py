from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, SimpleJsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_tavily import TavilySearch

class WebSearch():
    def __int__(self):
        pass

    
    def queryToQuestion(self, idea: str):

        llm = ChatNVIDIA(
              model="meta/llama-3.3-70b-instruct",
              api_key="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", 
              temperature=0,
              top_p=0.7,
              timeout=300
            )

        queryTemplate = ChatPromptTemplate.from_template("""
        You are an expert web-research question generator for startup, product, business, and technology idea validation.

ROLE:
Convert the supplied idea into exactly 10 high-quality, web-searchable research questions.

INPUT:
The idea is provided through the LangChain variable {IDEA}.

LANGCHAIN SAFETY:

* This prompt is used with LangChain `PromptTemplate.from_template()` using the default f-string format.
* '{IDEA}' is the only permitted single-brace LangChain variable.
* Escape every other literal '{{' and '}}' as '{{' and '}}'.
* Do not introduce any other LangChain variables.
* Do not use literal single-brace examples.
* Do not create nested replacement fields.

TASK:
Generate exactly 10 distinct research questions divided into:

* 'social_media': 3 questions
* 'competitors': 3 questions
* 'web_articles': 4 questions

SOCIAL MEDIA:
Find qualitative evidence about real user problems, complaints, frustrations, workflows, recommendations, and alternatives.

Prioritize:

* Reddit
* Stack Overflow
* Quora
* Hacker News
* LinkedIn

Use search concepts such as:

* problems users Reddit
* complaints Reddit
* alternatives Reddit
* recommendations Reddit
* frustrated users Reddit

Adapt the searches to the supplied idea. Focus on concrete discussions and experiences, not social-media statistics or sentiment scores.

COMPETITORS:
Research the existing solution landscape.

Consider:

* competitors
* alternatives
* platforms
* startups
* direct and indirect solutions
* open-source solutions where relevant

The questions should identify existing solutions, how they work, relevant capabilities, documented limitations, and alternative approaches.

Do not focus on market size, market share, revenue, growth, or demand statistics.

WEB ARTICLES:
Find authoritative information relevant to building or validating the idea.

Prioritize:

* technical articles
* research papers
* academic sources
* official documentation
* engineering articles
* case studies
* regulatory or government sources
* standards

Focus on the most relevant combination of:

* underlying problem
* existing workflows
* technical feasibility
* implementation approaches
* technologies
* security or privacy
* legal or regulatory constraints
* usability
* documented challenges
* best practices

EXCLUSIONS:
Do not generate questions primarily about:

* market size
* TAM, SAM, or SOM
* market growth or CAGR
* demand statistics
* industry trends
* market forecasts
* competitor market share
* social-media audience or engagement statistics
* social-media sentiment analysis
* which features the market demands

QUALITY:

* Every question must be specific to the supplied idea.
* Every question must be independently searchable on the web.
* Prefer questions that can produce concrete evidence or sources.
* Avoid generic or overlapping questions.
* Questions should provide information useful for product, UX, business, or engineering decisions.
* Do not ask for reasoning or explanations.

OUTPUT:
Return only valid JSON with no Markdown, explanation, or additional text.

Use this structure:

{{
"idea": "{IDEA}",
"research_questions": {{
"social_media": [
{{"id": 1, "question": "..."}},
{{"id": 2, "question": "..."}},
{{"id": 3, "question": "..."}}
],
"competitors": [
{{"id": 4, "question": "..."}},
{{"id": 5, "question": "..."}},
{{"id": 6, "question": "..."}}
],
"web_articles": [
{{"id": 7, "question": "..."}},
{{"id": 8, "question": "..."}},
{{"id": 9, "question": "..."}},
{{"id": 10, "question": "..."}}
]
}}
}}

USER IDEA:
{IDEA}

        """)
        parser = SimpleJsonOutputParser()

        chain = queryTemplate | llm | parser

        print("Generating Questions....")
        questionSet = chain.invoke({"IDEA": idea})
        print("Query Generation Complete.")
        return questionSet

    @staticmethod
    def deduplicate_results(results):

        seen = set()
        unique = []

        for result in results:

            url = result.get("url")

            if url and url not in seen:
                seen.add(url)
                unique.append(result)

        return unique
    
    def webSearch(self, idea):
        print("Web Search Started.......")
        web_article_results = []
        social_media_results = []
        competitors_search_results = []

        search_tool = TavilySearch(
            max_results=5,
            topic="general",
            search_depth="advanced",
            include_raw_content=True,
        )

        # questionsSet = self.queryToQuestion(idea)
        questionsSet = {'idea': 'I wan to build a platform that analysis users face from live cam and perform deep face anlysis and tell what should user follow to make them look young', 'research_questions': {'social_media': [{'id': 1, 'question': 'What are common complaints about facial analysis apps on Reddit'}, {'id': 2, 'question': 'How do users on Quora recommend improving facial features to look younger'}, {'id': 3, 'question': 'What are frustrated users on LinkedIn discussing about current facial analysis technology'}], 'competitors': [{'id': 4, 'question': 'What facial analysis platforms are currently available for live cam analysis'}, {'id': 5, 'question': 'How do competitors like FaceApp perform deep face analysis and provide recommendations'}, {'id': 6, 'question': 'What are the limitations of existing facial analysis startups and their approaches'}], 'web_articles': [{'id': 7, 'question': 'What are the technical requirements for building a real-time facial analysis platform using deep learning'}, {'id': 8, 'question': 'How do researchers in academic papers approach the problem of facial aging and analysis'}, {'id': 9, 'question': 'What are the security and privacy concerns associated with collecting and analyzing facial data from live cams'}, {'id': 10, 'question': 'What are the best practices for implementing facial analysis in a user-friendly and accessible way'}]}}

        print("Performing Web Article Search....")
        # Web Article Search
        for i in questionsSet['research_questions']['web_articles']:
            response = search_tool.invoke({
            "query": i['question']
            })

            web_article_results.extend(response.get("results", []))

        print("Performing Social Search....")
        # Social Media Search
        for query in questionsSet['research_questions']['social_media']:

          response = search_tool.invoke({
              "query": query['question'],
              "include_domains": [
                  "reddit.com",
                  "stackoverflow.com",
              ]
          })   
          social_media_results.extend(response.get("results", []))

        print("Performing Competitors Search....")
        # Competitors
        for query in questionsSet['research_questions']['competitors']:

          response = search_tool.invoke({
              "query": query['question']
          })

          competitors_search_results.extend(response.get("results", []))

        print("Web Search Completed.......")
        print("Removing Duplicate Links......")
        deDupWebResult = self.deduplicate_results(web_article_results)
        deDupSmResult = self.deduplicate_results(social_media_results)
        deDupCompResult = self.deduplicate_results(competitors_search_results)
        print("Deduplication Completed......")

        with open("res.txt", "a") as f:
            f.write(f"['webSearch': {deDupWebResult}, 'socialMedia': {deDupSmResult}, 'competitors': {deDupCompResult}]")
        return [{'webSearch': deDupWebResult}, {'socialMedia': deDupSmResult}, {'competitors': deDupCompResult}]


    
if __name__ == "__main__":

    ws = WebSearch()
    idea = "I wan to build a platform that analysis users face from live cam and perform deep face anlysis and tell what should user follow to make them look young"

    print(ws.webSearch(idea)[2]['competitors'])
