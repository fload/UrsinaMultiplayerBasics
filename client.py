import time

import numpy as np
from ursina import *
from ursinanetworking import *

window.borderless = False
window.vsync = True

app = Ursina(
    title="Square Game",
)
Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)

SelfId = -1
entity_map = {}
actions_player = np.array([0, 0], dtype=float)
current_time = 0


@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}")


@Easy.event
def onReplicatedVariableCreated(variable):
    global Client
    disc_entity = Entity(
        model="quad",
        color="#000000",
        scale=1,
        position=variable.content["position"],
    )
    entity_map[variable.name] = disc_entity


@Easy.event
def onReplicatedVariableUpdated(variable):
    entity_map[variable.name].position = variable.content["position"]


@Easy.event
def onReplicatedVariableRemoved(variable):
    global Client
    destroy(entity_map[variable.name])


@Client.event
def Pong(message):
    print(f"Pong {(time.time_ns() - current_time) * 1e-6}ms")


def action_handle():
    global actions_player
    global Client
    actions_player = np.array([0, 0], dtype=float)
    for key, value in held_keys.items():
        if value != 0:
            if key == Keys.right_arrow:
                actions_player[0] += 1
            if key == Keys.left_arrow:
                actions_player[0] -= 1
            if key == Keys.up_arrow:
                actions_player[1] += 1
            if key == Keys.down_arrow:
                actions_player[1] -= 1

    if actions_player[0] != 0 or actions_player[1] != 0:
        Client.send_message("Move", {"id": SelfId, "direction": actions_player * 0.05})


def input(key):
    global current_time
    if key == "p":
        Client.send_message("Ping", {})
        current_time = time.time_ns()


def update():
    action_handle()
    Easy.process_net_events()


app.run()
