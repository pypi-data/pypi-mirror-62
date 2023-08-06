# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from hestia.tz_utils import local_now

from polyaxon_schemas.api.experiment import (
    ContainerGPUResourcesConfig,
    ContainerResourcesConfig,
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentJobStatusConfig,
    ExperimentMetricConfig,
    ExperimentStatusConfig
)


class TestExperimentConfigs(TestCase):
    def test_experiment_config(self):
        config_dict = {
            'uuid': uuid.uuid4().hex,
            'project': 'name.name',
            'experiment_group': 'name.name.1',
            'build_job': 'name.name.1',
            'unique_name': 'user.proj.1',
            'last_status': 'Running',
            'description': 'description',
            'content': "{'k': 'v'}",
            'is_managed': False,
            'tags': ['tag1'],
            'num_jobs': 1,
            'backend': 'foo',
            'framework': 'bar',
            'created_at': local_now().isoformat(),
            'updated_at': local_now().isoformat(),
            'has_tensorboard': True,
        }
        config = ExperimentConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('params')
        config_to_dict.pop('finished_at')
        config_to_dict.pop('is_clone')
        config_to_dict.pop('jobs')
        config_to_dict.pop('last_metric')
        config_to_dict.pop('resources')
        config_to_dict.pop('run_env')
        config_to_dict.pop('ttl')
        config_to_dict.pop('id')
        config_to_dict.pop('started_at')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        config_to_dict.pop('name')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict()
        config_dict.pop('uuid')
        config_dict.pop('description')
        config_dict.pop('content')
        config_dict.pop('project')
        config_dict.pop('updated_at')
        config_dict.pop('tags')
        config_dict.pop('num_jobs')
        config_dict.pop('is_managed')
        config_dict.pop('framework')
        config_dict.pop('backend')
        config_to_dict.pop('finished_at')
        config_to_dict.pop('id')
        config_to_dict.pop('started_at')
        config_dict.pop('has_tensorboard')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('started_at') is None

    def test_experiment_with_jobs_config(self):
        config_dict = {'id': 2,
                       'unique_name': 'adam.proj.1',
                       'uuid': uuid.uuid4().hex,
                       'project': 'user.name',
                       'experiment_group': 'user.name.1',
                       'last_status': 'Running',
                       'num_jobs': 1,
                       'backend': 'foo',
                       'framework': 'bar',
                       'created_at': local_now().isoformat(),
                       'updated_at': local_now().isoformat(),
                       'started_at': local_now().isoformat(),
                       'finished_at': local_now().isoformat(),
                       'has_tensorboard': False,
                       'is_managed': False,
                       'tags': ['tag'],
                       'jobs': [ExperimentJobConfig(uuid=uuid.uuid4().hex,
                                                    experiment=2,
                                                    created_at=local_now(),
                                                    updated_at=local_now(),
                                                    definition={}).to_dict()]}
        config = ExperimentConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict.pop('total_run') == '0s'
        config_to_dict.pop('params')
        config_to_dict.pop('description')
        config_to_dict.pop('is_clone')
        config_to_dict.pop('last_metric')
        config_to_dict.pop('resources')
        config_to_dict.pop('run_env')
        config_to_dict.pop('user')
        config_to_dict.pop('name')
        config_to_dict.pop('build_job')
        config_to_dict.pop('ttl')
        config_to_dict.pop('content')
        assert config_to_dict == config_dict

        config_dict.pop('tags')
        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('total_run') == '0s'
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('started_at') == 'a few seconds ago'
        assert config_to_dict.pop('finished_at') == 'a few seconds ago'

    def test_experiment_job_config(self):
        config_dict = {'uuid': uuid.uuid4().hex,
                       'experiment': 1,
                       'created_at': local_now().isoformat(),
                       'updated_at': local_now().isoformat(),
                       'started_at': local_now().isoformat(),
                       'finished_at': local_now().isoformat(),
                       'definition': {},
                       'role': 'master',
                       'id': 1,
                       'pod_id': 'job_1',
                       'unique_name': 'project.1.1.master'}
        config = ExperimentJobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict.pop('total_run') == '0s'
        config_to_dict.pop('last_status')
        config_to_dict.pop('resources')
        assert config_to_dict == config_dict

        config_dict.pop('definition')
        config_dict.pop('experiment')
        config_dict.pop('updated_at')
        config_dict.pop('uuid')
        config_to_dict = config.to_light_dict()
        assert config_to_dict.pop('total_run') == '0s'
        config_dict.pop('unique_name')
        config_to_dict.pop('last_status')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('total_run') == '0s'
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('started_at') == 'a few seconds ago'
        assert config_to_dict.pop('finished_at') == 'a few seconds ago'

    def test_experiment_status_config(self):
        config_dict = {'id': 1,
                       'uuid': uuid.uuid4().hex,
                       'experiment': 1,
                       'created_at': local_now().isoformat(),
                       'status': 'Running',
                       'traceback': 'None',
                       'message': None}
        config = ExperimentStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_dict.pop('experiment', None)
        config_dict.pop('uuid', None)
        config_dict.pop('traceback', None)
        config_to_dict = config.to_light_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'

    def test_experiment_metric_config(self):
        config_dict = {'id': 1,
                       'uuid': uuid.uuid4().hex,
                       'experiment': 1,
                       'created_at': local_now().isoformat(),
                       'values': {'accuracy': 0.9}}
        config = ExperimentMetricConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_dict.pop('experiment', None)
        config_dict.pop('uuid', None)
        config_to_dict = config.to_light_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'

    def test_experiment_job_status_config(self):
        config_dict = {'id': 1,
                       'uuid': uuid.uuid4().hex,
                       'job': 1,
                       'created_at': local_now().isoformat(),
                       'status': 'Running'}
        config = ExperimentJobStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('details')
        config_to_dict.pop('message')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict()
        config_dict.pop('details', None)
        config_dict.pop('job', None)
        config_dict.pop('uuid', None)
        config_to_dict.pop('message')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'

    def test_container_gpu_resources(self):
        config_dict = {
            'index': 0,
            'bus_id': '0000:00:1E.1',
            'memory_free': 10000,
            'memory_total': 12883853312,
            'memory_used': 8388608000,
            'memory_utilization': 0,
            'minor': 1,
            'name': 'GeForce GTX TITAN 0',
            'power_draw': 125,
            'power_limit': 250,
            'processes': [{'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 48448,
                           'username': 'user1'},
                          {'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 153223,
                           'username': 'user2'}],
            'serial': '0322917092147',
            'temperature_gpu': 80,
            'utilization_gpu': 76,
            'uuid': 'GPU-10fb0fbd-2696-43f3-467f-d280d906a107'
        }
        config = ContainerGPUResourcesConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('memory_free') == '9.77 Kb'
        assert config_to_dict.pop('memory_total') == '12.0 Gb'
        assert config_to_dict.pop('memory_used') == '7.81 Gb'

    def test_container_resources(self):
        gpu_resources = {
            'index': 0,
            'bus_id': '0000:00:1E.1',
            'memory_free': 10000,
            'memory_total': 12883853312,
            'memory_used': 8388608000,
            'memory_utilization': 0,
            'minor': 1,
            'name': 'GeForce GTX TITAN 0',
            'power_draw': 125,
            'power_limit': 250,
            'processes': [{'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 48448,
                           'username': 'user1'},
                          {'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 153223,
                           'username': 'user2'}],
            'serial': '0322917092147',
            'temperature_gpu': 80,
            'utilization_gpu': 76,
            'uuid': 'GPU-10fb0fbd-2696-43f3-467f-d280d906a107'
        }

        config_dict = {
            'job_uuid': uuid.uuid4().hex,
            'experiment_uuid': uuid.uuid4().hex,
            'job_name': 'master.0',
            'container_id': '3175e88873af9077688cee20eaadc0c07746efb84d01ae696d6d17ed9bcdfbc4',
            'n_cpus': 2,
            'cpu_percentage': 0.6947691836734693,
            'percpu_percentage': [0.4564075715616173, 0.23836161211185192],
            'memory_used': 84467712,
            'memory_limit': 2096160768,
            'gpu_resources': [gpu_resources]
        }
        config = ContainerResourcesConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('cpu_percentage') == '69.48%'
        assert config_to_dict.pop('memory_limit') == '1.95 Gb'
        assert config_to_dict.pop('memory_used') == '80.55 Mb'
