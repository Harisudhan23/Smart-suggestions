from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

API_KEY = "#API_KEY"
LLM_MODEL = "gemini-pro"  # Replace with the appropriate model name

prompt_template = PromptTemplate(
    template='''
        You are an intelligent assistant responsible for analyzing and assigning titles to content and creating tailored prompts for various platforms. Follow these guidelines:
                    
        1. **Title Generation**:
        - If the "titles" variable is null or empty:
            - Analyze the "context" and "transcript".
            - Generate a single common title that is meaningful and relevant to both "context" and "transcript".
        - If the "titles" variable contains one or more titles:
            - For each title, compare it with the "context" and "transcript".
            - If the title is closely related to both "context" and "transcript", retain that title.
            - If the title is not related to both "context" and "transcript", generate a new title that is meaningful and related to both.

        2. **Title Matching**:
        - After generating the title for the "context" and "transcript":
            - Check if the generated title is already present in the "titles" list.
            - If the title is in the "titles" list, set the variable `matching_title` to `True`.
            - If the title is not in the "titles" list, set `matching_title` to `False`.

        3. **Prompt Creation for Platforms**:
        - Based on the provided "context", "transcript", and "titles":
            - Create five tailored prompts for the following platforms: LinkedIn, email, Facebook, Twitter, and a blog post.
            - Each prompt should instruct an AI to generate engaging content specific to the platform, adhering to its tone, style, and character limits.
            - Return the response in a JSON format.

        4. **Conditional Output**:
        - If `matching_title` is `True`:
            - Do not include the `titles` fields in the output.
            - Strictly don't add titles if the matching titles are True.
        - If `matching_title` is `False`:
            - Provide the following fields in the output:
                - `"titles"`: Include the generated title.
                - `"platform_prompts"`: Create five tailored prompts for the following platforms: LinkedIn, email, Facebook, Twitter, and a blog post.
    ''',
    input_variables=["context", "transcript", "titles"]
)

# Initialize LLM
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=API_KEY)

# Example usage
context = "AI content generation for social media."
transcript = "This session explores how AI can generate content for different platforms."
titles = []  # Empty list means new title should be generated

formatted_prompt = prompt_template.format(
    context=context, transcript=transcript, titles=titles
)

response = llm.invoke(formatted_prompt)
print(response)
