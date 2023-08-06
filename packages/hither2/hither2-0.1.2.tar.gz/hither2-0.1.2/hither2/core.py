import time
from typing import Union, Any
import os
import sys
import kachery as ka
from ._etconf import ETConf
from ._shellscript import ShellScript
from ._generate_source_code_for_function import _generate_source_code_for_function
from ._run_serialized_job_in_container import _run_serialized_job_in_container
from ._util import _random_string, _docker_form_of_container_string, _deserialize_item, _serialize_item
from .jobcache import JobCache
from .file import File

_default_global_config = dict(
    container=None,
    job_handler=None,
    job_cache=None,
    download_results=None,
    job_timeout=None
    # cache=None,
    # cache_failing=None,
    # rerun_failing=None,
    # force_run=None,
    # gpu=None,
    # exception_on_fail=None, # None means True
    # job_handler=None,
    # show_console=None, # None means True
    # show_cached_console=None, # None means False
    # job_timeout=None,
    # log_path=None
)

_global_config = ETConf(
    defaults=_default_global_config
)

def set_config(
        container: Union[str, bool, None]=None,
        job_handler: Any=None,
        job_cache: Union[JobCache, None]=None,
        download_results: Union[bool, None]=None,
        job_timeout: Union[float, None]=None
) -> None:
    _global_config.set_config(
        container=container,
        job_handler=job_handler,
        job_cache=job_cache,
        download_results=download_results,
        job_timeout=job_timeout
    )

class config:
    def __init__(self,
        container: Union[str, bool, None]=None,
        job_handler: Any=None,
        job_cache: Union[JobCache, None]=None,
        download_results: Union[bool, None]=None,
        job_timeout: Union[float, None]=None
    ):
        self._config = dict(
            container=container,
            job_handler=job_handler,
            job_cache=job_cache,
            download_results=download_results,
            job_timeout=job_timeout
        )
        self._old_config = None
    def __enter__(self):
        self._old_config = _global_config.get_config()
        set_config(**self._config)
    def __exit__(self, exc_type, exc_val, exc_tb):
        _global_config.set_full_config(self._old_config)

class _JobManager:
    def __init__(self) -> None:
        self._queued_jobs = dict()
        self._running_jobs = dict()
    def queue_job(self, job):
        job._status = 'queued'
        self._queued_jobs[job._job_id] = job
    def iterate(self):
        # Called periodically during wait()
    
        # Check which queued jobs are ready to run
        queued_job_ids = list(self._queued_jobs.keys())

        # Check which containers need to be prepared (pulled or built)
        for id in queued_job_ids:
            job: Job = self._queued_jobs[id]
            if job._container is not None:
                if not job._job_handler.is_remote:
                    try:
                        _prepare_container(job._container)
                    except:
                        job._status = 'error'
                        job._exception = Exception(f'Unable to prepare container for job {job._label}: {job._container}')

        # Check which queued jobs are ready to run (and remove jobs where status!='queued')
        for id in queued_job_ids:
            job: Job = self._queued_jobs[id]
            if job._status != 'queued':
                del self._queued_jobs[id]
            elif self._job_is_ready_to_run(job):
                del self._queued_jobs[id]
                if _some_jobs_have_status(job._kwargs, ['error']):
                    exc = _get_job_exception_in_item(job._kwargs)
                    job._status = 'error'
                    job._exception = Exception(f'Exception in argument. {str(exc)}')
                else:
                    self._running_jobs[id] = job
                    job._kwargs = _resolve_job_values(job._kwargs)
                    if job._job_cache is not None:
                        if not job._job_handler.is_remote:
                            job._job_cache.check_job(job)
                    if job._status == 'queued':
                        # still queued even after checking the cache
                        job._status = 'running'
                        job._job_handler.handle_job(job)

        # Check which running jobs are finished and iterate job handlers of running jobs
        running_job_ids = list(self._running_jobs.keys())
        for id in running_job_ids:
            job: Job = self._running_jobs[id]
            if job._status == 'running':
                # Note: we effectively iterate the same job handler potentially many times here -- I think that's okay but not 100% sure.
                job._job_handler.iterate()
            if job._status in ['error', 'finished']:
                if job._download_results:
                    _download_files_as_needed_in_item(job._result)
                if job._job_cache is not None:
                    if not job._job_handler.is_remote:
                        job._job_cache.cache_job_result(job)
                del self._running_jobs[id]
    
    def reset(self):
        self._queued_jobs = dict()
        self._running_jobs = dict()
    
    def wait(self, timeout: Union[float, None]=None):
        timer = time.time()
        while True:
            self.iterate()
            if self._queued_jobs == {} and self._running_jobs == {}:
                return
            time.sleep(0.02)
            elapsed = time.time() - timer
            if timeout is not None and elapsed > timeout:
                return
    
    def _job_is_ready_to_run(self, job):
        assert job._status == 'queued'
        if _some_jobs_have_status(job._kwargs, ['error']):
            # In this case the job will error due to an error input
            return True
        if _some_jobs_have_status(job._kwargs, ['pending', 'queued', 'running']):
            return False
        return True

