import numpy as np
from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)
Easy = EasyUrsinaNetworkingServer(Server)

positions = [
    np.array([-2, 0], dtype=float),
    np.array([2, 0], dtype=float),
]


@Server.event
def onClientConnected(Client):
    Easy.create_replicated_variable(
        f"disc_{Client.id}", {"id": Client.id, "position": positions[Client.id % 2]}
    )
    print(f"{Client} connected !")
    Client.send_message("GetId", Client.id)


@Server.event
def onClientDisconnected(Client):
    Easy.remove_replicated_variable_by_name(f"disc_{Client.id}")
    print(f"{Client} disconnected !")


@Server.event
def Move(Client, message):
    client_id = message["id"]
    position_disc = Easy.get_replicated_variable_by_name(f"disc_{client_id}").content[
        "position"
    ]
    Easy.update_replicated_variable_by_name(
        f"disc_{Client.id}", "position", position_disc + message["direction"]
    )


@Server.event
def Ping(Client, message):
    Client.send_message("Pong", {})


while True:
    Easy.process_net_events()
    time.sleep(1 / 60)
