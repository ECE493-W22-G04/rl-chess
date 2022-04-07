from rl_agent.agent import RlAgent

# This File is used to satisfy FR8 - Computer.Learn

if __name__ == '__main__':
    rl_agent = RlAgent()
    rl_agent.belief_revision(num_episodes=100)