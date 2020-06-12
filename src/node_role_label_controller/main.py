import kopf
import asyncio
from kubernetes import client, config
from kubernetes.client import configuration

SOURCE_NODE_ROLE_PREFIX = 'node.kubernetes.io/'
TARGET_NODE_ROLE_PREFIX = 'node-role.kubernetes.io/'

@kopf.on.create("", "v1", "nodes")
@kopf.on.resume("", "v1", "nodes")
@kopf.on.update("", "v1", "nodes")
async def on_node(name, labels, logger, patch, **kwargs):
    for k, v in labels.items():
        if k.startswith(SOURCE_NODE_ROLE_PREFIX):
            role = k.replace(SOURCE_NODE_ROLE_PREFIX, '')
            node_role_label = f'{TARGET_NODE_ROLE_PREFIX}{role}'
            if not node_role_label in labels:
                logger.info(f"Found label {k}, about to add {node_role_label} in node {name}")
                patch.metadata.labels[node_role_label] = 'true'


@kopf.on.login(errors=kopf.ErrorsMode.PERMANENT)
async def login_fn(**kwargs):
    return kopf.login_via_client(**kwargs)
