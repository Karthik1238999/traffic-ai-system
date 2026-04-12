import traci
import json
import random

sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "simulation.sumocfg"]

traci.start(sumoCmd)

step = 0

while step < 500:
    traci.simulationStep()

    tls_ids = traci.trafficlight.getIDList()

    data = {}

    for tls in tls_ids:
        lanes = traci.trafficlight.getControlledLanes(tls)

        total_vehicles = 0

        for lane in lanes:
            total_vehicles += traci.lane.getLastStepVehicleNumber(lane)

        # ✅ AI SIGNAL CONTROL
        if total_vehicles > 10:
            traci.trafficlight.setPhaseDuration(tls, 30)
        else:
            traci.trafficlight.setPhaseDuration(tls, 10)

        # ✅ SIMPLE PREDICTION
        predicted = total_vehicles + random.randint(0, 3)

        data[tls] = {
            "current": total_vehicles,
            "predicted": predicted
        }

    # ✅ INCIDENT SIMULATION (random road block)
    if step == 200:
        edges = traci.edge.getIDList()
        blocked_edge = random.choice(edges)
        traci.edge.setMaxSpeed(blocked_edge, 0.1)  # simulate accident

        print(f"🚨 Incident simulated on edge: {blocked_edge}")

    # SAVE DATA
    with open("traffic_data.json", "w") as f:
        json.dump(data, f)

    step += 1

traci.close()