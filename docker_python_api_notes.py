import docker

client = docker.from_env()

# Example of running the first timer

client.containers.run("ptp4l:latest", command="ptp4l -S -s -i eth0", auto_remove=True, network="multicast", name="ptp1", detach=True)

# Get first container
container = client.containers.get('ptp1')

# Kill container
container.kill()