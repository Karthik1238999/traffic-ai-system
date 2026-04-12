import traci
import json
import random

sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "simulation.sumocfg"]

# Q-table (state → action)
Q = {}

actions = [10, 20, 30]  # green durations

alpha = 0.1
gamma = 0.9
epsilon = 0.2

def get_state(vehicles):
    if vehicles < 5:
        return "low"
    elif vehicles < 15:
        return "medium"
    else:
        return "high"

def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions)
    return max(Q.get(state, {}), key=Q.get(state, {}).get, default=random.choice(actions))

def update_q(state, action, reward, next_state):
    if state not in Q:
        Q[state] = {a: 0 for a in actions}

    if next_state not in Q:
        Q[next_state] = {a: 0 for a in actions}

    Q[state][action] += alpha * (
        reward + gamma * max(Q[next_state].values()) - Q[state][action]
    )

traci.start(sumoCmd)

step = 0

while step < 500:
    traci.simulationStep()

    tls_ids = traci.trafficlight.getIDList()

    data = {}

    for tls in tls_ids:
        lanes = traci.trafficlight.getControlledLanes(tls)

        total = 0
        for lane in lanes:
            total += traci.lane.getLastStepVehicleNumber(lane)

        state = get_state(total)

        action = choose_action(state)

        # Apply action (green time)
        traci.trafficlight.setPhaseDuration(tls, action)

        # Reward: less vehicles = better
        reward = -total

        next_state = get_state(total)

        update_q(state, action, reward, next_state)

        # Prediction
        predicted = total + random.randint(0, 3)

        data[tls] = {
            "current": total,
            "predicted": predicted,
            "action": action
        }

    # Save data
    with open("traffic_data.json", "w") as f:
        json.dump(data, f)

    step += 1

traci.close()

print("Q-table learned:")
print(Q)