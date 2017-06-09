package main

import (
	"context"
	"crypto/tls"
	"io/ioutil"
	"net/http"
	"net/http/httptrace"
	"time"
)

type Timeline struct {
	StartTime             time.Time
	DNSLookup             time.Duration
	Connection            time.Duration
	TLSHandshake          time.Duration
	SendRequest           time.Duration
	Waiting               time.Duration
	FirstResponseByteTime time.Time
	ReceiveResponse       time.Duration
	EndTime               time.Time
	Total                 time.Duration

	ResponseSizeBytes int
	RequestSizeBytes  int

	ResponseStatusCode int

	IsError bool

	dnsLookupStart    time.Time
	dnsLookupEnd      time.Time
	connectionStart   time.Time
	connectionEnd     time.Time
	tlsHandshakeStart time.Time
	tlsHandshakeEnd   time.Time
	sendRequestStart  time.Time
	sendRequestEnd    time.Time
}

func (t *Timeline) AsMap() map[string]time.Duration {
	m := make(map[string]time.Duration)

	m["DNSLookup"] = t.DNSLookup
	m["Connection"] = t.Connection
	m["TLSHandshake"] = t.TLSHandshake
	m["SendRequest"] = t.SendRequest
	m["Waiting"] = t.Waiting
	m["ReceiveResponse"] = t.ReceiveResponse
	m["Total"] = t.Total

	return m
}

func (t *Timeline) Start(req *http.Request) {
	t.StartTime = time.Now()
	t.IsError = false
}

func (t *Timeline) Done(resp *http.Response) {
	t.EndTime = time.Now()
	t.ReceiveResponse = time.Since(t.FirstResponseByteTime)
	t.Total = time.Since(t.StartTime)
	t.ResponseStatusCode = resp.StatusCode

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)

	if err != nil {
		t.IsError = true
	} else {
		t.ResponseSizeBytes = len(body)
	}
}

func (t *Timeline) SetResponseStatusCode(statusCode int) {
	t.ResponseStatusCode = statusCode
}

func (t *Timeline) TraceContext(context context.Context) context.Context {
	return httptrace.WithClientTrace(context, &httptrace.ClientTrace{
		DNSStart: func(startInfo httptrace.DNSStartInfo) {
			t.dnsLookupStart = time.Now()
		},
		DNSDone: func(doneInfo httptrace.DNSDoneInfo) {
			if doneInfo.Err != nil {
				t.IsError = true
			}

			t.dnsLookupEnd = time.Now()
			t.DNSLookup = time.Since(t.dnsLookupStart)
		},
		ConnectStart: func(network, addr string) {
			t.connectionStart = time.Now()
		},
		ConnectDone: func(network, addr string, err error) {
			t.connectionEnd = time.Now()
			t.Connection = time.Since(t.connectionStart)
		},
		TLSHandshakeStart: func() {
			t.tlsHandshakeStart = time.Now()
		},
		TLSHandshakeDone: func(connState tls.ConnectionState, err error) {
			if err != nil {
				t.IsError = true
			}

			t.tlsHandshakeEnd = time.Now()
			if !t.tlsHandshakeStart.IsZero() {
				t.TLSHandshake = time.Since(t.tlsHandshakeStart)
			}
		},
		WroteRequest: func(requestInfo httptrace.WroteRequestInfo) {
			if requestInfo.Err != nil {
				t.IsError = true
			}

			t.sendRequestEnd = time.Now()

			if !t.tlsHandshakeEnd.IsZero() {
				t.SendRequest = time.Since(t.tlsHandshakeEnd)
			} else if !t.connectionEnd.IsZero() {
				t.SendRequest = time.Since(t.connectionEnd)
			}
		},
		GotFirstResponseByte: func() {
			t.FirstResponseByteTime = time.Now()
			t.Waiting = time.Since(t.sendRequestEnd)
		},
	})
}
