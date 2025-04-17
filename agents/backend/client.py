import sys
import os
import asyncio
import time
import re

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.utils import get_agent_card, send_task_to_agent, extract_agent_reply, log_message

from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is not set.")
    print("Please make sure you have a valid API key in your .env file.")
    sys.exit(1)

# URLs for our agent servers
BACKEND_URL = "http://localhost:5003"

# Desktop Commander MCP server for file operations
desktop_commander = MCPServerStdio(
    'npx', ['-y', '@wonderwhy-er/desktop-commander'],
    env={}
)

# Local agent for analyzing tasks
client_agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt="""You analyze tasks.md files to identify backend tasks that need to be completed.
    You help coordinate the work of a backend development agent by identifying which tasks to work on next.
    """,
    mcp_servers=[desktop_commander]
)

def get_backend_tasks():
    """Read tasks.md and identify uncompleted backend tasks."""
    try:
        with open('/home/adria/a2a-agent/tasks.md', 'r') as f:
            content = f.read()
        
        # Look for sections that might contain backend tasks
        backend_section_pattern = r'#{1,3}\s+(?:Backend|Back[- ]?end|Server|API).*?\n(.*?)(?=#{1,3}|\Z)'
        backend_sections = re.findall(backend_section_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not backend_sections:
            return "No backend section found in tasks.md"
        
        # Find incomplete tasks in those sections
        incomplete_tasks = []
        for section in backend_sections:
            task_pattern = r'- \[ \](.*?)(?=\n- |\n\n|\Z)'
            tasks = re.findall(task_pattern, section, re.DOTALL)
            incomplete_tasks.extend(tasks)
        
        if not incomplete_tasks:
            return "All backend tasks are completed!"
        
        # Format the tasks
        task_list = "\n".join(f"- {task.strip()}" for task in incomplete_tasks)
        return f"Uncompleted backend tasks:\n\n{task_list}"
    except Exception as e:
        return f"Error reading tasks.md: {e}"

async def main():
    # 1. Discover the backend agent
    log_message("Connecting to Backend Agent...", "Backend Client")
    backend_card = get_agent_card(BACKEND_URL)
    if not backend_card:
        log_message("Failed to connect to Backend Agent. Make sure it's running.", "Backend Client")
        return
    
    log_message(f"Connected to {backend_card['name']} - {backend_card.get('description', '')}", "Backend Client")
    
    # Check if plan.md and tasks.md exist
    if not os.path.exists('/home/adria/a2a-agent/plan.md') or not os.path.exists('/home/adria/a2a-agent/tasks.md'):
        log_message("Error: plan.md or tasks.md not found. Run the Planner Agent first.", "Backend Client")
        return
    
    # Continuous loop to process backend tasks
    while True:
        # Use the client agent to analyze the tasks file
        async with client_agent.run_mcp_servers():
            result = await client_agent.run("Read the tasks.md file and identify uncompleted backend tasks.")
            next_task_analysis = result.data
        
        # Check if there are any backend tasks to complete
        backend_tasks = get_backend_tasks()
        if "All backend tasks are completed" in backend_tasks:
            log_message("All backend tasks are completed! 🎉", "Backend Client")
            break
        
        # Generate instructions for backend agent
        task_prompt = f"""Please implement the next set of backend tasks from tasks.md.

Here are the pending backend tasks:
{backend_tasks}

Please work on these tasks one by one. For each task:
1. Create or modify the necessary files
2. Implement the functionality described
3. Mark the task as completed in tasks.md (change "[ ]" to "[x]")

After completing each task, provide a summary of what you've done.
"""
        
        log_message("Sending backend tasks to agent...", "Backend Client")
        backend_response = send_task_to_agent(BACKEND_URL, task_prompt)
        backend_reply = extract_agent_reply(backend_response)
        
        if not backend_reply:
            log_message("Failed to get response from Backend Agent.", "Backend Client")
            break
        
        log_message("Backend Agent has completed some tasks!", "Backend Client")
        print("\n" + backend_reply + "\n")
        
        log_message("Waiting before checking for more tasks...", "Backend Client")
        time.sleep(3)  # Short pause before next iteration

if __name__ == "__main__":
    asyncio.run(main())
