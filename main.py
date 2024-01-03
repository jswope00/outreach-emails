import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

template_base_job = """
Write a very short outreach email to a hiring manager. The email should be no longer than 100 words total. This person is looking for a person to fill their position but I'd like to offer myself as a capable temporary consultant that can either fill the role or help in some other way. 

Most importantly, this email should address they KEY MESSAGE provided below. 
"""

template_base_grant = """
Write a very short outreach email to a person that is the lead researcher for a research grant. The email should be no longer than 100 words total. I'd like to position myself as a competent course-builder who can help them build courses as part of their grant activities. 

Most importantly, this email should address they KEY MESSAGE provided below. 
"""

template_tone = """

The email should incorporate some of the following elements:
Friendly Introduction: Starting with a casual greeting and acknowledging the recipient's current activities or needs.
Professional Background: Highlighting your extensive experience in a specific field, emphasizing key areas of expertise. I have included a list of my key expertise below.
Offer of Support: Expressing willingness to assist, collaborate, or share ideas, even if not directly applying for the role.
Community Involvement: Mentioning your role in a relevant professional community, indicating your willingness to engage and share knowledge.
Invitation to Collaborate: Offering an opportunity for the recipient or their team to join a community or event, fostering professional networking and growth. 
Personalized Sign-Off: Maintaining a friendly and approachable tone until the end of the email.

The email should NOT be salesy. It should not use big words. And it should focus more on making a personal connection in order to elicit a phone call or connection on LinkedIn, rather than directly a hire. 

"""

template_expertise = """

My key expertise:
- I've spent the last 10 years working on Open edX courses
- I am adept at building exciting games and other interactives for online courses. 
- I've got a team of people who can support all aspects of course creation. From instructional design to media creation like videos and infographics. 
- I understand how to read and leverage data especially in large online courses. 
- The courses we build are exceptionally aesthetically pleasing. 
- I chair the Open edX Educators working group. It's a community of practice for educators who build courses on Open edX. Very good way to share and learn how others are being creative with the platform. I'd love to invite you or your new hire to an upcoming session! 

"""

template_details_job = """
Here are the details I know about the job and the contact: 
JOB: {job}
KEY MESSAGE: {pain}
HIRING MANAGER NAME: {name}
HIRING MANAGER TITLE: {job_title}

"""

template_details_grant = """
Here are the details I know about the grant and the contact: 
GRANT DETAILS: {job}
KEY MESSAGE: {pain}
LEAD RESEARCHER NAME: {name}
LEAD RESEARCHER TITLE: {job_title}

"""

template_job = """

And here is a starter template that is indicative of my style and tone: 

Hi [LEAD RESEARCHER NAME],

I came across your posting for [JOB] and wanted to reach out. I hope your search for candidates is going well!

Over the past 10 years, I've been deeply involved in [specific area of expertise or platform, e.g., Open edX], focusing on [key aspects of your work, e.g., building courses, customizing platforms, integrating third-party tools]. My work includes [mention any specific projects or achievements, e.g., creating custom assessments, games, and simulations].


All the best,
John

"""

template_grant = """

And here is a starter template that is indicative of my style and tone: 

Hi [Recipient's Name],

I came across your [grant award]. 

Over the past [number of years] years, I've been deeply involved in [specific area of expertise or platform, e.g., Open edX], focusing on [key aspects of your work, e.g., building courses, customizing platforms, integrating third-party tools]. My work includes [mention any specific projects or achievements, e.g., creating custom assessments, games, and simulations].

If you ever want some support building out any online instructional materials or just want to bounc ideas off someone, don't hesitate to reach out.

Here is my Linkedin: https://www.linkedin.com/in/johnpswope00/
And website: https://johnswope.com/

All the best,
[Your Name]

"""

job_prompt = PromptTemplate(
	input_variables = ["job","name","job_title"],
	template=template_base_job + template_tone + template_expertise + template_details_job,
	)

grant_prompt = PromptTemplate(
	input_variables = ["job","name","job_title"],
	template=template_base_grant + template_tone + template_expertise + template_details_grant,
	)

template_shorten_job = """
	Take this text and summarize it in 50 words or less, focusing especially on the parts about online courses, online learning, or Open edX if applicable:

	TEXT: {job}
	"""

shorten_job_prompt = PromptTemplate(
	input_variables=["job"],
	template=template_shorten_job,
	)

#Access the API key
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
	print("OpenAI API Key not found. Please set it as an environment variable")
else:
	def load_LLM():
		"""Logic for laoding the chain you want to use should go here."""
		llm=OpenAI(temperature=.5)
		return llm

	llm=load_LLM()

st.set_page_config(page_title="Email Outreach", page_icon=":robot:")
st.header("Email Outreach Builder")

st.markdown("This will allow a user to input some details about an opportunity and get an email output draft.")

st.markdown("## Enter Opportunity Details")

option_type = st.selectbox(
	'What kind of opportunity is this?',
	('Job Posting', 'Grant'))

def get_job():
	input_text=st.text_area(label="Core job description", placeholder="Paste the core description of the opportunity here, to give the system context about the opportunity", key="job_desc")
	return input_text

job_desc = get_job()

def get_pain():
	input_text=st.text_area(label="Key Emphasis", placeholder="Write 1 or 2 sentences that the email should focus on. What can we offer this person?", key="pain_point")
	return input_text

pain_point = get_pain()

def get_name():
	input_text=st.text_area(label="Contact Name", placeholder="Opportunity Contact Name", key="contact_name")
	return input_text

contact_name = get_name()

def get_title():
	input_text=st.text_area(label="Contact's Title", placeholder="The title of the HIRING MANAGER. Not the title being hired.", key="contact_title")
	return input_text

contact_title = get_title()


if option_type=="Job Posting" and st.button('Submit'):
	shorten_job_desc = shorten_job_prompt.format(job=job_desc)
	short_job_desc = llm(shorten_job_desc)
	st.write(short_job_desc)
	email_prompt = job_prompt.format(job=short_job_desc,name=contact_name,job_title=contact_title,pain=pain_point)
	email_returned = llm(email_prompt)
	st.write(email_returned)
elif option_type=="Grant" and st.button('Submit'):
	shorten_job_desc = shorten_job_prompt.format(job=job_desc)
	short_job_desc = llm(shorten_job_desc)
	st.write(short_job_desc)
	email_prompt = grant_prompt.format(job=short_job_desc,name=contact_name,job_title=contact_title,pain=pain_point)
	email_returned = llm(email_prompt)
	st.write(email_returned)

