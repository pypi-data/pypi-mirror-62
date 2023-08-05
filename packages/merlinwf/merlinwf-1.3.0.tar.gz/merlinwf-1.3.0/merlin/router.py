###############################################################################
# Copyright (c) 2019, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by the Merlin dev team, listed in the CONTRIBUTORS file.
# <merlin@llnl.gov>
#
# LLNL-CODE-797170
# All rights reserved.
# This file is part of Merlin, Version: 1.3.0.
#
# For details, see https://github.com/LLNL/merlin.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

"""
This module routes actions from the Merlin CLI to the appropriate tasking
logic.

This module is intended to help keep the task management layer (i.e., Celery)
decoupled from the logic the tasks are running.
"""
import logging
import os
from contextlib import suppress
from datetime import datetime

from merlin.study.celeryadapter import (
    create_celery_config,
    purge_celery_tasks,
    query_celery_queues,
    query_celery_workers,
    run_celery,
    start_celery_workers,
    stop_celery_workers,
)


try:
    import importlib.resources as resources
except ImportError:
    import importlib_resources as resources


LOG = logging.getLogger(__name__)


def run_task_server(study, run_mode=None):
    """
    Creates the task server interface for communicating the tasks.

    :param `study`: The MerlinStudy object
    :param `run_mode`: The type of run mode, e.g. local, batch
    """
    if study.spec.merlin["resources"]["task_server"] == "celery":
        run_celery(study, run_mode)
    else:
        LOG.error("Celery is not specified as the task server!")


def launch_workers(spec, steps, worker_args="", just_return_command=False):
    """
    Launches workers for the specified study.

    :param `specs`: Tuple of (YAMLSpecification, MerlinSpec)
    :param `steps`: The steps in the spec to tie the workers to
    :param `worker_args`: Optional arguments for the workers
    :param `just_return_command`: Don't execute, just return the command
    """
    if spec.merlin["resources"]["task_server"] == "celery":
        # Start workers
        cproc = start_celery_workers(spec, steps, worker_args, just_return_command)
        return cproc
    else:
        LOG.error("Celery is not specified as the task server!")


def purge_tasks(task_server, spec, force, steps):
    """
    Purges all tasks.

    :param `task_server`: The task server from which to purge tasks.
    :param `spec`: A MerlinSpec object
    :param `force`: Purge without asking for confirmation
    :param `steps`: Space-separated list of stepnames defining queues to purge,
        default is all steps
    """
    LOG.info(f"Purging queues for steps = {steps}")

    if task_server == "celery":
        queues = spec.make_queue_string(steps)
        # Purge tasks
        return purge_celery_tasks(queues, force)
    else:
        LOG.error("Celery is not specified as the task server!")


def query_status(task_server, spec, steps):
    """
    Queries status of queues in spec file from server.

    :param `task_server`: The task server from which to purge tasks.
    :param `spec`: A MerlinSpec object
    :param `steps`: Spaced-separated list of stepnames to query. Default is all
    """
    LOG.info(f"Querying queues for steps = {steps}")

    if task_server == "celery":
        queues = spec.get_queue_list(steps)
        # Query the queues
        return query_celery_queues(queues)
    else:
        LOG.error("Celery is not specified as the task server!")


def dump_status(query_return, csv_file):
    """
    Dump the results of a query_status to a csv file.

    :param `query_return`: The output of query_status
    :param `csv_file`: The csv file to append
    """
    if os.path.exists(csv_file):
        fmode = "a"
    else:
        fmode = "w"
    with open(csv_file, mode=fmode) as f:
        if f.mode == "w":  # add the header
            f.write("# time")
            for name, job, consumer in query_return:
                f.write(f",{name}:tasks,{name}:consumers")
            f.write("\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        for name, job, consumer in query_return:
            f.write(f",{job},{consumer}")
        f.write("\n")


def query_workers(task_server):
    """
    Gets info from workers.

    :param `task_server`: The task server to query.
    """
    LOG.info(f"Searching for workers...")

    if task_server == "celery":
        # Stop workers
        return query_celery_workers()
    else:
        LOG.error("Celery is not specified as the task server!")


def stop_workers(task_server, spec_worker_names, queues, workers_regex):
    """
    Stops workers.

    :param `task_server`: The task server from which to stop workers.
    :param `spec_worker_names`: Worker names to stop, drawn from a spec.
    :param `queues`     : The queues to stop
    :param `workers_regex`    : Regex for workers to stop
    """
    LOG.info(f"Stopping workers...")

    if task_server == "celery":
        # Stop workers
        return stop_celery_workers(queues, spec_worker_names, workers_regex)
    else:
        LOG.error("Celery is not specified as the task server!")


def route_for_task(name, args, kwargs, options, task=None, **kw):
    """
    Custom task router for queues
    """
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}


def create_config(task_server, config_dir, broker):
    """
    Create a config for the given task server.

    :param `task_server`: The task server from which to stop workers.
    :param `config_dir`: Optional directory to install the config.
    """
    LOG.info(f"Creating config ...")

    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    if task_server == "celery":
        config_file = "app.yaml"
        data_config_file = "app.yaml"
        if broker == "redis":
            data_config_file = "app_redis.yaml"
        with resources.path("merlin.data.celery", data_config_file) as data_file:
            create_celery_config(config_dir, config_file, data_file)
    else:
        LOG.error("Only celery can be configured currently.")
