ASCIInator Benchmarking Utility
=======================================
(c)2017 Ivan Tam.

A utility to benchmark the performance of an ASCIInator
service instance.


Dependencies and requirements
---------------------------------------

* Requires Go version 1.7 or above


Building
---------------------------------------

While in this directory, run the following:

`go build`

This should produce an executable named `benchmark`.


Usage
---------------------------------------

Command-line help is available via the `--help` arg:

```
asciinator/benchmark - [master●] » ./benchmark --help
Usage of ./benchmark:
  -c int
        Number of concurrent requests. (default 1)
  -image string
        Path to file to use as input. (default "sample_gopher.jpg")
  -n int
        Number of requests to make. (default 10)
  -url string
        URL at which the Asciinator service is running. (default "http://localhost:5000")
```

For example, to run 100 requests, with 5 requests concurrently:

```
./benchmark -c 5 -n 100
```

A sample image (`sample_gopher.jpg`) is included in this directly and is the
default `-image` flag value.

An instance of ASCIInator at the default URL can be started by running
the following in this files parent directory:

`make start`


Design
---------------------------------------

At a high level, this benchmark utility spawns a number of goroutine
workers (`ProfileWorker`) equal to the desired concurrency factor.

Another goroutine fans-out boolean messages to each worker over the `keepGoing`
channel. When workers receive a `true`, they make a request. This goroutine
will send out a number of of `true` messages equal to the number of desired
requests. When a `false` is received, the worker signals completion to
a `sync.WaitGroup`.

The `ProfileRequest()` function called by the `ProfileWorkers`
can be supplied options for target URLs, HTTP methods, and request bodies. This
can be reused to target services other than ASCIInator.

`ProfileRequest` sends request timing information (`Timeline`) over a channel
to be saved. Aggregate Timeline information is then calculated and output
by the `PrintAggregateTimelines()` function.
