# surfacescan

Attack surface scanner

## Run local

### Prerequisites

* docker
* docker-compose
* poetry (global or virtualenv)
* locust (options, global or virtualenv)

### Docker way

Build images
```console
foo@bar:~$ docker-compose build
```

Run api
```console
foo@bar:~$ docker-compose up -d api
```

Run lint (flake8)
```console
foo@bar:~$ docker-compose run --rm lint
```

Run tests (pytest)
```console
foo@bar:~$ docker-compose run --rm tests
```

To run locust execute

```console
foo@bar:~$ docker-compose up -d locust
```

Open in the browser `http://localhost:8089` and specify http://api:8001 as host
to be tested.

### Non docker way

Install dependencies
```console
foo@bar:~$ poetry install
```

Run flake8
```console
foo@bar:~$ flake8
```
Run tests
```console
foo@bar:~$ pytest
```

Start service
```console
foo@bar:~$ uvicorn surfacescan.main:app --reload --port 8001
```

## Notes

* The requirement "Statistics should be from process startup" makes it hard to
  scale application by processes and especially nodes. Because in that case all
  the processes will have differect lifetime. In the same time the calculations
  for the `/attack` are CPU intensive so scaling by threads is not the case
  because of pythons's GIL. We think the best choise would be to update
  statistics requirements (for example `/stats` returns accumulated statistics
  from initial service startup and allows to query it by time ranges). In such
  case we could accumulate statistisc in `statsd`, send it to som ebackend and
  query that backend.
* We assume `attacks` relation is transitive, e.g. if A can attack B and B can
  attack C then A can attack C too.
* In some cases responses returned by "search" endpoints parametrized by query
  parameters can return 200 status code if nothing was found, but here we
  return the 404 status code to distinguish cases when a VM is not found and a
  VM is isolated and its surface attack is empty.
* We use [FastAPI](https://github.com/tiangolo/fastapi) for this project
  because of several reasons: `Django` seems an overhead for such a small
  project, `FastAPI` provides rich abbilities for parsing, validating and
  handling HTTP requests, it has ready test client, API documentation "out of
  the box", abbility to run the app in different modes (ASGI, WSGI),
  seems it has good performance, embedded tools for dependencies instantiation.
* As `FastAPI` intensively uses modern python typing we use it too.
* We use middleware to track each request, because in this case adding of a new
  request handler would not require any statistics related work (like
  registering or decorating a handler).
* As we keep statistics as a single instance and `FastAPI` can handle requests
  in different threads, statistics should be updated in a thread safe manner.
  We use atomic counters instead of locks to reduce performance impact, in such
  cases updating of both counters is not an atomic operation e.g. if we have
  2 simultanious requests for scanning and 1 for statistics, /stats can return
  requests count updated twice and requests duration updated once (but
  eventially it will be updated twice too). We assume such discrepancies are
  not significant and allowable.
* /stats response does not includes itself -- we cannot track it while it's not
  finished.


### Project structure

A service with 2 simple endpoints could be implemented in a single file but
one of major goals of this project is to show our approach for structuring a
service application.

#### surfacescan.main

Application initialization, entry point.

#### surfacescan.api

Routes, HTTP handlers definition. We tried to keep the approach when a HTTP
handler is only responsible for "HTTP related staff" and relies on "business
logic" modules to do the main work.

#### surfacescan.registry

As the statistics is bound to the process lifetime we keep it in memory as
a single instance. Obviously the environment data should be kept in memory to
avoid reading it on each request. So we created a separate module which is
resposible for "instantiating" dependencies required by request handlers.

#### surfacescan.tracking

Module responsible for statistics accumulation. The middleware just uses the
tracking function provided so we can easily change the implementation (for
example send data to `statsd`) and do not touch the middleware itself.

#### surfacescan.scanning

Module responsible for scanning the attack surface. Test cases described in
`tests/data_scanning.py` illustrate our understanding (or its lack) of the
problem.

#### gendata.py

Allows to generate big (or actually any sizes which can fit memory available)
data sets for performance testing purposes.

### What would be nice to have but is not implemented due to time restrictions

* `mypy` validation
* test `surfacescan.tracking.Tracker` increments its counters in a thread safe
  manner
* validate data loaded on startup, for example raise error when a duplicated
  vm_id is found (it would require also additional tests)
