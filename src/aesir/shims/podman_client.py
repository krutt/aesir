# coding:utf-8
# Copyright (C) 2022-2025 All rights reserved.
# FILENAME:    ~~/src/aesir/shims/podman_client.py
# VERSION:     0.5.0
# CREATED:     2024-03-02 21:41
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from functools import cached_property
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryDirectory
from typing import BinaryIO, Generator

### Third-party packages ###
from podman import PodmanClient as OriginalPodmanClient, api
from podman.domain.images_manager import ImagesManager as OriginalImagesManager
from podman.errors.exceptions import ImageNotFound


class ImagesManager(OriginalImagesManager):
  def build(self, **kwargs) -> Generator[bytes, None, None]:  # type: ignore FIXME
    """Returns built image.

    Keyword Args:
      path (str) – Path to the directory containing the Dockerfile
      fileobj – A file object to use as the Dockerfile. (Or an IO object)
      tag (str) – A tag to add to the final image
      quiet (bool) – Whether to return the status
      nocache (bool) – Don’t use the cache when set to True
      rm (bool) – Remove intermediate containers. Default True
      timeout (int) – HTTP timeout
      custom_context (bool) – Optional if using fileobj (ignored)
      encoding (str) – The encoding for a stream. Set to gzip for compressing (ignored)
      pull (bool) – Downloads any updates to the FROM image in Dockerfile
      forcerm (bool) – Always remove intermediate containers, even after unsuccessful builds
      dockerfile (str) – full path to the Dockerfile / Containerfile
      buildargs (Mapping[str,str) – A dictionary of build arguments
      container_limits (dict[str, Union[int,str]]) –
        A dictionary of limits applied to each container created by the build process.
        Valid keys:

          - memory (int): set memory limit for build
          - memswap (int): Total memory (memory + swap), -1 to disable swap
          - cpushares (int): CPU shares (relative weight)
          - cpusetcpus (str): CPUs in which to allow execution, For example, "0-3", "0,1"
          - cpuperiod (int): CPU CFS (Completely Fair Scheduler) period (Podman only)
          - cpuquota (int): CPU CFS (Completely Fair Scheduler) quota (Podman only)
      shmsize (int) – Size of /dev/shm in bytes. The size must be greater than 0.
        If omitted the system uses 64MB
      labels (Mapping[str,str]) – A dictionary of labels to set on the image
      cache_from (list[str]) – A list of image's identifier used for build cache resolution
      target (str) – Name of the build-stage to build in a multi-stage Dockerfile
      network_mode (str) – networking mode for the run commands during build
      squash (bool) – Squash the resulting images layers into a single layer.
      extra_hosts (dict[str,str]) – Extra hosts to add to /etc/hosts in building
        containers, as a mapping of hostname to IP address.
      platform (str) – Platform in the format os[/arch[/variant]].
      isolation (str) – Isolation technology used during build. (ignored)
      use_config_proxy (bool) – (ignored)
      http_proxy (bool) - Inject http proxy environment variables into container (Podman only)
      layers (bool) - Cache intermediate layers during build.
      output (str) - specifies if any custom build output is selected for following build.
      outputformat (str) - The format of the output image's manifest and configuration data.

    Returns:
      first item is the podman.domain.images.Image built

      second item is the build logs

    Raises:
      BuildError: when there is an error during the build
      APIError: when service returns an error
      TypeError: when neither path nor fileobj is not specified
    """
    params = self._render_params(kwargs)

    body: BinaryIO
    path = None
    if "fileobj" in kwargs:
      path = TemporaryDirectory()
      filename = Path(path.name) / params["dockerfile"]  # type: ignore

      with open(filename, "w", encoding="utf-8") as file:
        copyfileobj(kwargs["fileobj"], file)
      body = api.create_tar(anchor=path.name, gzip=kwargs.get("gzip", False))
    elif "path" in kwargs:
      filename = Path(kwargs["path"]) / params["dockerfile"]  # type: ignore FIXME
      # The Dockerfile will be copied into the context_dir if needed
      params["dockerfile"] = api.prepare_containerfile(kwargs["path"], str(filename))  # type: ignore FIXME

      excludes = api.prepare_containerignore(kwargs["path"])
      body = api.create_tar(anchor=kwargs["path"], exclude=excludes, gzip=kwargs.get("gzip", False))

    post_kwargs = {}
    if kwargs.get("timeout"):
      post_kwargs["timeout"] = float(kwargs.get("timeout"))  # type: ignore

    response = self.client.post(  # type: ignore FIXME
      "/build",
      params=params,  # type: ignore FIXME
      data=body,  # type: ignore FIXME
      headers={
        "Content-type": "application/x-tar",
      },
      stream=True,
      **post_kwargs,
    )
    if hasattr(body, "close"):  # type: ignore FIXME
      body.close()  # type: ignore FIXME

    if hasattr(path, "cleanup"):
      path.cleanup()  # type: ignore FIXME
    response.raise_for_status(not_found=ImageNotFound)
    yield from response.raw


class PodmanClient(OriginalPodmanClient):
  """Custom `PodmanClient` clone with `build` method originally defined under
  podman-py BuildMixin subclass shimmed to return stream chunks
  """

  @cached_property
  def images(self) -> ImagesManager:
    """Returns Manager for operations on images stored by a Podman service."""
    return ImagesManager(client=self.api)


__all__ = ("PodmanClient",)
