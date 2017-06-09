package main

import (
	"bytes"
	"log"
	"net/http"
	"sync"
)

type ProfileWorkerOpts struct {
	client      *http.Client
	httpMethod  string
	url         string
	bodyBytes   []byte
	contentType string
}

func ProfileRequest(client *http.Client, req *http.Request) (Timeline, error) {
	timeline := new(Timeline)

	req = req.WithContext(timeline.TraceContext(req.Context()))

	timeline.Start(req)
	resp, err := client.Do(req)
	if err != nil {
		log.Println(err)
		return *timeline, err
	}
	timeline.Done(resp)

	return *timeline, nil
}

func ProfileWorker(p ProfileWorkerOpts, tc chan Timeline, continueRequests chan bool, wg *sync.WaitGroup) {

	for keepGoing := range continueRequests {
		if keepGoing {
			req, _ := http.NewRequest(p.httpMethod, p.url, bytes.NewBuffer(p.bodyBytes))
			req.Header.Set("Content-Type", p.contentType)

			timeline, err := ProfileRequest(p.client, req)
			if err != nil {
				log.Println(err)
			}

			tc <- timeline
		} else {
			break
		}
	}

	wg.Done()
}
