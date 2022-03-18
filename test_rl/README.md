### Setting up tensorflow-gpu

-   Follow [this link](https://www.tensorflow.org/install/gpu) to install tensorflow with gpu support (note you need an nvidia gpu).

-   You'll also need to sign up for the NVIDIA developer program to get access to cuDNN - will also need a legacy version.

-   I haven't followed the linux version, but you'll likely need to adapt it to be 11.2 instead of the 11.0 install instructions they list (maybe older versions will work though?).

-   You can verify if the install was correct by opening a python interpreter and running the following commands
    ```
    import tensorflow as tf
    tf.test.gpu_device_name()
    ```
    If you see a gpu device ie. '/device:GPU:0', you've successfully installed tensorflow-gpu

**NOTE:** you must install the exact versions specified for the version (don't make the same mistake as me and install the wrong version).

### RL findings

-   I didn't manage to get the openspiel_test.py working (missing dependencies with reverb) - could try doing it on linux or just without reverb to see if tf.sessions actually gpu accelerates.

-   cartpole.py has an attempt at RL, seems to be pretty bad and not actually gpu accelerated.

-   main.ipynb contains some test code, I tried to copy an example but it was only for tensorflow 1.X and does not work.

**Ultimately** probably something like what the openspiel_test has with the tf_agents will likely be the most successful option but requires testing (need to exclude reverb because it doesn't work with Windows, but it seems like it's just a filesystem database thing to store games). I think we can make a custom wrapper for the gym models I (Robert) can possibly get to it later if need be.
