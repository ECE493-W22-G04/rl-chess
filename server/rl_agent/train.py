from rl_agent.agent import RlAgent

if __name__ == '__main__':
    rl_agent = RlAgent()
    for _ in range(100):
        rl_agent.train(num_episodes=1000)
