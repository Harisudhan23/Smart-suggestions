import google.generativeai as generativeai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import os
from googleapiclient.discovery import build

os.environ['GOOGLE_API_KEY'] = "AIzaSyBzSFL43Im7fIv-UGD9WTV4RitWG4VQC0g"

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)

def smart_query_generate(transcript, context, titles):
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
        - **Hook**: Begin with a compelling question, bold statement, or data-driven insight to immediately capture attention.
        - **Tone**: Professional, informative and engaging.
        - **Content**: Craft a concise and insightful post that highlights key takeaways from the document. Provide a unique perspective or actionable insights that add value to the audience. Conclude with a thought-provoking call-to-action to encourage discussion and engagement.
        - **Format**: 3–4 short paragraphs with 2-5 relevant hashtags.

    - **Twitter**:
        - **Hook**: Open with an attention-grabbing statement, question, fact, or bold statement.
        - **Tone**: Concise, impactful,engaging and to the point.
        - **Content**: Create a tweet or a short thread that distills a critical insight from the document. Ensure clarity and engagement within the 280-character limit. Use relevant hashtags, emojis, and an optional link for further reading.
        - **Hashtags**: Use 2–3 relevant trending hashtags and relevant emoji to enhance engagement and maximize visibility.
        - **Format**: A single tweet or thread (1–2 tweets).

    - **Facebook**:
        - **Hook**: Start with an engaging question, bold statement, or relatable insight.
        - **Tone**: Conversational, friendly, informal style and relatable.
        - **Content**: Write a medium-length post that summarizes the document in a casual way. Include a question or call-to-action to invite comments.
        - **Format**: 2–3 paragraphs with relevant hashtags.

    - **Blog**:
        - **Hook**: Begin with a compelling question, bold statement, or surprising fact to draw in the reader.
        - **Tone**: Informative, Detailed, and educational.
        - **Content**: Create a well-structured blog post (500–600 words) that introduces the document’s key insights in an engaging and easy-to-digest manner. Utilize bullet points, numbered lists, or bold highlights to emphasize key insights for better readability. Use supporting data, case studies, or real-world examples where applicable. Provide a solution or actionable takeaway.
        - **SEO Optimization**: Naturally integrate relevant keywords for search visibility. Include a meta description summarizing the article and reference credible sources through internal and external links.
        - **Format**: Use clear subheadings for structure, keeping paragraphs concise (2–3 sentences each). Ensure a clear introduction, main body, and conclusion.

    - **Email**:
        - **Tone**: Personal, direct, and action-oriented.
        - **Subject Line**: Create a compelling subject line (max 8 words) that grabs attention.
        - **Personalization**: If possible, address the recipient by name for engagement.
        - **Introduction**: Start with a hook, question, or problem statement related to the content.
        - **Content**: Write a concise email that summarizes the document and ends with a strong and clear call-to-action (e.g., visiting a website, signing up, etc.).
        - **Closing**: Use a friendly and professional sign-off.
        - **Format**: Short introduction, body with key insights, and a clear CTA.

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
features for critical security even
"""

query = """Develop an in-depth blog post that explores the challenges and best practices of customer identity and access management. Showcase Infisign's solutions as a comprehensive approach to addressing these challenges and provide valuable insights for businesses seeking to enhance their user management capabilities.s
"""
websearch_result="""no web_search result 
"""

final_title = smart_query_generate(document, query, websearch_result)
print("final_title:", final_title)