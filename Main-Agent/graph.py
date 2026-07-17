"""
LangGraph Graph Definition.
"""

from __future__ import annotations

from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from nodes import create_agent
from state import GraphState


async def build_graph():

    model, tools = await create_agent()

    tool_node = ToolNode(tools)

    async def chatbot(state: GraphState):

        response = await model.ainvoke(state["messages"])

        return {
            "messages": [response]
        }

    builder = StateGraph(GraphState)

    builder.add_node(
        "chatbot",
        chatbot,
    )

    builder.add_node(
        "tools",
        tool_node,
    )

    builder.add_edge(
        START,
        "chatbot",
    )

    builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )

    builder.add_edge(
        "tools",
        "chatbot",
    )

    memory = InMemorySaver()
    graph = builder.compile(
        checkpointer = memory
    )

    return graph