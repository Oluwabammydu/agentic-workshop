import os

from textwrap import dedent

from crewai import LLM, Agent, Crew, Task

# Explicitly set the AWS_REGION environment variable
os.environ['AWS_REGION'] = 'us-east-1'

# Load Claude from Amazon Bedrock
llm = LLM(model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0", temperature=0.7)


class TravelListicleAgents:
    def travel_researcher_agent(self):
        return Agent(
            role="Travel Researcher",
            goal="Research and compile interesting activities and attractions for a given location",
            backstory=dedent(
                """You are an experienced travel researcher with a knack for 
                discovering both popular attractions and hidden gems in any 
                location. Your expertise lies in gathering comprehensive 
                information about various activities, their historical 
                significance, and practical details for visitors."""
            ),
            allow_delegation=False,
            verbose=True,
            llm=llm,
        )

    def content_writer_agent(self):
        return Agent(
            role="Travel Content Writer",
            goal="Create engaging and informative content for the top 10 listicle",
            backstory=dedent(
                """You are a skilled travel writer with a flair for creating 
                captivating content. Your writing style is engaging, 
                informative, and tailored to inspire readers to explore new 
                destinations. You excel at crafting concise yet compelling 
                descriptions of attractions and activities."""
            ),
            allow_delegation=False,
            verbose=True,
            llm=llm,
        )

    def editor_agent(self):
        return Agent(
            role="Content Editor",
            goal="Ensure the listicle is well-structured, engaging, and error-free",
            backstory=dedent(
                """You are a meticulous editor with years of experience in 
                travel content. Your keen eye for detail helps polish articles 
                to perfection. You focus on improving flow, maintaining 
                consistency, and enhancing the overall readability of the 
                content while ensuring it appeals to the target audience."""
            ),
            allow_delegation=True,
            verbose=True,
            llm=llm,
        )
        
    def local_expert_agent(self):
        return Agent(
            role="Local Expert",
            goal="Provide insider tips and cultural context for the location",
            backstory="You are a long-time resident of the location with deep knowledge of its hidden gems and local customs.",
            allow_delegation=True,
            verbose=True,
            llm=llm,
        )    


class TravelListicleTasks:
    def research_task(self, agent, location):
        return Task(
            description=dedent(
                f"""Research and compile a list of at least 15 interesting 
                activities and attractions in {location}. Include a mix of 
                popular tourist spots and lesser-known local favorites. For 
                each item, provide:
                1. Name of the attraction/activity
                2. Brief description (2-3 sentences)
                3. Why it's worth visiting
                4. Any practical information (e.g., best time to visit, cost)

                Your final answer should be a structured list of these items.
                """
            ),
            agent=agent,
            expected_output="Structured list of 15+ attractions/activities",
        )
        
    def write_listicle_task(self, agent, location):
        return Task(
            description=f"Create an engaging top 15 listicle article about things to do in {location}. Include a mix of popular attractions and off-the-beaten-path experiences...",
            agent=agent,
            expected_output="Complete top 15 listicle article",
        )    

    def edit_listicle_task(self, agent, location):
        return Task(
            description=dedent(
                f"""Review and edit the top 10 listicle article about things to 
                do in {location}. Focus on:
                1. Improving the overall structure and flow
                2. Enhancing the engagement factor of the content
                3. Ensuring consistency in tone and style
                4. Correcting any grammatical or spelling errors
                5. Optimizing for SEO (if possible, suggest relevant keywords)

                Your final answer should be the polished, publication-ready 
                version of the article.
                """
            ),
            agent=agent,
            expected_output="Edited and polished listicle article",
        )


tasks = TravelListicleTasks()
agents = TravelListicleAgents()

print("## Welcome to the Travel Listicle Crew")
print("--------------------------------------")
location = input("What location would you like to create a top 10 listicle for?\n")

# Create Agents
travel_researcher = agents.travel_researcher_agent()
content_writer = agents.content_writer_agent()
editor = agents.editor_agent()
local_expert = agents.local_expert_agent()

# Create Tasks
research_location = tasks.research_task(travel_researcher, location)
write_listicle = tasks.write_listicle_task(content_writer, location)
local_content = tasks.write_listicle_task(local_expert, location)
edit_listicle = tasks.edit_listicle_task(editor, location)


# Create Crew for Listicle Production
crew = Crew(
    agents=[travel_researcher, content_writer, editor, local_expert],
    tasks=[research_location, write_listicle, local_content, edit_listicle],
    verbose=True,
)

listicle_result = crew.kickoff()

# Print results
print("\n\n########################")
print("## Here is the result")
print("########################\n")
print(f"Top 15 Things to Do in {location}:")
print(listicle_result)
