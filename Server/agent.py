from pydantic_ai import Agent

agent = Agent('gateway/openai:gpt-5')

result = agent.run_sync('Where does "hello world" come from?')
print(result.output)
"""
The first known use of "hello, world" was in a 1974 textbook about the C programming language.
"""