"""
Version 1: CrewAI Implementation
Role-based agents executing tasks sequentially
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from pipelines.crewai_workflow.src.shared_tools import research_topic, generate_content
from shared.utils.llm_utils import DEFAULT_MODEL
import time

load_dotenv()


def run_crewai_version(topic="Create a Work From Home policy for US-based tech companies"):
    """
    CrewAI approach: Define agents with roles, create tasks, run crew.
    
    Architecture:
    - 4 Agents (HR Analyst, Writer, Compliance Officer, Editor)
    - 4 Tasks (Research, Draft, Review, Finalize)
    - Sequential execution
    """
    
    print("\n" + "="*70)
    print("CREWAI VERSION: Role-Based Sequential Agents")
    print("="*70 + "\n")
    

    # Initialize LLM with Groq via CrewAI's native LLM
    llm = LLM(
        model=os.getenv("CREWAI_MODEL", f"groq/{DEFAULT_MODEL}"),
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Define Agents with roles
    hr_analyst = Agent(
        role="Policy Research Analyst",
        goal="Research best practices, regulations, and requirements for the requested policy topic",
        backstory=(
            "You are a senior policy research analyst with 15 years of experience "
            "researching workplace policies, labor laws, and regulatory requirements "
            "across multiple industries and regions. You use web search to find "
            "current, accurate information rather than relying on assumptions."
        ),
        tools=[research_topic, generate_content],
        llm=llm,
        verbose=True
    )

    policy_writer = Agent(
        role="Policy Writer",
        goal="Write clear, structured, and actionable policy documents based on research",
        backstory=(
            "You are a professional policy writer who creates company-ready "
            "documents. You excel at translating research into clear, "
            "implementable policies that employees can understand and follow."
        ),
        tools=[research_topic, generate_content],
        llm=llm,
        verbose=True
    )

    compliance_officer = Agent(
        role="Compliance & Legal Reviewer",
        goal="Review policies for compliance gaps, legal risks, and security vulnerabilities",
        backstory=(
            "You are a detail-oriented compliance officer with expertise in "
            "legal requirements, data protection laws, and risk management. You "
            "identify gaps that could expose the company to legal or security risks."
        ),
        tools=[research_topic, generate_content],
        llm=llm,
        verbose=True
    )

    editor = Agent(
        role="Policy Editor & Formatter",
        goal="Finalize policy documents into polished, professional, shareable format",
        backstory=(
            "You are an editor who produces publication-ready documents. You "
            "ensure consistency, clarity, and professional formatting that "
            "reflects well on the organization."
        ),
        tools=[research_topic, generate_content],
        llm=llm,
        verbose=True
    )

    # Define Tasks
    research_task = Task(
        description=(
            f"Research and compile key points for the following request: {topic}\n\n"
            "Use the research_topic tool to search the web for current, accurate information.\n"
            "Search for:\n"
            "- Current best practices and standards\n"
            "- Legal and regulatory requirements\n"
            "- Common implementation approaches\n"
            "- Real examples from similar organizations\n\n"
            "Do multiple searches to gather comprehensive information. "
            "Compile everything into well-organized research points."
        ),
        agent=hr_analyst,
        expected_output="Detailed research points with sources covering all relevant aspects of the topic"
    )

    draft_task = Task(
        description=(
            "Using the research output, draft a complete structured policy document.\n\n"
            "Requirements:\n"
            "- Clear numbered sections with headers\n"
            "- Purpose and scope statements\n"
            "- Actionable guidelines for each area\n"
            "- Logical flow from eligibility to review process\n"
            "- Specific, implementable rules not vague guidelines\n\n"
            "Use the generate_content tool if you need help structuring specific sections. "
            "Create a complete draft ready for compliance review."
        ),
        agent=policy_writer,
        expected_output="Complete structured policy document with numbered sections",
        context=[research_task]
    )

    compliance_task = Task(
        description=(
            "Review the draft policy and provide compliance feedback.\n\n"
            "Use the research_topic tool to verify any legal or regulatory requirements.\n"
            "Check for:\n"
            "- Legal compliance gaps\n"
            "- Security vulnerabilities\n"
            "- Missing clauses (confidentiality, disciplinary actions)\n"
            "- Risk mitigation opportunities\n"
            "- Data protection requirements\n\n"
            "Provide specific, actionable compliance notes with required additions."
        ),
        agent=compliance_officer,
        expected_output="Detailed compliance review notes with specific required additions",
        context=[draft_task]
    )

    finalize_task = Task(
        description=(
            "Create the final, polished version of the policy document.\n\n"
            "Requirements:\n"
            "- Professional formatting with clear section headers\n"
            "- Incorporate all compliance feedback from the review\n"
            "- Include document metadata (version, effective date, policy owner)\n"
            "- Add disclaimer and contact information\n"
            "- Ensure publication-ready quality\n\n"
            "This is the final document that will be distributed."
        ),
        agent=editor,
        expected_output="Final formatted policy document ready for distribution",
        context=[draft_task, compliance_task]
    )
    
    # Create Crew
    crew = Crew(
        agents=[hr_analyst, policy_writer, compliance_officer, editor],
        tasks=[research_task, draft_task, compliance_task, finalize_task],
        process=Process.sequential,  # Tasks execute in order
        verbose=False
    )
    
    # Execute
    print("\n🚀 Starting CrewAI execution...\n")
    max_retries = 3
    result = None
    for attempt in range(max_retries):
        try:
            result = crew.kickoff()
            break
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait_time = 30 * (attempt + 1)
                print(f"\n⏳ Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
            else:
                raise

    print("\n" + "="*70)
    print("CREWAI RESULT")
    print("="*70)
    print(result)
    print("="*70 + "\n")

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Join all command line arguments as the topic
        topic = " ".join(sys.argv[1:])
        result = run_crewai_version(topic=topic)
    else:
        # Run with default topic
        result = run_crewai_version()
