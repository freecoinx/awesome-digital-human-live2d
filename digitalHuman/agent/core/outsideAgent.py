# -*- coding: utf-8 -*-
'''
@File    :   outsideAgent.py
@Author  :   Mozilla88 
'''

import importlib

from yacs.config import CfgNode as CN

from ..builder import AGENTS
from ..agentBase import BaseAgent
from typing import List, Union
from digitalHuman.utils import logger
from digitalHuman.utils import AudioMessage, TextMessage


__all__ = ["OutsideAgent"]


@AGENTS.register("OutsideAgent")
class OutsideAgent(BaseAgent):
    def __init__(self, config: CN):
        super().__init__(config)
        
        self.agent_type = ""
        self.agent_module_name = ""
        self.agent_module = None
        
        for param in config.PARAMETERS:
            if param['NAME'] == "AGENT_TYPE":
                self.agent_type = param['DEFAULT']
            if param['NAME'] == "AGENT_MODULE":
                self.agent_module_name = param['DEFAULT']

        if self.agent_type == "local_lib":
            self.agent_module = importlib.import_module(self.agent_module_name)

    async def run(
        self, 
        input: Union[TextMessage, AudioMessage], 
        streaming: bool,
        **kwargs
    ):
        try: 
            if isinstance(input, AudioMessage):
                raise RuntimeError("OutsideAgent does not support AudioMessage input yet")
            yield await self.agent_module.chat_with_agent(input.data)
        except Exception as e:
            logger.error(f"[AGENT] Engine run failed: {e}", exc_info=True)
            yield ""

