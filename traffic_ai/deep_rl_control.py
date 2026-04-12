import traci
import torch
import torch.nn as nn
import torch.optim as optim
import random
import json

# SUMO setup
sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "simulation.sumocfg"]

# Neural Network (Policy)
class PolicyNet(nn.Module):
    def __init__(self):
        super(PolicyNet, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(1, 16),
            nn.ReLU(),
            nn.Linear(16, 3)  # 3 actions
        )

    def forward(self, x):
        return self.fc(x)

model = PolicyNet()
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.MSELoss()

actions = [10, 20, 30]

def choose_action(state):
    state_tensor = torch.tensor([[state]], dtype=torch.float32)
    output = model(state_tensor)

    action_idx = torch.argmax(output).item()
    return action_idx, actions[action_idx], output

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

        state = float(total)

        action_idx, action, output = choose_action(state)

        traci.trafficlight.setPhaseDuration(tls, action)

        # Reward: minimize vehicles
        reward = -state

        target = output.clone().detach()
        target[0][action_idx] = reward

        loss = criterion(output, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        predicted = total + random.randint(0, 3)

        data[tls] = {
            "current": total,
            "predicted": predicted,
            "action": action
        }

    with open("traffic_data.json", "w") as f:
        json.dump(data, f)

    step += 1

traci.close()

print("Deep RL simulation completed")