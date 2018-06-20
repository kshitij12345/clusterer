from .base import BaseScheduler

class PipelineReplicate(BaseScheduler):
    def schedule(self,info,functions):
        func_list = []
        for func in functions:
            func_list.append(functions[func])

        return func_list