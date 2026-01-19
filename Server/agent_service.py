from Server.config.agent import DatabaseConn , SupportDependencies, my_agent
import asyncio
async def function():
    deps = SupportDependencies(user_id=2, db=DatabaseConn())

    result = await my_agent.run_sync("Give me account status", deps=deps)
    print(result.output)


if __name__ == "__main__":
   asyncio.run(function())