_global_job_manager = _JobManager()

def reset():
    _global_job_manager.reset()
    set_config(**_default_global_config)

def container(container):
    assert container.startswith('docker://'), f"Container string {container} must begin with docker://"
    def wrap(f):
        setattr(f, '_hither_container', container)
        return f
    return wrap

def additional_files(additional_files):
    def wrap(f):
        setattr(f, '_hither_additional_files', additional_files)
        return f
    return wrap

def local_modules(local_modules):
    def wrap(f):
        setattr(f, '_hither_local_modules', local_modules)
        return f
    return wrap

def wait(timeout: Union[float, None]=None):
    _global_job_manager.wait(timeout)

def function(name, version):
    def wrap(f):
        assert f.__name__ == name, f"Name does not match function name: {name} <> {f.__name__}"
        def run(**kwargs):
            if _global_config.get('container') is True:
                container = getattr(f, '_hither_container', None)
            elif _global_config.get('container') is not None and _global_config.get('container') is not False:
                container = _global_config.get('container')
            else:
                container=None
            job_handler = _global_config.get('job_handler')
            job_cache = _global_config.get('job_cache')
            if job_handler is None:
                job_handler = _global_job_handler
            download_results = _global_config.get('download_results')
            if download_results is None:
                download_results = False
            job_timeout = _global_config.get('job_timeout')
            label = name
            job = Job(f=f, kwargs=kwargs, job_manager=_global_job_manager, job_handler=job_handler, job_cache=job_cache, container=container, label=label, download_results=download_results, job_timeout=job_timeout)
            _global_job_manager.queue_job(job)
            return job
        setattr(f, 'run', run)
        setattr(f, '_hither_name', name)
        setattr(f, '_hither_version', version)
        return f
    return wrap

def _download_files_as_needed_in_item(x):
    if isinstance(x, File):
        info0 = ka.get_file_info(x._sha1_path, fr=None)
        if info0 is None:
            remote_handler = getattr(x, '_remote_job_handler')
            assert remote_handler is not None, f'Unable to find file: {x._sha1_path}'
            a = remote_handler._load_file(x._sha1_path)
            assert a is not None, f'Unable to load file {x._sha1_path} from remote compute resource: {remote_handler._compute_resource_id}'
        else:
            pass
    elif type(x) == dict:
        for val in x.values():
            _download_files_as_needed_in_item(val)
    elif type(x) == list:
        for val in x:
            _download_files_as_needed_in_item(val)
    elif type(x) == tuple:
        for val in x:
            _download_files_as_needed_in_item(val)
    else:
        pass

class DefaultJobHandler:
    def __init__(self):
        self.is_remote = False
    def handle_job(self, job):
        job._execute()

