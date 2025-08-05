from llama_index.core import llms, query_engine, SQLDatabase, tools
from sqlalchemy import create_engine
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context, JsonPickleSerializer
from llama_index.core.workflow.handler import WorkflowHandler
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import VectorStoreIndex
from llama_index.core.prompts.default_prompts import DEFAULT_TEXT_TO_SQL_PROMPT
from llama_index.core.prompts import PromptTemplate, PromptType
from typing import Dict
import os
from pathlib import Path
from llama_index.core.schema import TextNode
from sqlalchemy import text
from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core import StorageContext

class ReActAgentService:
    def __init__(self, llm: llms.LLM, connection_string: str):
        print(f"Initializing ReActAgentService")
        self.llm = llm
        self.temp_conversation_id_storage = {}
        engine = create_engine(connection_string)
        include_tables=['interview_invitations', 'interviews', 'applicants', 'applications', 'job_posts']
        sql_database = SQLDatabase(engine=engine, include_tables=include_tables)

        table_node_mapping = SQLTableNodeMapping(sql_database)

        table_schema_objs = []
        for table_name in include_tables:
            table_schema_objs.append(SQLTableSchema(table_name=table_name))

        obj_index = ObjectIndex.from_objects(
            table_schema_objs,
            table_node_mapping,
            VectorStoreIndex,
        )
        text2sql_prompt = DEFAULT_TEXT_TO_SQL_PROMPT.partial_format(
            dialect=engine.dialect.name
        )
        custom_prompt = PromptTemplate(
            template=text2sql_prompt.template + "\nRemember to double-quote uppercase identifiers (e.g. \"applicants\".\"fullName\").",
            prompt_type=PromptType.TEXT_TO_SQL,
            template_var_mappings=text2sql_prompt.template_var_mappings,
        )

        vector_index_dict = self.index_all_tables(sql_database, table_index_dir="table_index_dir")
        row_retrievers = {}

        for table_name, index in vector_index_dict.items():
            row_retrievers[table_name] = index.as_retriever(similarity_top_k=1)

        self.sql_query_engine = query_engine.NLSQLTableQueryEngine(
            sql_database=sql_database,
            tables=include_tables,
            text_to_sql_prompt=custom_prompt,
            table_retriever=obj_index.as_retriever(similarity_top_k=5),
            rows_retrievers=row_retrievers,
            llm=llm,
        )
        query_engine_tools = [
            tools.QueryEngineTool.from_defaults(
                query_engine=self.sql_query_engine,
                name="SQLQueryEngine",
                description="Use this tool to query the SQL database for structured data. You can ask questions about interview invitations, interviewers, job posts and applicants.",
            )
        ] 
        system_prompt="""
            You are a helpful assistant who supports users in the hiring and interview process.

            You can:
            - Answer open-ended questions (e.g., help write job descriptions, interview questions, etc.),
            - Query a SQL database when structured data is required (e.g., list applicants, see interview status, etc.).

            Only use the SQL database tool when the user asks for data that would reasonably come from the system.
            Otherwise, respond directly using your general knowledge.
            """
        self.agent = ReActAgent(
            tools=query_engine_tools,
            llm=self.llm,
            system_prompt=system_prompt,
        )

    def test(self, query: str):
        return self.sql_query_engine.query(query)
    
    def send_message(self, query: str, conversation_id: str) -> WorkflowHandler:
        print(self.temp_conversation_id_storage)
        if self.temp_conversation_id_storage.get(conversation_id, None) is None:
            ctx = Context(self.agent)
        else:
            try:
                ctx_dict = self.temp_conversation_id_storage[conversation_id]
                ctx = Context.from_dict(self.agent, ctx_dict, serializer=JsonPickleSerializer())
            except Exception as e:
                print(f"Error loading context for conversation {conversation_id}: {e}")
                ctx = Context(self.agent)

        handler = self.agent.run(query, ctx=ctx)

        return handler
    
    async def save_context(self, conversation_id: str, context: Context) -> bool:
        await context.shutdown()
        ctx_dict = context.to_dict(serializer=JsonPickleSerializer())
        self.temp_conversation_id_storage[conversation_id] = ctx_dict
        return True
    
    @staticmethod
    def index_all_tables(sql_database: SQLDatabase, table_index_dir: str = "table_index_dir") -> Dict[str, VectorStoreIndex]:
        """Index all tables."""
        if not Path(table_index_dir).exists():
            os.makedirs(table_index_dir)

        vector_index_dict = {}
        engine = sql_database.engine
        for table_name in sql_database.get_usable_table_names():
            print(f"Indexing rows in table: {table_name}")
            if not os.path.exists(f"{table_index_dir}/{table_name}"):
                # get all rows from table
                with engine.connect() as conn:
                    cursor = conn.execute(text(f'SELECT * FROM "{table_name}" limit 1'))
                    result = cursor.fetchall()
                    row_tups = []
                    for row in result:
                        row_tups.append(tuple(row))

                # index each row, put into vector store index
                nodes = [TextNode(text=str(t)) for t in row_tups]

                # put into vector store index (use OpenAIEmbeddings by default)
                index = VectorStoreIndex(nodes)

                # save index
                index.set_index_id("vector_index")
                index.storage_context.persist(f"{table_index_dir}/{table_name}")
            else:
                # rebuild storage context
                storage_context = StorageContext.from_defaults(
                    persist_dir=f"{table_index_dir}/{table_name}"
                )
                # load index
                index = load_index_from_storage(
                    storage_context, index_id="vector_index"
                )
            vector_index_dict[table_name] = index

        return vector_index_dict