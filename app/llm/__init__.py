import logging

from .llm_service import answer_users_msg
from .schemas import LlmResponse

logger = logging.getLogger('llm')


async def process_user_message(message: str) -> LlmResponse:
    # flow_result = await answer_users_msg(msg=message)
    # logger.info(flow_result)
    # response = LlmResponse(
    #     text=flow_result['reply'],
    #     decision=flow_result.get("decision", "reject")
    # )
    response = LlmResponse(
        text="mocked data",
        decision="reject"
    )
    return response
