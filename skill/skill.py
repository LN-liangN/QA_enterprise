from langchain.agents import create_agent

from model.factory import chat_model
from skill.middleware import monitor_tool, log_before_model
from skill.tools import sql_query, rag_summarize
from utils.prompts_loader import load_system_prompts


class ReactSkill:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[sql_query, rag_summarize],
            middleware=[monitor_tool, log_before_model],
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        for chunk in self.agent.stream(input_dict, stream_mode="values"):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"


if __name__ == '__main__':
    agent = ReactSkill()
    for chunk in agent.execute_stream("年假怎么计算,还有，张三的邮箱多少呀"):
        print(chunk, end="", flush=True)
