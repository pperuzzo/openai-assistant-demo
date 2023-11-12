from openai import OpenAI

client = OpenAI(api_key="@@@@@@")

# Create the assistant with the specific prompt
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)
assistantId = assistant.id

# Start a new thread.
# Each thread is like a chat hisotory with a user
thread = client.beta.threads.create()
threadId = thread.id

# Add a message from the user to the
message = client.beta.threads.messages.create(
    thread_id=threadId,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)

# Start the run
run = client.beta.threads.runs.create(
    thread_id=threadId,
    assistant_id=assistantId,
    instructions="Please always start your response with 'My dear friend,'",
)
runId = run.id

print("Running request...")

# Wait for the run to be complete
# TODO: Should add more checks to account for other statuses
while True:
    run = client.beta.threads.runs.retrieve(thread_id=threadId, run_id=runId)

    if run.status == "completed":
        break

# Get the messages and dump them as json to a file
messages = client.beta.threads.messages.list(thread_id=threadId)
with open("messages.json", "w") as file:
    file.write(messages.model_dump_json())


# List the internal steps for debug purpose
stepList = client.beta.threads.runs.steps.list(run_id=runId, thread_id=threadId)
with open("steps.json", "w") as file:
    file.write(stepList.model_dump_json())

print("Done!")
