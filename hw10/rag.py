from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# 定義提示詞
sys_prompt = """
You run in a loop of Thought, Action, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

call_google:
e.g. call_google: European Union
Returns a summary from searching European Union on google

You can look things up on Google if you have the opportunity to do so, or you are not sure about the query

Example1:

Question: What is the capital of Australia?
Thought: I can look up Australia on Google
Action: call_google: Australia

You will be called again with this:

Observation: Australia is a country. The capital is Canberra.

You then output:

Answer: The capital of Australia is Canberra
"""

# 定義問題提示
question_prompt = "Question: {question}\nThought:"

# 創建 LLM 鏈接
prompt_template = PromptTemplate(template=sys_prompt + question_prompt, input_variables=["question"])
llm_chain = LLMChain(
    llm=OpenAI(api_key="open-ai-key"),    
    prompt=prompt_template
)

# 執行 LLM 鏈接
question = "What is the capital of Australia?"
response = llm_chain.run({"question": question})
print(response)
