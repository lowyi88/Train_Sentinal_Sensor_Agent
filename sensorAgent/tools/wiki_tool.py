from langchain_openai import ChatOpenAI
import wikipedia
from langchain_core.messages import HumanMessage, SystemMessage

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def wiki_tool(content) -> str:
    """Search Wikipedia and retrieve article content"""
    print(f"content:{content}")
    search_term = generate_wiki_search_term(content)
    print(f"search_term: {search_term}")
    try:
        # Search for articles
        results = wikipedia.search(search_term)
        if not results:
            return f"No Wikipedia articles found for '{search_term}'"

        # Get the first result
        first_result = results[0]
        page = wikipedia.summary(first_result, auto_suggest=False)
        print(page)
        # Return the content (you can also access page.summary for a shorter version)
        return page
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation pages
        return f"Multiple options found: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return f"Page not found for '{search_term}'"
    except Exception as e:
        return f"Error: {str(e)}"
    
def generate_wiki_search_term(topic: str) -> str:
    llm = ChatOpenAI(model="gpt-5-mini", temperature=1)

    system_prompt = ""
    user_prompt = """Given the chunk of text in the next paragraph, identify the primary topic and generate the most relevant Wikipedia search term. Only respond with the search term.
        {topic}"""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    # response = client.responses.create(
    #     model="gpt-5",
    #     input=f"""Given the chunk of text in the next paragraph, identify the primary topic and generate the most relevant Wikipedia search term. Only respond with the search term.
    #     {topic}"""
    # )
    #print(response.output[1].content[0])

    return response.output[1].content[0].text