_global_job_handler = DefaultJobHandler()

class Job:
    def __init__(self, *, f, kwargs, job_manager, job_handler, job_cache, container, label, download_results, job_timeout: Union[float, None], code=None, function_name=None, function_version=None, job_id=None):
        self._f = f
        self._code = code
        self._function_name = function_name
        self._function_version = function_version
        self._label = label
        self._kwargs = kwargs
        # the following is important for converting ndarray items into File items
        self._kwargs = _deserialize_item(_serialize_item(self._kwargs))
        self._job_id = job_id
        if self._job_id is None:
            self._job_id = _random_string(15)
        self._container = container
        self._download_results = download_results
        self._job_timeout = None

        self._status = 'pending'
        self._result = None
        self._runtime_info = None
        self._exception: Union[Exception, None] = None

        self._job_handler = job_handler
        self._job_manager = job_manager
        self._job_cache = job_cache

        if self._function_name is None:
            self._function_name = getattr(self._f, '_hither_name')
        if self._function_version is None:
            self._function_version = getattr(self._f, '_hither_version')
    def wait(self, timeout: Union[float, None]=None):
        timer = time.time()
        while True:
            self._job_manager.iterate()
            if self._status == 'finished':
                return self._result
            elif self._status == 'error':
                assert self._exception is not None
                raise self._exception
            elif self._status == 'queued':
                pass
            elif self._status == 'running':
                pass
            else:
                raise Exception(f'Unexpected status: {self._status}') # pragma: no cover
            time.sleep(0.02)
            elapsed = time.time() - timer
            if timeout is not None and elapsed > timeout:
                return None
    def result(self):
        if self._status == 'finished':
            return self._result
        raise Exception('Cannot get result of job that is not yet finished.')
    def exception(self):
        if self._status == 'error':
            assert self._exception is not None
        return self._exception
    def set(self, *, label=None):
        if label is not None:
            self._label = label
        return self
    def _execute(self):
        if self._container is not None:
            job_serialized = self._serialize(generate_code=True)
            success, result, runtime_info, error = _run_serialized_job_in_container(job_serialized)
            self._runtime_info = runtime_info
            if success:
                self._result = result
                self._status = 'finished'
            else:
                assert error is not None
                assert error != 'None'
                self._exception = Exception(error)
                self._status = 'error'
        else:
            assert self._f is not None, 'Cannot execute job outside of container when function is not available'
            try:
                kwargs2 = _resolve_files_in_item(self._kwargs)
                ret = self._f(**kwargs2)
                self._result = _deserialize_item(_serialize_item(ret))
                self._status = 'finished'
            except Exception as e:
                self._status = 'error'
                self._exception = e
    def _serialize(self, generate_code):
        function_name = self._function_name
        function_version = self._function_version
        if generate_code:
            if self._code is not None:
                code = self._code
            else:
                assert self._f is not None, 'Cannot serialize function with generate_code=True when function and code are both not available'
                additional_files = getattr(self._f, '_hither_additional_files', [])
                local_modules = getattr(self._f, '_hither_local_modules', [])
                code = _generate_source_code_for_function(self._f, name=function_name, additional_files=additional_files, local_modules=local_modules)
            function = None
        else:
            assert self._f is not None, 'Cannot serialize function with generate_code=False when function is not available'
            code = None
            function = self._f
        x = dict(
            job_id=self._job_id,
            function=function,
            code=code,
            function_name=function_name,
            function_version=function_version,
            label=self._label,
            kwargs=_serialize_item(self._kwargs),
            container=self._container,
            download_results=self._download_results,
            job_timeout=self._job_timeout
        )
        x = _serialize_item(x)
        return x
    
    @staticmethod
    def _deserialize(serialized_job, job_manager=None):
        j = serialized_job
        return Job(
            f=j['function'],
            code=j['code'],
            function_name=j['function_name'],
            function_version=j['function_version'],
            label=j['label'],
            kwargs=_deserialize_item(j['kwargs']),
            container=j['container'],
            download_results=j.get('download_results', False),
            job_timeout=j.get('job_timeout', None),
            job_manager=job_manager,
            job_handler=None,
            job_cache=None,
            job_id=j['job_id']
        )

