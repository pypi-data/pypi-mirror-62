from celery import chain

from django.conf import settings

from waldur_core.core import executors as core_executors
from waldur_core.core import tasks as core_tasks, utils as core_utils
from waldur_core.core.models import StateMixin

from . import tasks


class ClusterCreateExecutor(core_executors.BaseExecutor):

    @classmethod
    def get_task_signature(cls, instance, serialized_instance, user):
        _tasks = [core_tasks.BackendMethodTask().si(
            serialized_instance,
            'create_cluster',
            state_transition='begin_creating')]
        _tasks += cls.create_nodes(instance.node_set.all(), user)
        _tasks += [core_tasks.PollRuntimeStateTask().si(
            serialized_instance,
            backend_pull_method='check_cluster_creating',
            success_state=settings.WALDUR_RANCHER['ACTIVE_CLUSTER_STATE'],
            erred_state='error'
        )]
        return chain(*_tasks)

    @classmethod
    def create_nodes(cls, nodes, user):
        _tasks = []
        for node in nodes:
            serialized_instance = core_utils.serialize_instance(node)
            _tasks.append(tasks.CreateNodeTask().si(
                serialized_instance,
                user_id=user.id,
            ))
            _tasks.append(tasks.PollRuntimeStateNodeTask().si(serialized_instance))
        return _tasks


class ClusterDeleteExecutor(core_executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, instance, serialized_instance, user):
        if instance.node_set.count():
            return tasks.DeleteClusterNodesTask().si(
                serialized_instance,
                user_id=user.id,
            )
        else:
            return core_tasks.BackendMethodTask().si(
                serialized_instance,
                'delete_cluster',
                state_transition='begin_deleting')


class ClusterUpdateExecutor(core_executors.UpdateExecutor):

    @classmethod
    def get_task_signature(cls, instance, serialized_instance, **kwargs):
        if instance.backend_id and {'name'} & set(kwargs['updated_fields']):
            return core_tasks.BackendMethodTask().si(
                serialized_instance,
                'update_cluster',
                state_transition='begin_updating')
        else:
            return core_tasks.StateTransitionTask().si(
                serialized_instance,
                state_transition='begin_updating'
            )


class NodeCreateExecutor(core_executors.CreateExecutor):
    @classmethod
    def get_task_signature(cls, instance, serialized_instance, user):
        return chain(
            tasks.CreateNodeTask().si(
                serialized_instance,
                user_id=user.id,
            ),
            tasks.PollRuntimeStateNodeTask().si(serialized_instance)
        )


class NodeDeleteExecutor(core_executors.BaseExecutor):
    @classmethod
    def get_task_signature(cls, instance, serialized_instance, user):
        return tasks.DeleteNodeTask().si(
            serialized_instance,
            user_id=user.id,
        )

    @classmethod
    def pre_apply(cls, instance, **kwargs):
        """
        We can start deleting a node even if it does not have the status OK or Erred,
        because a virtual machine could already be created.
        """
        instance.state = StateMixin.States.DELETION_SCHEDULED
        instance.save(update_fields=['state'])


class ClusterPullExecutor(core_executors.ActionExecutor):

    @classmethod
    def get_task_signature(cls, cluster, serialized_cluster, **kwargs):
        return core_tasks.BackendMethodTask().si(
            serialized_cluster, 'pull_cluster', state_transition='begin_updating')
