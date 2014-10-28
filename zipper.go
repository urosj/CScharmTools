package main

import (
	"gopkg.in/juju/charm.v4"
	"log"
	"os"
)

func main() {
	switch os.Args[1] {
	case "zip":
		ch, err := charm.ReadCharmDir(os.Args[2])
		if err != nil {
			log.Fatal(err)
		}
		err = ch.ArchiveTo(os.Stdout)
		if err != nil {
			log.Fatal(err)
		}
	case "unzip":
		ch, err := charm.ReadCharmArchive(os.Args[2])
		if err != nil {
			log.Fatal(err)
		}
		err = ch.ExpandTo(os.Args[3])
		if err != nil {
			log.Fatal(err)
		}
	default:
		log.Fatal("usage?")
	}
}
