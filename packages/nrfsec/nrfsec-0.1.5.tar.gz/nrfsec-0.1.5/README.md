
# nrfsec 

nrfsec is security research tool used for unlocking and reading memory on nrf51 series SoCs from Nordic Semiconductor. 

  - Read all target memory, bypassing the Memory Protection Unit (MPU) settings with integrated read gadget searching
  - Automated unlock feature: read all program and UICR memory, erase all memory, patch UICR image, relash target into unlocked state
  - boot delay command flag for interacting with target prior to performing memory read, allow for RAM dumps
  - All firmware images are saved for importing into your favorite disassembler 

### Installation

nrfsec is built on the [pyswd library](https://github.com/cortexm/pyswd/) and currently only works with the [ST-Link](https://www.adafruit.com/product/2548) debugging interface.

nrfsec requires python 3.7+ to run and can be installed with pip

```sh
pip3 install nrfsec
```



### Todos

 - Test on moar targets

License
----

GNU GPLv3 
