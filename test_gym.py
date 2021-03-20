# import gym
# env = gym.make('CartPole-v0')
# env.reset()
# for _ in range(1000):
#     env.render()
#     env.step(env.action_space.sample()) # take a random action
# env.close()



# import gym

# from gym import spaces
# s= spaces.MultiDiscrete([3]*9)


# env = gym.make('CartPole-v0')
# print(env.action_space)
# print(env.observation_space)

# for i_episode in range(20):
#     observation = env.reset()
#     for t in range(100):
#         env.render()
#         print(observation)
#         action = env.action_space.sample()
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break
# env.close()


from env import tictactoe

import time
ttt_env = tictactoe.TicTacToeEnv()
for i_episode in range(20):
    observation = ttt_env.reset()
    for t in range(100):
        ttt_env.render()
        time.sleep(0.5)
        # print(observation)
        action = ttt_env.action_space.sample()
        observation, reward, done, info = ttt_env.step(action)
        print(action,observation, reward, done)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
ttt_env.close()