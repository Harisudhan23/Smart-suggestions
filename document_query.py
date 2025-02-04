import google.generativeai as generativeai
import json
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser



os.environ['GOOGLE_API_KEY']="AIzaSyBzSFL43Im7fIv-UGD9WTV4RitWG4VQC0g"
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)

def generate_prompts_with_gemini(content):
    """
    Generate platform-specific prompts using Google's Gemini 1.5.

    Parameters:
        content (str): The document content to generate prompts from.
        api_key (str): Your Google Generative AI API key.

    Returns:
        dict: JSON object with prompts and AI-generated responses.
    """
    try:
        
# Define the primary prompt
        template = ("""
            f"Based on the following content:\n\n{content}\n\n"
            "Create five tailored prompts for the following platforms: LinkedIn, email, Facebook, Twitter, and blog post. "
            "Each prompt should instruct an AI to generate engaging content specific to the platform, adhering to its tone, style, and character limits."
            "Return the response in json format"
            """
        )
       
        prompt = ChatPromptTemplate.from_template(template)
        chain = (
            { "content": RunnablePassthrough()}
            | prompt
            | model
            | JsonOutputParser()
        )
        answer = chain.invoke(content)
        print(answer)
        return answer

    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    document_content = """Infisign
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
    response_json = generate_prompts_with_gemini(document_content)