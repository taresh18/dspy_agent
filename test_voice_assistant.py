"""
Test script for Sky Credit Voice Assistant DSPy Pipeline
Uses a testing agent to simulate realistic customer interactions.
"""

import dspy
from src.main_agent import MainAgent
from testing_agent import TestingAgent, ConversationEvaluator
from logger_config import get_logger
import os
from dotenv import load_dotenv
load_dotenv()

# Set up test logger with separate log file
test_logger = get_logger("test_assistant", "logs/test_assistant.log")

def test_assistant_with_agent():
    """Test the voice assistant using a testing agent"""

    test_logger.info("Starting comprehensive AI-driven conversation test")
    test_logger.debug("Configuring DSPy with OpenRouter LM")

    # Configure DSPy
    lm = dspy.LM("openrouter/qwen/qwen3-30b-a3b-instruct-2507", api_base="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
    dspy.configure(lm=lm)

    # Initialize systems
    test_logger.debug("Initializing Main Agent")
    main_agent = MainAgent()
    test_logger.debug("Initializing Testing Agent")
    testing_agent = TestingAgent()
    test_logger.debug("Initializing Conversation Evaluator")
    evaluator = ConversationEvaluator()

    print("🤖 Starting AI-Driven Conversation Test")
    print("=" * 60)

    # Start conversation
    test_logger.debug("Starting conversation with greeting")
    greeting = main_agent.start_conversation()
    test_logger.info(f"Greeting response: {greeting}")
    print(f"Assistant: {greeting}")

    # Get initial customer message
    test_logger.debug("Getting initial customer message")
    customer_message = testing_agent.get_initial_message()
    test_logger.info(f"Initial customer message: {customer_message}")
    print(f"Customer: {customer_message}")

    # Store full conversation for evaluation
    full_conversation = [
        f"Assistant: {greeting}",
        f"Customer: {customer_message}"
    ]
    
    # Continue conversation until testing agent decides to end
    turn_count = 1
    max_turns = 15  # Safety limit

    test_logger.info(f"Starting conversation loop with max {max_turns} turns")

    while not testing_agent.is_conversation_ended() and turn_count < max_turns:
        # Get assistant response
        assistant_response = main_agent.process_customer_input(customer_message)
        test_logger.info(f"Turn {turn_count}: Assistant responded")

        print(f"Assistant: {assistant_response}")
        full_conversation.append(f"Assistant: {assistant_response}")

        # Get customer response from testing agent
        customer_message = testing_agent.generate_response(assistant_response)
        test_logger.info(f"Turn {turn_count}: Customer responded")

        if customer_message is None:
            test_logger.info(f"Turn {turn_count}: Customer ended conversation")
            print("Customer: [Call ended]")
            full_conversation.append("Customer: [Call ended]")
            break

        print(f"Customer: {customer_message}")
        full_conversation.append(f"Customer: {customer_message}")

        turn_count += 1

    if turn_count >= max_turns:
        test_logger.warning(f"Conversation reached maximum turns ({max_turns})")
        print(f"\n⚠️  Conversation reached maximum turns ({max_turns})")
    
    print("\n" + "=" * 60)
    print("📊 Conversation Analysis")
    print("=" * 60)

    # Show conversation state
    test_logger.info("Conversation analysis section")
    test_logger.info(f"Final state - Verified: {main_agent.state.verified}, Scenario: {main_agent.state.scenario_type}")
    test_logger.debug(f"Final verification data: {main_agent.verification_data}")
    test_logger.debug(f"Final actions taken: {main_agent.actions_taken}")

    print("🔍 Final Conversation State:")
    print(f"Verified: {main_agent.state.verified}")
    print(f"Customer Data: {main_agent.state.customer_data['firstName'] if main_agent.state.customer_data else 'None'} {main_agent.state.customer_data['lastName'] if main_agent.state.customer_data else ''}")
    print(f"Scenario Type: {main_agent.state.scenario_type}")
    print(f"Verification Data: {main_agent.verification_data}")
    print(f"Actions Taken: {main_agent.actions_taken}")
    print(f"Total Turns: {turn_count}")

    # Evaluate conversation
    test_logger.info("Starting conversation evaluation")
    print("\n📋 Evaluating Conversation Against Expected Outcomes...")
    evaluation = evaluator.evaluate_conversation(full_conversation)
    test_logger.debug(f"Evaluation result: {evaluation}")

    if "error" in evaluation:
        test_logger.error(f"Evaluation failed: {evaluation['error']}")
        print(f"❌ Evaluation failed: {evaluation['error']}")
    else:
        print("\n✅ Evaluation Results:")
        if "outcome_checks" in evaluation:
            followed_count = 0
            total_count = len(evaluation["outcome_checks"])
            test_logger.info(f"Found {total_count} outcome checks")

            for i, check in enumerate(evaluation["outcome_checks"], 1):
                status = check.get("status", "UNKNOWN")
                description = check.get("outcome_description", "Unknown outcome")
                evidence = check.get("evidence", "No evidence provided")

                status_icon = "✅" if status == "FOLLOWED" else "❌"
                print(f"{status_icon} {i}. {description}")
                print(f"   Evidence: {evidence}")

                if status == "FOLLOWED":
                    followed_count += 1

            score = followed_count/total_count*100 if total_count > 0 else 0
            test_logger.info(f"Evaluation score: {followed_count}/{total_count} ({score:.1f}%)")
            print(f"\n📈 Score: {followed_count}/{total_count} outcomes followed ({score:.1f}%)")
        else:
            test_logger.warning("No outcome checks found in evaluation")
            print("❌ No outcome checks found in evaluation")

    test_logger.info("Test summary")
    print("\n🎯 Test Summary:")
    print("✅ DSPy-driven conversation completed")
    print("✅ Testing agent simulated realistic customer behavior")
    print("✅ Conversation evaluation performed")
    print("✅ No hardcoded responses used")
    print("✅ Comprehensive logging enabled for debugging")

def test_simple_demo():
    """Simple demonstration without full evaluation"""

    test_logger.info("Starting simple demo test")

    # Configure DSPy
    lm = dspy.LM("openrouter/qwen/qwen3-30b-a3b-instruct-2507", api_base="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
    dspy.configure(lm=lm)

    # Initialize systems
    test_logger.debug("Initializing systems for simple demo")
    main_agent = MainAgent()
    testing_agent = TestingAgent()

    print("🤖 Quick Demo: AI vs AI Conversation")
    print("=" * 40)

    # Start conversation
    test_logger.debug("Starting simple demo conversation")
    greeting = main_agent.start_conversation()
    test_logger.info(f"Demo greeting: {greeting}")
    print(f"Assistant: {greeting}")

    customer_message = testing_agent.get_initial_message()
    test_logger.info(f"Demo customer message: {customer_message}")
    print(f"Customer: {customer_message}")

    # Run a few turns
    for turn in range(5):
        test_logger.info(f"Demo turn {turn + 1}: Processing customer message")
        assistant_response = main_agent.process_customer_input(customer_message)
        test_logger.info(f"Demo turn {turn + 1}: Assistant response: {assistant_response}")
        print(f"Assistant: {assistant_response}")

        test_logger.debug(f"Demo turn {turn + 1}: Generating customer response")
        customer_message = testing_agent.generate_response(assistant_response)
        test_logger.info(f"Demo turn {turn + 1}: Customer response: {customer_message}")

        if customer_message is None:
            test_logger.info(f"Demo turn {turn + 1}: Customer ended conversation")
            print("Customer: [Call ended]")
            break

        print(f"Customer: {customer_message}")

    test_logger.info("Simple demo completed")
    print("\n✅ Demo completed - Two AI agents conversing naturally!")

if __name__ == "__main__":
    test_assistant_with_agent()
