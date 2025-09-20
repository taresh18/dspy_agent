"""
Simple test runner for Sky Credit Voice Assistant DSPy Pipeline
"""

import dspy
from src.main_agent import MainAgent
from testing_agent import TestingAgent
from logger_config import get_logger
import os
from dotenv import load_dotenv
load_dotenv()

logger = get_logger("test_runner")

def run_conversation_test():
    """Run a simple conversation test between AI agents"""
    
    logger.info("Starting DSPy conversation test")
    
    # Configure DSPy
    lm = dspy.LM("openrouter/qwen/qwen3-30b-a3b-instruct-2507", api_base="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
    dspy.configure(lm=lm)

    # Initialize agents
    main_agent = MainAgent()
    testing_agent = TestingAgent()

    print("🤖 Sky Credit Voice Assistant Test")
    print("=" * 40)

    # Start conversation
    customer_message = testing_agent.get_initial_message()
    print(f"Customer: {customer_message}")
    
    assistant_response = main_agent.process_input(customer_message)
    print(f"Assistant: {assistant_response}")

    # Continue conversation
    max_turns = 10
    for turn in range(max_turns):
        customer_message = testing_agent.generate_response(assistant_response)
        
        if customer_message is None:
            print("Customer: [Call ended]")
            logger.info(f"Conversation ended after {turn + 1} turns")
            break

        print(f"Customer: {customer_message}")
        assistant_response = main_agent.process_input(customer_message)
        print(f"Assistant: {assistant_response}")

    # Show results
    print("\n" + "=" * 40)
    print("📊 Test Results")
    print("=" * 40)
    print(f"Total Messages: {len(main_agent.state.history.messages)}")
    
    # Check if customer was found
    customer_found = any("Customer found:" in str(msg) for msg in main_agent.state.history.messages)
    print(f"Customer Lookup: {'✅ Success' if customer_found else '❌ Failed'}")
    
    logger.info("Test completed successfully")
    print("✅ Test completed - Check logs/app.log for detailed logs")

    # dumpt the inspect history of main agent to a txt file
    with open("logs/history.txt", "w") as f:
        f.write(main_agent.get_history())

if __name__ == "__main__":
    run_conversation_test()
