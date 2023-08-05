# gressify

Adds a TCP IPv4 ingress/egress rule on a target vpc security group.

## Install

```bash
pip install gressify 
```

## Usage
```bash
gressify -g $GROUP_ID -i $IP
```
If IP not specified, public IP of the agent is assumed.


For more available arg options:
```bash
gressify --help
```