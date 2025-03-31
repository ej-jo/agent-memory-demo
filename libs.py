
import importlib
import pandas as pd
import os
import inspect
from langchain.agents import Tool
from langchain.tools import StructuredTool


DEFAULT_GPT_SYSTEM_PROMPT = """You are a helpful assistant
Restrictions:
    1. Print the "Final Answer" in Korean
    2. When using ibk-retrieval action, the action input should be Korean.
    3. Be sure to check the "area" of the observation before responding to the user.
    4. If there is a region in the user query, please include the region name in Korean in the ibk-retrieval action input so that only documents from right region can be retrieved.
    5. If your question includes multiple regions, ask about multiple regions at once when using the ibk-retrieval tool. For example, "종로구와 동작구의 금리 및 대출한도 비교".
    6. If the resulting has a "CD 91일 금리", change it to the current CD rate using tool "get_CD_rate".   
    7. When using "google_search" tool, use the Korean in the "User Query" and include today's date({today}) to find the latest information.                 
    8. Please indicate in the results the link you referenced to answer the “google_search” tool result.
"""

DEFAULT_LLAMA_SYSTEM_PROMPT = """You are a helpful assistant
Restrictions:
    1. Print the "Final Answer" in Korean and include all logic, numbers, and rationale in detail.     
    2. When using ibk-retrieval action, the action input should be Korean.
    3. Be sure to check the "area" of the observation before responding to the user.
    4. If there is a region in the user query, please include the region name in Korean in the ibk-retrieval action input so that only documents from right region can be retrieved.
    5. If your question includes multiple regions, ask about multiple regions at once when using the ibk-retrieval tool. For example, "종로구와 동작구의 금리 및 대출한도 비교".
    6. If the resulting has a "CD 91일 금리", change it to the current CD rate using tool "get_CD_rate".   
    7. When using "google_search" tool, use the Korean in the "User Query" and include today's date({today}) to find the latest information.                 
    8. Please indicate in the results the link you referenced to answer the “google_search” tool result.
    9. Don't suggest or ask additional question to user. Please answer the question.
    10. Don't use the same 'Action' and 'Action Input' repeatedly. 
"""

DEFAULT_TOOL_LIST = ['ibk_retriever_tool', 'get_banksalad_interest_rate', 'get_kookmin_bank_interest_rate', 'get_CD_rate', 'search_tool', 'get_current_weather_tool']

def import_all_modules_from_directory(directory):
    tools = []

    # 디렉토리 내의 모든 파일 목록 가져오기
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            # 파일 이름에서 확장자를 제거하여 모듈 이름 얻기
            module_name = filename[:-3]
            module_path = f'{directory.replace(".", "").replace("/", "")}.{module_name}'

            print(f"name: {module_name}, path: {module_path}")

            # 모듈 동적 임포트
            module = importlib.import_module(module_path)

            # 모듈 내의 모든 함수 가져오기
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, StructuredTool) or isinstance(obj, Tool):
                    tools.append((name, obj))

    return tools


def get_custom_tools_list():
    tools_list = []
    all_custom_tools = import_all_modules_from_directory("./custom_tool")
    for tool_name, tool in all_custom_tools:
        if(type(tool) == StructuredTool) or (type(tool) == Tool):
            tools_list.append({"tool_name": tool_name, "tool": tool})

    return tools_list

def get_custom_tool_names_list():
    tools_list = []
    all_custom_tools = import_all_modules_from_directory("./custom_tool")
    for tool_name, tool in all_custom_tools:
        if(type(tool) == StructuredTool) or (type(tool) == Tool):
            tools_list.append(tool_name)

    return tools_list


def register_custom_tool(name, code, description):
    custom_tool = f"""\n\n
{name}_tool = StructuredTool.from_function(    
    name="{name}",
    description='''{description}''',
    func={name}
)
"""
    
    with open("./custom_tool/"+name+".py", "w") as file:
        file.write("from langchain.tools import StructuredTool\n\n")
        file.write(code)
        file.write(custom_tool)

    return

def register_custom_knowledge(filename, description):
    header = f"""
from langchain.agents import Tool
from langchain.tools import StructuredTool
import pandas as pd
"""


    new_file_name = filename.replace(".", "_")

    custom_knowledge = f"""\n\n
def read_csv(filename):
    return pd.read_csv("custom_knowledge/"+filename)


{new_file_name}_tool = Tool(    
    name="{new_file_name}",
    description='''{description}''',
    func=lambda *args, **kwargs: read_csv("{filename}")
)
"""
    
    with open("./custom_tool/"+new_file_name+".py", "w") as file:
        file.write(header)
        file.write(custom_knowledge)

    return