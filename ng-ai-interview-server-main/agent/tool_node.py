import json
from typing import Dict, List
from langchain_core.messages import ToolMessage
from agent.agent_state import AgentState

class ToolNode:
    """Tool node class for handling tool operations"""
    
    def __init__(self, tools: List):
        """
        Initialize ToolNode with a list of tools
        
        Args:
            tools: List of available tools
        """
        self.tools = tools
        self.tools_by_name = {tool.name: tool for tool in tools}
    
    def process_tool_calls(self, state: AgentState) -> Dict:
        """
        Process tool calls from the agent state
        
        Args:
            state: Current agent state containing messages and tool calls
            
        Returns:
            Dict containing list of tool messages
        """
        outputs = []
        
        for tool_call in state["messages"][-1].tool_calls:
            tool_result = self._execute_tool(tool_call)
            outputs.append(self._create_tool_message(tool_call, tool_result))
        
        return {"messages": outputs}
    
    def _execute_tool(self, tool_call: Dict) -> Dict:
        """
        Execute a specific tool call
        
        Args:
            tool_call: Dictionary containing tool call details
            
        Returns:
            Tool execution result
        """
        tool = self.tools_by_name[tool_call["name"]]
        return tool.invoke(tool_call["args"])
    
    def _create_tool_message(self, tool_call: Dict, result: Dict) -> ToolMessage:
        """
        Create a tool message from execution result
        
        Args:
            tool_call: Original tool call details
            result: Tool execution result
            
        Returns:
            ToolMessage containing the result
        """
        return ToolMessage(
            content=json.dumps(result),
            name=tool_call["name"],
            tool_call_id=tool_call["id"]
        )