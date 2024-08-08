from crewai import Agent
from tools import *
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"
##Create a senior blog content researcher

blog_researcher=Agent(
    role='Blog researcher from Youtube videos',
    goal='get the relevant video content for the topic {topic} from youtube channel',
    verbose= True,
    memory=True,
    backstory=("Expert in understanding videos in AI, Data Science, and Generative AI amd providing suggestions"),
    tools=[yt_tool],
    allow_delegation=True,
    llm=llm
)

##creating a senior blog writer agent with youtube tool
blog_writer=Agent(
    role='Writer',
    goal='Narrate compelling tech stories about the video {topic}',
    verbose=True,
    memory=True,
    backstory=(
      "With a flair for simplifying complex topics, you craft"
      "engaging narratives that captivate and educate, bringing new"
      "discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    allow_delegation=False
)