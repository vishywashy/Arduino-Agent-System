
from datetime import datetime
from ReactTools import *
from pyautogui import click
import pywhatkit
from fastapi import FastAPI
import ArduinoController
import pyttsx3
import uvicorn
from time import sleep
class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]


@tool
def WhatsappMessageSender(content:str, phone_number:str):
    """(The phone_number is the number the message is being sent to) and (the content is the message that needs to be sent).
    Args:
       phone_number:Phone number that user provided.
       content:Content provided by the user."""
    time = str(datetime.now())
    time = time.split(" ")[1]
    hours = int(time.split(":")[0])
    minutes = int(time.split(":")[1])
    pywhatkit.sendwhatmsg(phone_number, content, hours, minutes+1, wait_time=15)
    click(x = 1877, y = 984)
    return "Message has been sent successfully."



@tool
def YoutubePlayTool(topic:str):
    """The topic is the type of youtube video the user wants.
    Args:
      topic:topic provided by user for youtube video."""
    
    pywhatkit.playonyt(topic)
    return "Youtube video is playing."

@tool
def GoogleSearch(topic:str):
    """The topic is provided by the user.
    Args:
       topic:topic provided by user for GoogleSearch."""
    pywhatkit.search(topic)
    return "Google search has been performed."

@tool
def LEDLightControls(light:str, state:str):
    """State:On or off, Light:Colour of the light. All information must be lowercase"""
    sleep(2)
    ArduinoController.LEDController(state, light)
    return "Done"

@tool
def DistanceCalculator():
    """used to calculate distance via an ultrasonic sensor."""
    engine = pyttsx3.init()
    sleep(2)
    try:
        engine.say("The distance is "+ArduinoController.DistanceCalculator()+"cm")
        engine.runAndWait()
    except RuntimeError:
        return "Runtime error"
    return f"The distance is {ArduinoController.DistanceCalculator()}cm"


    
tools = [YoutubePlayTool, WhatsappMessageSender, GoogleSearch, LEDLightControls, DistanceCalculator]
llm = ChatOllama(model = "llama3.2", temperature=0)#sets up connection
model = llm.bind_tools(tools)#adds tools to it.
full_response = ""
def Agent(state:AgentState):
    global full_response
    system_msg = SystemMessage(
        """You are an AI agent with capabilities to play a youtube video, send a message on whatsapp and perform a google search.
        You can also operate led by turning it on and off and can also calculate distances.
        Please follow the information to use those capabilities and assist the user as much as possible."""
    )
    response = model.invoke([system_msg]+state["messages"])
    full_response+=response.content
    return {"messages":[response]}

def looper(state:AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "continue"
    else:
        return "exit"
    
graph = StateGraph(AgentState)
toolnode = ToolNode(tools = tools)
graph.add_node("Agent", Agent)
graph.set_entry_point("Agent")
graph.add_node("Tool", toolnode)
graph.add_conditional_edges(
    "Agent",
    looper,
    {"continue":"Tool", "exit":END}

)
graph.add_edge("Tool", "Agent")

app = graph.compile()

def streamwriter(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()



def Payload_Receiver(prompt):
    streamwriter(app.stream({"messages":["user", prompt]}, stream_mode="values"))
    return full_response


        

APIBuilder = FastAPI()
@APIBuilder.get("/")
def Server(payload:str):
    return {"Messages":Payload_Receiver(payload)}

if __name__ == "__main__":
    uvicorn.run("AutomatedAgent:APIBuilder", host="127.0.0.1", port=8000)


    






