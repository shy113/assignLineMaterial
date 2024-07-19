# 模型文件
from typing import List, Dict, Any


class AssignState:
    """分配状态"""
    ASSIGNING = '分配中'
    FINISHED = '已完成'


class ProductionLine:
    """生产线
    """

    def __init__(self, name='', code='', line_type='', line_desc='', init_life='', usage=0, target_usage_rate=0.85):
        self.name = name
        self.code = code
        self.line_type = line_type
        self.line_desc = line_desc
        self.init_life = init_life
        self.usage = usage
        self.target_usage_rate = target_usage_rate  # 目标利用率
        self.produce_material: List[Material] = []

    def __str__(self, *args, **kwargs):  # real signature unknown
        return f"{self.name}"

    @property
    def usage_rate(self):
        return self.usage / self.init_life

    @property
    def remaining_life(self):
        return self.init_life - self.usage

    @property
    def assign_state(self):
        if self.usage_rate >= self.target_usage_rate:
            return AssignState.FINISHED
        else:
            return AssignState.ASSIGNING


class MaterialLine:
    """物料和产线的关系,即该物料可在哪条线上生产和它在该条线一件所消耗的时间
    """

    def __init__(self, line: ProductionLine, ct):
        self.line = line
        self.ct = ct


class Material:
    def __init__(self, name='', code='', material_type='',
                 material_desc='', req=0,
                 production_lines: List[MaterialLine] = []):
        self.name = name
        self.code = code
        self.material_type = material_type
        self.material_desc = material_desc
        self.req = req
        self.production_lines = production_lines
