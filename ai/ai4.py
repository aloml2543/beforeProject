import gym
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from collections import deque
from  tensorflow.keras.losses import Huber
import tensorflow as tf

tf.debugging.set_log_device_placement(False)

NUM_EPISODE = 500
MAX_STEPS = 200
GAMMA = 0.99
WARMUP = 10

E_START = 1.0
E_STOP = 0.01
E_DECAY_RATE = 0.001

MEMORY_SIZE = 10000
BATCH_SIZE = 32

class QNetwork:
    def __init__(self, state_size, action_size):
        self.model = Sequential()
        self.model.add(Dense(16, activation='relu', input_dim = state_size))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(action_size, activation='linear'))

        self.model.compile(loss=Huber(), optimizer = 'Adam')

class Memory():
    def __init__(self, memory_size):
        self.buffer = deque(maxlen = memory_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)), size = batch_size, replace = False)
        return [self.buffer[i] for i in idx]

    def __len__(self):
        return len(self.buffer)


env = gym.make('CartPole-v0')
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

main_qn = QNetwork(state_size, action_size)
target_qn = QNetwork(state_size, action_size)
memory = Memory(MEMORY_SIZE)

state = env.reset()
state = np.reshape(state, [1, state_size])

total_step = 0
success_count = 0
for episode in range(1, NUM_EPISODE+1):
    step = 0

    target_qn.model.set_weights(main_qn.model.get_weights())

    for _ in  range(1, MAX_STEPS+1):
        step+=1
        total_step +=1

        epsilon = E_STOP + (E_START - E_STOP) * np.exp(-E_DECAY_RATE * total_step)

        if epsilon > np.random.rand():
            action = env.action_space.sample()
        else:
            action = np.argmax(main_qn.model.predict(state)[0])

        next_state, _, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])

        if done:
            if step >=190:
                success_count += 1
                reward = 1
            else:
                success_count = 0
                reward = 0

            next_state = np.zeros(state.shape)

            if step > WARMUP:
                memory.add((state, action, reward, next_state))

        else:
            reward = 0

            if step > WARMUP:
                memory.add((state, action, reward, next_state))

            state = next_state
        if len(memory) >= BATCH_SIZE:
            inputs = np.zeros((BATCH_SIZE, 4))
            targets = np.zeros((BATCH_SIZE, 2))

            minibatch = memory.sample(BATCH_SIZE)

            for i, (state_b, action_b, reward_b, next_state_b) in enumerate(minibatch):
                inputs[i] = state_b

                if not (next_state_b == np.zeros(state_b.shape)).all(axis=1):
                    target = reward_b + GAMMA * np.amax(target_qn.model.predict(next_state_b)[0])
                else:
                    target = reward_b
                
                targets[i] = main_qn.model.predict(state_b)
                targets[i][action_b] = target

            main_qn.model.fit(inputs, targets, epochs=1, verbose=0)

        if done:
            break

    print('에피소드: {}, 스텝 수: {}, epsilon: {:.4f}'.format(episode, step, epsilon))
        


    if success_count >= 5:
        break
    
    state = env.reset()
    state = np.reshape(state, [1, state_size])