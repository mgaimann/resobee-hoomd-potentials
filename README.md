# ResoBee HOOMD Potentials

`resobee-hoomd-potentials` provides a plugin for [HOOMD-blue](https://hoomd-blue.readthedocs.io/) that implements several potentials used in the [ResoBee](https://github.com/mgaimann/ResoBee) project for reservoir computing with swarms.

## Building the component

To build this component:

1. Build and install **HOOMD-blue** from source.
2. Obtain the component's source.
    ```
    git clone https://github.com/mgaimann/resobee-hoomd-potentials
    ```
3. Configure.
    ```
    cmake -B build/resobee-hoomd-potentials -S resobee-hoomd-potentials
    ```
   Note: you might have to set your TBB path manually, for example by adding
   ```
   -DTBB_LIBRARY=/usr/lib/x86_64-linux-gnu/libtbb.so -DTBB_INCLUDE_DIR=/usr/include/oneapi/
   ```
4. Build the component.
    ```
    cmake --build build/resobee-hoomd-potentials
    ```
5. Install the component.
    ```
    cmake --install build/resobee-hoomd-potentials
    ```

Once installed, the template is available for import via:
```
import hoomd.resobee_hoomd_potentials
```
