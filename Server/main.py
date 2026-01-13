from agent import DatabaseConn , SupportDependencies, my_agent
import asyncio
async def function():
    deps = SupportDependencies(user_id=1, db=DatabaseConn())

    result = await my_agent.run("whats is my subscription plan?", deps=deps)
    print(result.output)


if __name__ == "__main__":
   asyncio.run(function())