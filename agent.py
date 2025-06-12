from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from IPython.display import Image, display
from api import get_commits

# 1. Define the state
class ScrumState(MessagesState):
    commits: Optional[List[dict]]
    commit_summaries: Optional[List[str]]
    scrum_report: Optional[str]

# 2. LLM Setup
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Helper to maintain state and messages
def update_state(state, **kwargs):
    return {
        **state,
        "messages": state["messages"],  # ensure messages is preserved
        **kwargs
    }

# 4. Mocked commit fetch
def get_mock_commits(state: ScrumState):
    commits = get_commits()
    print(f"Found {len(commits)} commits")
    print("Sample commits:")
    print(type(commits['Hari2k3']))  # Show first 3 commits for brevity
    # for i, commit in enumerate(commits[:3], 1):  # Show first 3 commits
    #     print(f"{i}. {commit['message']} by {commit['author']} on {commit['date']}")
    commitList = []
    for author, commit_data in commits.items():
        for commit in commit_data:
            commitList.append({
                "id": commit['sha'],
                "message": commit['message'],
                "author": author,
                "date": commit['date'],
                "url": commit['url'],
                "patches": commit['patches'],
            })
    return update_state(state, commits=commitList)

# 5. Mock diff function
def get_mock_diff(commit_id: str):
    # commitData = get_commits()
    for author, commit_data in state["commits"].items():
        for commit in commit_data:
            if commit['sha'] == commit_id:
                return commit['patches'] if commit['patches'] else ""


# 6. Structured model for commit summary
class CommitSummary(BaseModel):
    summary: str = Field(description="Summary of the commit in 3-4 sentences.")

def summarize_commits(state: ScrumState):
    summaries = []
    for commit in state["commits"]:
        prompt = f"""
        Commit by {commit['author'] if commit['author'] else "Unknown Author"} on {commit['date']}:
        Message: {commit['message'] if commit['message'] else "No message available"}
        Diff: {"| ".join(commit['patches']) if commit['patches'] else "No diff available"}
        """
        output = llm.with_structured_output(CommitSummary).invoke([HumanMessage(content=prompt)])
        summaries.append(output.summary)
    return update_state(state, commit_summaries=summaries)

# 7. Structured model for final Scrum report
class FinalSummary(BaseModel):
    report: str = Field(description="Scrum report based on commit summaries.")

def generate_scrum_report(state: ScrumState):
    combined = "\n".join(state["commit_summaries"])
    prompt = f"""You are a Scrum Master assistant. Write a daily summary based on the following:
{combined}
"""
    response = llm.with_structured_output(FinalSummary).invoke([HumanMessage(content=prompt)])
    print(f"Generated Scrum Report:\n{response.report}")
    return update_state(state, scrum_report=response.report)

# 8. Build the LangGraph
builder = StateGraph(ScrumState)
builder.add_node("GetCommits", get_mock_commits)
builder.add_node("SummarizeCommits", summarize_commits)
builder.add_node("GenerateScrumReport", generate_scrum_report)

builder.set_entry_point("GetCommits")
builder.add_edge("GetCommits", "SummarizeCommits")
builder.add_edge("SummarizeCommits", "GenerateScrumReport")
builder.add_edge("GenerateScrumReport", END)

# 9. Compile with MemorySaver and show graph
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Optional: visualize
# display(Image(graph.get_graph(xray=True).draw_mermaid_png()))

# 10. Invoke with a thread ID
# state = graph.invoke({}, config={"thread_id": f"scrum-thread-{uuid.uuid4()}"})

# # 11. Print result
# print("📝 Final Scrum Report:\n")
# print(state)

def generate_scrum_report():
    """
    Function to generate a scrum report based on commits.
    This is the main entry point for the script.
    """
    # Invoke the graph
    state = graph.invoke({}, config={"thread_id": f"scrum-thread-{uuid.uuid4()}"})
    
    # Print the final scrum report
    return state



print(generate_scrum_report())  # Call the function to generate the report