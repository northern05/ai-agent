import logging

from utils.smc_driver import SMCDriver
from .llm_service import answer_users_msg
from .schemas import LlmResponse

logger = logging.getLogger('llm')


async def process_user_message(message: str, smc_driver: SMCDriver, user_address: str) -> LlmResponse:
    flow_result, decision = answer_users_msg(msg=message, smc_driver=smc_driver, user_address=user_address)
    logger.info(flow_result)
    response = LlmResponse(
        text=flow_result,
        decision=decision
    )
    return response
