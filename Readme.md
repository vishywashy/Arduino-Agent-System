# Arduino Agent System

The Arduino Agent System is a lightweight automation setup that connects an Arduino board with a Python LangGraph agent. It performs hardware actions and web automation tasks through a clean user interface.

## Features

• HC-SR04 distance measurement  
  The Arduino reads object distance using an HC-SR04 ultrasonic sensor and sends the data back to Python.

• LED control  
  Users can turn an LED on or off. Commands are routed through a LangGraph agent before reaching the Arduino.

• Web automation  
  The system can play YouTube videos, search Google, and send WhatsApp messages using PyWhatKit.

• Clean UI  
  A simple HTML/CSS interface allows users to trigger actions easily.

• Agent tool routing  
  The LangGraph agent interprets user commands and decides which tool to call, choosing between hardware control or web automation.

## How It Works

1. The user sends a command through the clean UI.  
2. The LangGraph agent interprets the request.  
3. The agent selects the correct tool to call.  
4. The Arduino controller or PyWhatKit module executes the action.