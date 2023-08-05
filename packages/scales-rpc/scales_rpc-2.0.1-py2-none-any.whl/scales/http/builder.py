from .sink import (
  HttpTransportSink
)
from ..core import Scales
from ..loadbalancer.aperture import ApertureBalancerSink
from ..pool import SingletonPoolSink


class _HttpIface(object):
  def Get(self, url, **kwargs):
    """Issue an HTTP GET to url.

    kwargs aligns with arguments to requests, although timeout is ignored.
    """
    pass

  def Post(self, url, **kwargs):
    """Issue an HTTP POST to url.

    kwargs aligns with arguments to requests, although timeout is ignored.
    """
    pass

  def Put(self, url, **kwargs):
    """Issue an HTTP PUT to url.

    kwargs aligns with arguments to requests, although timeout is ignored.
    """
    pass

  def Delete(self, url, **kwargs):
    """Issue an HTTP DELETE to url.

    kwargs aligns with arguments to requests, although timeout is ignored.
    """
    pass

  def Patch(self, url, **kwargs):
    """Issue an HTTP PATCH to url.

    kwargs aligns with arguments to requests, although timeout is ignored.
    """
    pass

  def Head(self, url, **kwargs):
    """Issue an HTTP HEAD to url.

    kwargs aligns with arguments to requests, although timeout is ignored.
    """
    pass

  def Options(self, url, **kwargs):
    """Issue an HTTP OPTIONS to url.

    kwargs aligns with arguments to requests, although timeout is ignored.
    """
    pass


class Http(object):
  @staticmethod
  def NewBuilder():
    return Scales.NewBuilder(_HttpIface)\
      .WithSink(ApertureBalancerSink.Builder())\
      .WithSink(SingletonPoolSink.Builder())\
      .WithSink(HttpTransportSink.Builder())

  @staticmethod
  def NewClient(uri, timeout=60):
    return Http.NewBuilder()\
      .SetUri(uri)\
      .SetTimeout(timeout)\
      .Build()
