package main

import (
	"fmt"
	"os"
	"time"
)

const MyNodePath = "./data/clientNode"

func main() {
	args := os.Args[1:]

	if len(args) < 2 {
		fmt.Println("Not enough arguments, please specify peerID and peerIP")
		os.Exit(1)
	}

	targetPeer := args[0]
	targetIP := args[1]

	fmt.Println("Test reachability on target peer", targetPeer+"@"+targetIP)

	if !Exists(MyNodePath) {
		err := NewNodeRepo(MyNodePath, nil)
		if err != nil {
			panic(err)
		}
	}

	node, err := NewNode(MyNodePath)
	if err != nil {
		panic(err)
	}

	start := time.Now()
	for {
		_, err := Request(node, targetPeer, "/health")
		if err == nil {
			break
		}
		fmt.Println(":", err)
		time.Sleep(500 * time.Microsecond)
	}

	elapsed := time.Since(start)
	fmt.Println(elapsed)
}
