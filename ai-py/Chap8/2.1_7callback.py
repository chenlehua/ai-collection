import logging
import uuid
from typing import Any, Dict, List, Optional
from llama_index.core.callbacks.base_handler import BaseCallbackHandler
from llama_index.core.callbacks.schema import CBEventType, EventPayload

# 设置日志记录器
logger = logging.getLogger("llama_index_error_logger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("llama_index_errors.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ErrorLoggingHandler(BaseCallbackHandler):
    """扩展的回调处理类，用于在事件追踪时记录错误日志"""

    def __init__(self) -> None:
        # 调用父类构造器，不忽略任何事件类型
        super().__init__(event_starts_to_ignore=[], event_ends_to_ignore=[])

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        """
        事件开始时触发，记录事件开始的基本信息。

        参数:
            event_type (CBEventType): 事件类型
            payload (Optional[Dict[str, Any]]): 事件的额外数据
            event_id (str): 事件ID（默认生成唯一ID）
            parent_id (str): 父事件ID
        返回:
            str: 当前事件的ID
        """
        event_id = event_id or str(uuid.uuid4())  # 确保事件ID唯一
        logger.debug(f"Starting event: {event_type} with ID: {event_id}")
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """
        事件结束时触发，检查并记录错误日志（若有异常）。

        参数:
            event_type (CBEventType): 事件类型
            payload (Optional[Dict[str, Any]]): 事件的额外数据
            event_id (str): 事件ID
        """
        if payload and EventPayload.EXCEPTION in payload:
            # 如果 payload 中有异常，则记录错误日志
            exception = payload[EventPayload.EXCEPTION]
            logger.error(f"Exception in event {event_type} (ID: {event_id}): {exception}")
        else:
            # 正常结束时记录事件结束信息
            logger.debug(f"Ending event: {event_type} with ID: {event_id}")

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """
        追踪开始时触发，记录追踪开始的日志。

        参数:
            trace_id (Optional[str]): 追踪ID
        """
        logger.info(f"Starting trace with ID: {trace_id}")

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """
        追踪结束时触发，记录追踪结束的日志。

        参数:
            trace_id (Optional[str]): 追踪ID
            trace_map (Optional[Dict[str, List[str]]]): 事件追踪映射
        """
        logger.info(f"Ending trace with ID: {trace_id}")

# 示例使用：在 CallbackManager 中添加错误日志记录处理器
callback_manager = CallbackManager(handlers=[ErrorLoggingHandler()])

# 示例代码：启动事件并捕获错误
with callback_manager.event(CBEventType.QUERY, payload={"example_key": "example_value"}) as event:
    try:
        # 模拟发生错误
        raise ValueError("This is a test error!")
    except Exception as e:
        # 捕获到的异常加入到事件 payload 中
        payload = {EventPayload.EXCEPTION: e}
        event.on_end(payload=payload)  # 确保错误信息在事件结束时记录
