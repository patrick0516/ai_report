import gymnasium as gym

def fixed_policy(observation):
    _, _, pole_angle, _ = observation
    return 0 if pole_angle < 0 else 1  

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)

total_steps = 0  

for episode in range(10):  
    observation, info = env.reset()
    steps = 0
    while True:
        env.render()
        action = fixed_policy(observation)  
        observation, reward, terminated, truncated, info = env.step(action)
        steps += 1
        total_steps += 1
        if terminated or truncated:
            print(f"Episode {episode + 1}: {steps} steps")
            break

print(f"Total steps over 10 episodes: {total_steps}")
env.close()
