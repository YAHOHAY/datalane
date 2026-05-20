"""pandas 清洗插件（预留，后续实现表格去重、聚合等）。"""

from core.models import JobContext, PipelineData
from core.registry import register_transform


@register_transform("pandas_clean")
def transform_pandas_clean(data: PipelineData, params: dict, ctx: JobContext) -> PipelineData:
    raise NotImplementedError(
        "pandas_clean 尚未实现。请安装 pandas 后在此添加清洗逻辑。"
    )
