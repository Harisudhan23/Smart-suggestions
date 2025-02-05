import google.generativeai as generativeai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import os
from googleapiclient.discovery import build

os.environ['GOOGLE_API_KEY'] = "AIzaSyBzSFL43Im7fIv-UGD9WTV4RitWG4VQC0g"

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)

def smart_query_generate(document, query, titles):
    template1 = ('''
        "system", 
        """
        Given the query: '[query]' and the document '[Document]' and [websearch_result], identify the social media platform (LinkedIn, Twitter, Facebook, Blog, or Email) mentioned or implied in the query. Based on the identified platform, generate one tailored post for that platform, using content from the document and websearch_result for context. Follow these instructions for the post:

1. **Analyze the query**:
    - If the query is a random greeting (e.g., "hi", "hello") or unrelated to post generation, the knowledge base, or the content in websearch_result, respond strictly with:  
      **"The query is unrelated to post generation or the knowledge base. Please provide a relevant query."**
    - If the query is related to post generation, the document, or the websearch_result, proceed to step 2.
    - If the query is unrelated to both the document and websearch_result, respond strictly with:  
      **"The query is unrelated to post generation or the knowledge base. Please provide a relevant query."**

2. **Identify the social media platform**:
    - Based on the query, determine the social media platform mentioned or implied (LinkedIn, Twitter, Facebook, Blog, or Email).

3. **Generate a tailored post for the identified platform**:
    - Use content from the document and websearch_result for context. 
    - Generate the post for **only the identified platform** and not for all platforms.

4. **Post Formatting Instructions**:
    - **LinkedIn**:
        - **Hook**: Begin with a compelling question, bold statement, or data-driven insight that immediately grabs attention and sparks curiosity.
        - **Tone**: Keep it approachable yet professional, informative, and engaging tone that resonates with industry professionals.
        - **Content**: Craft a concise and insightful post that highlights key takeaways from the document. Provide unique actionable insights, expert perspectives, or actionable strategies that add value to the audience.
                       Incorporate real-world applications, relevant trends, or thought-provoking statements to encourage engagement.End with a strong call-to-action (e.g., asking for opinions, encouraging discussion, or suggesting next steps).
        - **Format**: 3–4 short, well-structured paragraphs for readability. Use concise language while maintaining depth and clarity. Include 2–5 relevant hashtags to optimize reach and engagement.

    - **Twitter**:
        - **Hook**: Start with a bold statement, thought-provoking question, surprising fact, or a concise data-driven insight to immediately capture attention.
        - **Tone**: Keep it concise, impactful, and engaging.
        - **Content**: Craft a single tweet or a short thread (1–2 tweets) that highlights a key insight from the document. Ensure clarity and engagement within the 280-character limit. Ensure it is easy to understand, thought-provoking, and encourages engagement (likes, shares, replies). Use relevant emojis to enhance readability and engagement.
        - **Hashtags**: Use 2–5 relevant, trending hashtags to boost discoverability. Ensure hashtags are contextually relevant to the topic. 
        - **Format**: A single tweet or a thread (1–2 tweets) for additional context or deeper insights.

    - **Facebook**:
        - **Hook**: Start with a compelling question, bold statement, or relatable insight to grab attention.
        - **Tone**: Keep it friendly, conversational, and engaging, making it easy for readers to relate.  Speak to the audience like you would a friend but maintain professionalism. Use contractions and informal language to make it feel natural.
        - **Content**: Write a medium-length post that summarizes the document in a casual way. Use a casual, storytelling approach to make the topic more engaging. 
                       Keep sentences short and direct for better readability. Add a question or call-to-action to spark conversation and encourage comments.
        - **Engagement boosters**: Use emojis to add personality and improve readability. Include hashtags (2–3 relevant ones) to increase visibility         
        - **Format**: 2–3 short paragraphs with natural flow. Line breaks for better readability.

    - **Blog**:
        - **Hook**: Begin with a compelling question, bold statement, or surprising fact that immediately captures attention.
        - **Tone**: Keep the tone informative, detailed, and educational while ensuring readability.
        - **Content**: Create a well-structured blog post (500–600 words) that introduces the document’s key insights in an engaging and easy-to-digest manner.Ensure clarity and logical flow from introduction to conclusion. Use a storytelling approach where applicable to enhance engagement. 
        - **Readability & Engagement**: Utilize bullet points, numbered lists, or bold highlights to emphasize important takeaways. Support claims with real-world examples, case studies, or relevant data to add credibility. Provide a clear solution or actionable takeaway that readers can implement.
        - **SEO Optimization**: Include a meta description summarizing the article and reference credible sources through internal and external links. Write a meta description summarizing the article concisely (150–160 characters). Include internal and external links to authoritative sources where appropriate.
        - **Format**: Use clear subheadings for easy navigation and readability, keeping paragraphs concise (2–3 sentences each). Ensure a strong conclusion that reinforces key takeaways and encourages engagement (e.g., a thought-provoking question or call to action).

    - **Email**:
        - **Tone**: Personal, direct, and action-oriented to make the reader feel valued and motivated to respond.
        - **Subject Line**: Max 8 words for clarity and impact. Use power words to create urgency or curiosity.(e.g., "Unlock Seamless CIAM Security Today!" or "Struggling with Identity Management?")
        - **Personalization**: Address the recipient by name if available (e.g., "Hi [First Name],"). Make the message relevant to their needs or pain points.
        - **Introduction**: Start with a hook, question, or relatable problem statement to immediately engage the reader. Keep it short and impactful to encourage further reading.
        - **Content**: Summarize the document’s key takeaways in 2–3 short paragraphs. Use bullet points or bold highlights for easy scanning. Maintain a logical flow from problem to solution.
        - **Closing**: End with a clear and compelling CTA. Make it actionable and time-sensitive to drive engagement. Use a friendly and professional sign-off (e.g., Best regards, Looking forward to your thoughts, Let’s chat soon!).
        - **Format**: Short introduction, body content with key insights, and a clear CTA.

5. **Ensure no direct references to the original source**:
    - Revise the tone of the content so that it no longer directly references the original source in any way.

6. Return the output in JSON format with the following structure:

                        {{
                            "platform": <platform_type>,
                            "body": <content>,
                            "sources": "List of websearch_results sources relevant to the generated title"

                        }}
    
                    Once the platform is identified, generate content tailored for that platform.
                    "document":{document}
                    "query":{query} 
                    "websearch_result":{websearch_result}

               """                                                        
                                    ''')
    
    prompt = ChatPromptTemplate.from_template(template1)
    
    chain = (
        {
            "document": RunnablePassthrough(),
            "query": RunnablePassthrough(),
            "websearch_result": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()  
    )
    
    answer = chain.invoke({"document": document, "query": query, "websearch_result": titles})
    print("answer",answer)
    parser = JsonOutputParser()
    response_data = parser.parse(answer)
    
    return response_data

document = """Infisign
Case Study on Customer Identity and Access
Management
Company Overview
Our Client is a leading sales enablement platform provider based in California that
streamlines your sales meeting research and access al relevant information in one
place. They have 4000+ customers and growing exponentialy and wanted their SSO
integration to be seamless for their enterprise customers
Challenges Faced:
● Complex User Schema Management: The client struggled with managing
evolving business needs and lacked a flexible framework for defining and
modifying user attributes of their customers
● Organization Management and Directory Sync: Existing organization
management processes were cumbersome, and directory synchronization
across multiple systems and multiple Users posed scalability chalenges.
● Lack of Comprehensive User Management Tools: The client lacked a
centralized user management console and APIs, leading to inefficiencies in
customer/user lifecycle management.
● Integration Complexity with Identity Providers: Integrating with various Single
Sign-On (SSO) providers and IDPs posed integration chalenges and hindered
seamless authentication experiences for their Customers/users.
● Audit and Compliance Monitoring: The absence of advanced audit logs and
reporting mechanisms hindered the Client and their customer’s ability to track
user activities and ensure compliance with regulatory requirements.
Confidential. Copyright and Al Rights Reserved to Infisign Inc.
Methodology:
User Schema Management:
● Infisign thoroughly analyzed Client and their customers’ user attribute
requirements and business objectives.
● Infisign provided a flexible user schema framework alowing for custom
definition, modification, and management of user attributes.
● Developed an intuitive interface and APIs for efficient schema
management, ensuring alignment with Client and their customers’
evolving business needs.
SAML2 and OpenID Discovery:
● Configuration of OpenID Connect discovery and endpoints.
● SetupofSAMLdiscovery services and endpoints.
● Infisign Provided Integration manuals for leveraging OpenID Connect
and SAML services to Facilitate easy integration with identity providers
for Client
Organization Management and Directory Sync:
Provided an intuitive organization management console and Provided a directory
sync with a scheduler feature configured for a single connection, with scalability
options.
Confidential. Copyright and Al Rights Reserved to Infisign Inc.
User Management Console and APIs:
● Provided a comprehensive user-friendly management console for an
admin-level user account, roles, and permissions management.
● Developed robust APIs to automate user management tasks,
supported by extensive documentation and SDKs for seamless
integration with Client existing systems.
Audit Logs and Reports:
● Infisign provided advanced audit logs and reporting features for
comprehensive tracking and compliance monitoring.
● Infisign provided transactional log export APIs for audit data
integration, pre-configured reports, dashboards, and real-time alerting
features for critical security even.
"""

query = """"Create an engaging Facebook post that introduces Infisign's CIAM services to a wider audience. Use visually appealing graphics and a conversational tone to explain the benefits of CIAM and how it can help businesses improve security and streamline operations. Include a link to Infisign's website for more information.
"""
websearch_result="""no web_search result 
"""

final_title = smart_query_generate(document, query, websearch_result)
print("final_title:", final_title)