def _deserialize_job(serialized_job):
    return Job._deserialize(serialized_job)

def _resolve_files_in_item(x):
    if isinstance(x, File):
        if x._item_type == 'file':
            path = ka.load_file(x._sha1_path)
            assert path is not None, f'Unable to load file: {x._sha1_path}'
            return path
        elif x._item_type == 'ndarray':
            return x.array()
        else:
            raise Exception(f'Unexpected item type: {x._item_type}')
    elif type(x) == dict:
        ret = dict()
        for key, val in x.items():
            ret[key] = _resolve_files_in_item(val)
        return ret
    elif type(x) == list:
        return [_resolve_files_in_item(val) for val in x]
    elif type(x) == tuple:
        return tuple([_resolve_files_in_item(val) for val in x])
    else:
        return x

def _some_jobs_have_status(x, status_list):
    if isinstance(x, Job):
        if x._status in status_list:
            return True
    elif type(x) == dict:
        for v in x.values():
            if _some_jobs_have_status(v, status_list):
                return True
    elif type(x) == list:
        for v in x:
            if _some_jobs_have_status(v, status_list):
                return True
    elif type(x) == tuple:
        for v in x:
            if _some_jobs_have_status(v, status_list):
                return True
    return False

def _get_job_exception_in_item(x):
    if isinstance(x, Job):
        if x._status == 'error':
            return f'{x._label}: {str(x._exception)}'
    elif type(x) == dict:
        for v in x.values():
            exc = _get_job_exception_in_item(v)
            if exc is not None:
                return exc
    elif type(x) == list:
        for v in x:
            exc = _get_job_exception_in_item(v)
            if exc is not None:
                return exc
    elif type(x) == tuple:
        for v in x:
            exc = _get_job_exception_in_item(v)
            if exc is not None:
                return exc
    return None

def _resolve_job_values(x):
    if isinstance(x, Job):
        return x._result
    elif type(x) == dict:
        ret = dict()
        for k, v in x.items():
            ret[k] = _resolve_job_values(v)
        return ret
    elif type(x) == list:
        return [_resolve_job_values(v) for v in x]
    elif type(x) == tuple:
        return tuple([_resolve_job_values(v) for v in x])
    else:
        return x

_prepared_singularity_containers = dict()
_prepared_docker_images = dict()

def _prepare_container(container):
    if os.getenv('HITHER_USE_SINGULARITY', None) == 'TRUE':
        if container not in _prepared_singularity_containers:
            _do_prepare_singularity_container(container)
            _prepared_singularity_containers[container] = True
    else:
        if os.getenv('HITHER_DO_NOT_PULL_DOCKER_IMAGES', None) != 'TRUE':
            if container not in _prepared_docker_images:
                _do_pull_docker_image(container)
                _prepared_docker_images[container] = True


def _do_prepare_singularity_container(container):
    print(f'Building singularity container: {container}')
    ss = ShellScript(f'''
        #!/bin/bash

        exec singularity run {container} echo "built {container}"
    ''')
    ss.start()
    retcode = ss.wait()
    if retcode != 0:
        raise Exception(f'Problem building container {container}')

def _do_pull_docker_image(container):
    print(f'Pulling docker container: {container}')
    container = _docker_form_of_container_string(container)
    if (sys.platform == "win32"):
        if 1: # pragma: no cover
            ss = ShellScript(f'''
                docker pull {container}
            ''')
    else:
        ss = ShellScript(f'''
            #!/bin/bash
            set -ex
            
            exec docker pull {container}
        ''')
    ss.start()
    retcode = ss.wait()
    if retcode != 0:
        raise Exception(f'Problem pulling container {container}')

