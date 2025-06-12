# -*- coding: utf-8 -*-
'''
@File    :   outsideAgent.py
@Author  :   Mozilla88 
'''

import importlib

from yacs.config import CfgNode as CN

from ..builder import AGENTS
from ..agentBase import BaseAgent
from digitalHuman.protocol import *
from digitalHuman.utils import logger, resonableStreamingParser


__all__ = ["OutsideAgent"]


@AGENTS.register("OutsideAgent")
class OutsideAgent(BaseAgent):
    async def run(
        self, 
        user: UserDesc,
        input: TextMessage, 
        streaming: bool = True,
        conversation_id: str = "",
        **kwargs
    ):
        try: 
            if not isinstance(input, TextMessage):
                raise RuntimeError("OutsideAgent only support TextMessage")

            paramters = self.checkParameter(**kwargs)
            AGENT_TYPE = paramters["agent_type"]
            AGENT_MODULE = paramters["agent_module"]

            if AGENT_TYPE == "local_lib":
                agent_module = importlib.import_module(AGENT_MODULE)

                if streaming:
                    generator = agent_module.chat_with_agent
                    async for parseResult in resonableStreamingParser(generator(input.data)):
                        yield parseResult
                else:
                    agent_response = await agent_module.chat_with_agent(input.data)
                    yield eventStreamText(agent_response)
                    
                yield eventStreamDone()            

            else:
                yield eventStreamText(input.data)
            
            yield eventStreamDone()            

        except Exception as e:
            logger.error(f"[OutsideAgent] Exception: {e}", exc_info=True)
            yield eventStreamError(str(e))
