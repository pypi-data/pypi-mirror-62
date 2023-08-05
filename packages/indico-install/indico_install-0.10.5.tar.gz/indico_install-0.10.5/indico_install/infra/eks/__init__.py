#!/usr/bin/env python3
from pathlib import Path
from click import secho

import click
import yaml

from indico_install.infra.init import init
from indico_install.infra.eks import cluster, config, database, network, storage
from indico_install.config import ConfigsHolder, merge_dicts
from indico_install.utils import run_cmd, options_wrapper

SOURCES = [network, storage, database, cluster]


@click.group("eks")
@click.pass_context
def eks(ctx):
    """
    Indico infrastructure setup and validation for AWS Kubernetes Service
    """
    ctx.ensure_object(dict)
    if not ((config.access_key and config.access_secret) or config.aws_profile):
        secho("Missing AWS credentials for EKS", fg="yellow")
    else:
        secho(
            f"Using AWS profile: {config.aws_profile}"
            if config.aws_profile
            else f"Using AWS access key: {config.access_key[:5]}****",
            fg="blue",
        )


eks.command("init")(init(__name__))


@eks.command("check")
@click.pass_context
@options_wrapper(check_input=True)
def check(ctx, *, input_yaml, **kwargs):
    """Validate all resources"""
    try:
        ctx.obj["SESSION"] = config.Session()
    except Exception as e:
        secho(f"AWS Session could not be generated: {e}", fg="red")
        return
    if not input_yaml.is_file():
        click.secho(f"Could not find {input_yaml}.", fg="red")
        return
    failed = 0
    user_conf = ConfigsHolder(config=input_yaml)
    config.ask_for_infra_input(user_conf)
    user_conf.save()
    for resource in SOURCES:
        resource_name = resource.__name__
        secho(f"Validating {resource_name}...")
        try:
            resource.validate(user_conf, session=ctx.obj["SESSION"])
        except Exception as e:
            secho(f"{resource_name} NOT OK! Error: {e}\n", fg="red")
            failed += 1
        else:
            secho(f"{resource_name} OK!\n", fg="green")
    secho(
        f"Validation complete: {failed} errors",
        fg="red" if failed else "green",
        bold=True,
    )


@eks.command("create")
@click.pass_context
@click.option("--eksctl-file", help="eksctl config file used to create cluster")
@options_wrapper(check_input=True)
def create(ctx, *, input_yaml, eksctl_file, **kwargs):
    """
    Install the nvidia driver on the cluster
    """
    run_cmd(
        "kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml"
    )
    user_conf = ConfigsHolder(input_yaml)

    if not eksctl_file or not Path(eksctl_file).is_file():
        config.ask_for_infra_input(user_conf)
    else:
        with open(eksctl_file, "r") as conf_file:
            conf = yaml.safe_load(conf_file)

        cluster_name = conf["metadata"]["name"]
        user_conf["cluster"] = user_conf.get("cluster", {}) or {}
        user_conf["cluster"]["name"] = cluster_name

        if "public" not in conf["vpc"]["subnets"]:
            user_conf["services"] = merge_dicts(
                user_conf.get("services", {}),
                {
                    "app-edge": {
                        "values": {
                            "annotations": {
                                "service.beta.kubernetes.io/aws-load-balancer-internal": "0.0.0.0/0"
                            }
                        }
                    }
                },
            )
    user_conf.save()
