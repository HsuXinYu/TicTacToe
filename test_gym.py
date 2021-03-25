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


from tensorflow.keras.models import load_model
model0 = load_model('dqn_ttt0.h5')
model1 = load_model('dqn_ttt1.h5')



def one_player():
    import time
    ttt_env = tictactoe.TicTacToeEnv0()
    for i_episode in range(20):
        observation = ttt_env.reset()
        ttt_env.render()
        time.sleep(0.5)
            
        for t in range(10):
            # print(observation)
            if (observation==1).sum()%2 == 1:
                action = tictactoe.model_policy(model0, observation)
            else:
                action = tictactoe.model_policy(model1, observation)
                # action = ttt_env.action_space.sample()
            observation, reward, done, info = ttt_env.step(action)
            ttt_env.render()
            time.sleep(0.5)
            
            print(action,observation, reward, done)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
    ttt_env.close()


def two_player():
    import time
    import numpy as np
    ttt_env = tictactoe.TicTacToeEnv()
    for i_episode in range(20):
        observation = ttt_env.reset()
        ttt_env.render()
        time.sleep(0.5)
    
        for t in range(10):
            # print(observation)
            if (observation==1).sum()%2 == 1:
                action = tictactoe.model_policy(model0, observation)
                # state = np.mod(observation+1,3)
                # action = tictactoe.TicTacToeEnv0.avg_policy(state)
            else:
                action = tictactoe.model_policy(model1, observation)
                # state = np.mod(observation+1,3)
                # action = tictactoe.TicTacToeEnv0.avg_policy(state)
            observation, reward, done, info = ttt_env.step(action)
            ttt_env.render()
            time.sleep(0.5)
            
            print(action,observation, reward, done)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
    ttt_env.close()

if __name__ == '__main__':
    one_player()
    # two_player()