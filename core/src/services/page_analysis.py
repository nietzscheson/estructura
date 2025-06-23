from botocore.exceptions import BotoCoreError, ClientError
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.schema import OutputParserException
from pydantic import ValidationError


class PageAnalysis:
    def __init__(self, groq_client, logger):
        self.llm = groq_client
        self.logger = logger

    def __call__(self, page_content: list, page_number: str, structure: dict):
        try:
            llm = self.llm.with_structured_output(structure)
            system_template = """
                All instructions are in the Model Header
                """

            human_template = "Page Content: {page_content}. Page Number: {page_number}"

            system_prompt = SystemMessagePromptTemplate.from_template(system_template)
            human_prompt = HumanMessagePromptTemplate.from_template(human_template)

            chat_prompt = ChatPromptTemplate.from_messages(
                [system_prompt, human_prompt]
            )

            messages = chat_prompt.format_prompt(
                page_content=page_content, page_number=page_number
            ).to_messages()

            response = llm.invoke(messages)

            return response

        except (ValidationError, OutputParserException) as e:
            self.logger.error(f"Pydantic Validation Error: {e}")
            raise

        except (BotoCoreError, ClientError) as e:
            self.logger.error(f"AWS Bedrock Error: {e}")
            raise

        except Exception as e:
            self.logger.error(f"Unexpected Error: {e}")
            raise
