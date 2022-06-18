package providers

import (
	"fmt"
	"testing"
	"github.com/CiscoDevNet/ydk-go/ydk"
)

const testHome = "."

func TestNetconfServiceProvider(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	provider := NetconfServiceProvider{Address: "127.0.0.1", Username: "admin", Password: "admin", Port: 12022}
	provider.Connect()
	capabilities := provider.GetCapabilities()
	if len(capabilities) > 0 {
		fmt.Printf("===== Capabilities (%d):\n", len(capabilities))
		for i := 0; i < 2; i++ {
			fmt.Println(capabilities[i])
		}
	}
	provider.Disconnect()
}

func TestRestconfServiceProvider(t *testing.T) {
	if testing.Verbose() {
		ydk.EnableLogging(ydk.Debug)
	}
	provider := RestconfServiceProvider{Path: testHome, Address: "localhost", Username: "admin", Password: "admin", Port: 12306}
	provider.GetPrivate()
	capabilities := provider.GetCapabilities()
	if len(capabilities) > 0 {
		fmt.Printf("===== Capabilities (%d):\n", len(capabilities))
		for i := 0; i < 2; i++ {
			fmt.Println(capabilities[i])
		}
	}
	provider.Disconnect()
}
