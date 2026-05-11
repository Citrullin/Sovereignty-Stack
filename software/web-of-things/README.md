# Web of Things Contributions

[RIOT-OS:](RIOT-OS) Module for RIOT-OS adding quite comprehensive Web of Things functionality. 
Including TD (Thing Description) code generation, exposing TD via CoAP.
[Arduino:](arduino) WebThings fork that enables W3C Web of Things TD 1.0 in the Arduino IDE.

These tools can be used to create sovereign IoT devices. Devices you own. 
Which you can use to interact with the physical world in a sovereign way.
Yet, they have not been battle tested in a real world scenarios yet.

The RIOT-OS implementation has been [tested in plugfest scenarios](https://w3c.github.io/wot-architecture/testing/report11.html#impl-riot-wot) though.
There is also a [very early tutorial from a W3C Web of Things testing event.](https://github.com/w3c/wot-testing/blob/a7df7b8ab250441c1a0d9667ea18e91883e35287/events/2020.09.Online/prototypes/RIOT-OS/README.md) 
Fascinating enough, the best example for RIOT can be found in the [wot code generation tests](https://github.com/namib-project/RIOT/tree/wot-gcoap2/tests/wot_coap_generation).
Upstreaming these features into mainline RIOT would certainly benefit the sovereignity stack.