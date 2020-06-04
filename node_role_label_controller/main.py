import kopf
import asyncio
from kubernetes import client, config
from kubernetes.client import configuration

NODE_ROLE_PREFIX = 'node.kubernetes.io/'

@kopf.on.create("", "v1", "nodes")
@kopf.on.resume("", "v1", "nodes")
@kopf.on.update("", "v1", "nodes")
async def on_node(name, labels, logger, patch, **kwargs):
    for k, v in labels.items():
        if k.startswith(NODE_ROLE_PREFIX):
            role = k.replace(NODE_ROLE_PREFIX, '')
            node_role_label = f'node-role.kubernetes.io/{role}'
            if not node_role_label in labels:
                logger.info(f"Found label {k}, about to add {node_role_label} in node {name}")
                patch.metadata.labels[node_role_label] = 'true'


@kopf.on.login(errors=kopf.ErrorsMode.PERMANENT)
async def login_fn(**kwargs):
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    contexts, active_context = config.list_kube_config_contexts()
    print(active_context)

    conf = configuration.Configuration()
    token = conf.api_key['authorization'].split(' ')[1]
    server = conf.host
    verify_ssl = conf.verify_ssl
    ssl_ca_cert = conf.ssl_ca_cert

    return kopf.ConnectionInfo(
        server=server,
        insecure=True,
        scheme='Bearer',
        token=token,
    )