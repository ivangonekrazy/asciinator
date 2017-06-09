package main

import (
	"bytes"
	"io"
	"log"
	"mime/multipart"
	"os"
)

func ImageUploadFromFile(filename string) ([]byte, string) {
	imageFile, err := os.Open(filename)
	defer imageFile.Close()
	if err != nil {
		os.Exit(1)
	}

	requestBody := new(bytes.Buffer)
	requestBodyWriter := multipart.NewWriter(requestBody)
	defer requestBodyWriter.Close()
	if err != nil {
		log.Fatal(err)
	}

	formFile, _ := requestBodyWriter.CreateFormFile("file", filename)
	io.Copy(formFile, imageFile)
	requestBodyWriter.WriteField("style", "black_and_white")
	requestBodyWriter.Close()

	bodyBytes := requestBody.Bytes()
	contentType := requestBodyWriter.FormDataContentType()

	return bodyBytes, contentType
}
