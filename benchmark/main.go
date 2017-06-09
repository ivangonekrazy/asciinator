package main

import (
	"flag"
	"fmt"
	"net/http"
	"sync"
)

func main() {
	numRequestsFlag := flag.Int("n", 10, "Number of requests to make.")
	concurrentReqFlag := flag.Int("c", 1, "Number of concurrent requests.")
	filenameFlag := flag.String("image", "sample_gopher.jpg", "Path to file to use as input.")
	urlFlag := flag.String("url", "http://localhost:5000", "URL at which the Asciinator service is running.")
	flag.Parse()

	numConcurrentRequests := *concurrentReqFlag
	numRequests := *numRequestsFlag
	imagePath := *filenameFlag
	url := *urlFlag

	httpMethod := http.MethodPost

	var wg sync.WaitGroup

	client := http.DefaultClient
	bodyBytes, contentType := ImageUploadFromFile(imagePath)

	workerOpts := ProfileWorkerOpts{
		client:      client,
		httpMethod:  httpMethod,
		url:         url,
		bodyBytes:   bodyBytes,
		contentType: contentType,
	}

	fmt.Printf("Target URL: %v\n", url)
	fmt.Printf("POST body size: %v\n", len(bodyBytes))
	fmt.Printf("(%v requests; %v concurrently)\n\n", numRequests, numConcurrentRequests)

	keepGoing := make(chan bool)
	timelineChannel := make(chan Timeline)
	timelines := Timelines{}

	go func(tc chan Timeline) {
		for t := range tc {
			timelines = append(timelines, t)
		}
	}(timelineChannel)

	go func(keepGoing chan bool, numOfRequests int) {
		i := numOfRequests

		for {
			if i%numConcurrentRequests == 0 {
				fmt.Print(".")
			}
			if i > 0 {
				keepGoing <- true
				i = i - 1
			} else {
				keepGoing <- false
			}
		}

	}(keepGoing, numRequests)

	wg.Add(numConcurrentRequests)
	for i := 0; i < numConcurrentRequests; i++ {
		go ProfileWorker(workerOpts, timelineChannel, keepGoing, &wg)
	}

	wg.Wait()

	PrintAggregateTimelines(timelines)
}
