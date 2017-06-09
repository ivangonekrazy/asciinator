package main

import (
	"fmt"
	"sort"
	"time"
)

type Timelines []Timeline

func sortedSeries(ts Timelines, series string) []time.Duration {
	var durations []time.Duration

	for _, t := range ts {
		if t.IsError {
			continue
		}
		tm := t.AsMap()
		durations = append(durations, tm[series])
	}

	sort.Slice(durations, func(i, j int) bool { return durations[i] < durations[j] })
	return durations
}

func MaxDuration(ts Timelines, series string) time.Duration {
	durations := sortedSeries(ts, series)
	l := len(durations)
	return durations[l-1]
}

func MinDuration(ts Timelines, series string) time.Duration {
	durations := sortedSeries(ts, series)
	return durations[0]
}

func MedianDuration(ts Timelines, series string) time.Duration {
	durations := sortedSeries(ts, series)
	l := len(durations)

	if l%2 == 0 {
		return (durations[l/2-1] + durations[l/2+1]) / time.Duration(2)
	} else {
		return durations[l/2]
	}
}

func AverageDuration(ts Timelines, series string) time.Duration {
	var sum time.Duration

	durations := sortedSeries(ts, series)
	l := len(durations)

	for _, d := range durations {
		sum += d
	}

	return time.Duration(sum / time.Duration(l))
}

func PrintAggregateTimelines(ts Timelines) {
	seriesList := []string{
		"DNSLookup",
		"Connection",
		"Waiting",
		"ReceiveResponse",
		"Total",
	}

	fmt.Println("\nCount.Requests", len(ts))

	for _, series := range seriesList {
		fmt.Printf("%s:\n\tavg. %s; med. %s;\n\tmin. %s; max. %s\n",
			series,
			AverageDuration(ts, series),
			MedianDuration(ts, series),
			MinDuration(ts, series),
			MaxDuration(ts, series),
		)
	}
}
