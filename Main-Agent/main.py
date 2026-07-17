"""
Main entry point for the LangGraph Gmail Agent.
"""

from __future__ import annotations

import asyncio

from langchain_core.messages import HumanMessage

from graph import build_graph


async def main():

    graph = await build_graph()

    # print("=" * 60)
    # print(" Gmail MCP Agent")
    # print("=" * 60)
    # print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You : ")

        if user_input.lower() in {"exit", "quit"}:
            break

        config = {
            "configurable": {
            "thread_id": "gmail-user-1"
            }
        }

        result = await graph.ainvoke(
            {
                "messages": [
                    HumanMessage(content=user_input)
                ]
            },
            config = config,
        )

        print()

        print(
            "Assistant :",
            result["messages"][-1].content,
        )

        print()


if __name__ == "__main__":

    asyncio.run(main())