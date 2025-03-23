# Docker Mininet + OpenDaylight Oxygen

This repository contains Docker configurations to run Mininet and OpenDaylight Oxygen SDN controller in separate containers.

Limitation: ODL works only on x64_64 architectures for oxygen with UI.

## Features

- OpenDaylight Oxygen with UI (DLUX) enabled - Runs only on amd64
- Mininet with OpenVSwitch support
- Containers networked for SDN experimentation
- Persistent storage for OpenDaylight configuration

## Quick Start

Build and start the containers:

```bash
docker-compose up -d
```

Wait for OpenDaylight to initialize fully (about 1-2 minutes).

## Accessing OpenDaylight UI

Access the OpenDaylight DLUX web interface at:

```
http://<host-ip>:8181/index.html
```

Default credentials:
- Username: `admin`
- Password: `admin`

## Creating a Mininet Topology

Connect to the Mininet container:

```bash
docker exec -it mininet bash
```

Create a simple topology connected to the OpenDaylight controller:

```bash
mn --controller=remote,ip=opendaylight,port=6633 --topo tree,2
```

## Verifying Connection

In the OpenDaylight UI, navigate to "Topology" to view the network.

You can also check OpenFlow switch connections using the REST API:

```bash
curl -u admin:admin http://<host-ip>:8181/restconf/operational/opendaylight-inventory:nodes/
```

## Custom Topologies

Place your custom Python topology scripts in the `topologies` directory, which is mounted to the Mininet container.

## Troubleshooting

If OpenDaylight doesn't start properly, check the logs:

```bash
docker logs odl-oxygen
```

## License

This project is open source and available under the [MIT License](LICENSE).
