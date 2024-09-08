# agentの作成(llmは固定で引数指定する)。
# NOTE: データの永続化と取得ではないため、agentとしている

from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
)
from langchain_openai import ChatOpenAI

from infrastructure.tools.vectorstore_tool import VectorStoreTool


class RAGAgent:
    def __init__(self, llm_client: ChatOpenAI, vector_store_tool: VectorStoreTool):
        self.llm_client = llm_client
        self.vectorstore_tool = vector_store_tool

        # TODO: 適切なカスタムプロンプトに変更する
        self._prompt = hub.pull("hwchase17/openai-functions-agent")
        self.agent = self._get_agent()

    def _get_agent(self):
        agent = create_openai_functions_agent(
            llm=self.llm_client,
            tools=[self.vectorstore_tool.get_tool()],
            prompt=self._prompt,
        )
        agent_executor = AgentExecutor(
            agent=agent,  # type: ignore
            tools=[self.vectorstore_tool.get_tool()],
            verbose=True,
        )
        return agent_executor

    def get(self, query: str) -> str:
        res = self.agent.invoke(
            {
                "input": query,
            },
        )
        return res["output"]
