from rl_agent.agent import RlAgent

if __name__ == '__main__':
    rl_agent = RlAgent()
    rl_agent.train(num_episodes=100)
