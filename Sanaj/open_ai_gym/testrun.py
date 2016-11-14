import gym
import numpy as np

env = gym.make('CartPole-v0')

# env.reset()
# for i_episode in range(20):
# 	observation = env.reset()
# 	for t in range(10000):
# 		env.render()
# 		print(observation)
# 		action = env.action_space.sample()
# 		observation, reward, done, info = env.step(action)

# 		if done:
# 			print("episode finished after {} timesteps")
# 			break

#hill climbing initialize weights randomly, utilize memory to save food weights
def run_episode(env, parameters):
	observation = env.reset()
	totalreward = 0
	
	for _ in range(2000):
		env.render()
		action = 0 if np.matmul(parameters, observation) < 0 else 1
		observation, reward, done, info = env.step(action)
		totalreward += reward
		if done:
			break
	return totalreward

#actual hillcliming
def train(submit):
	env = gym.make('CartPole-v0')

	episodes_per_update = 5
	noise_scaling = 0.1
	parameters = np.random.rand(4) * 2 - 1
	bestreward = 0

	#2000 episods
	for _ in range(20000):
		newparameter = parameters + (np.random.rand(4) * 2 - 1) * noise_scaling
		reward = run_episode(env, newparameter)
		print("reward %d best %d" % (reward, bestreward))
		if reward > bestreward:
			bestreward = reward
			parameters = newparameter
			if reward == 200:
				break;

r = train(submit=False)



