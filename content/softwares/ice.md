---
title: "Hello World Application with ZeroC Ice"
date: 2022-04-17T07:55:59+08:00
---

[Ice](https://zeroc.com/products/ice) is ZeroC's opensource RPC framework which supports interoperability in multiple languages. With Ice framework, it takes care of server management, discovery, and serialization, so developer can concentrate on business logic.

When creating Ice application, the first step is create a slice file. This file sets up the contract/interface between client and server. In our hello world application, we use the following very simple `Hello` interface.
```
module Demo {
        interface Hello {
                string SayHello(string username);
        };
}di
```

The next step is to use ice tool `slice2py` to compile the `.ice` slice file. This generates codes required for both client and server application to use. To demonstrate how this is done, I have created [a docker image](https://github.com/mcai4gl2/ice-play/blob/main/ice-helloworld/Dockerfile), as docker is a great way to test and play software in an isolated environment without affecting existing development setup. I have built the image and published to [dockerhub](https://hub.docker.com/repository/docker/mcai4gl2/ice-helloworld) as well.

`slice2py` generates `Hello_ice.py` and `Demo` module from `Hello.ice` input:
```bash
$ docker run -it --rm mcai4gl2/ice-helloworld:latest /bin/bash
root@98884be4a9cb:/app# cd /dependencies
root@98884be4a9cb:/dependencies# ls -ltr
total 20
-rw-r--r-- 1 root root   91 Apr 17 08:27 environment.yml
-rw-r--r-- 1 root root  105 Apr 17 08:27 environment-dev.yml
-rw-r--r-- 1 root root  104 Apr 17 08:27 Hello.ice
-rw-r--r-- 1 root root 2668 Apr 17 08:30 Hello_ice.py
drwxr-xr-x 2 root root 4096 Apr 17 08:30 Demo

```
We can interactively connect to the docker image and run `python -c 'import Demo'` to make sure everything is setup.

The [server.py](https://github.com/mcai4gl2/ice-play/blob/main/ice-helloworld/server.py) implements the `Hello` code generated to provide concreate implementation of our demo interface:
```python
import sys
import Ice
from Demo import Hello


class HelloServer(Hello):
    def SayHello(self, input, current=None):
        return f"Hello {input}"


if __name__ == "__main__":
    communicator = Ice.initialize(sys.argv)
    try:
        adapter = communicator.createObjectAdapterWithEndpoints("HelloAdapter", "default -p 10000")
        servant = HelloServer()
        adapter.add(servant, communicator.stringToIdentity("hello"))
        adapter.activate()
        communicator.waitForShutdown()
    finally:
        communicator.destroy()
```
Here, we run our application on port 10000.

The [client.py](https://github.com/mcai4gl2/ice-play/blob/main/ice-helloworld/client.py) code to consume the server service is as follows:
```python
import sys
import Ice
from Demo import HelloPrx


if __name__ == "__main__":
    communicator = Ice.initialize(sys.argv)
    try:
        base = communicator.stringToProxy("hello:default -p 10000")
        hello = HelloPrx.checkedCast(base)
        if not hello:
            raise RunTimeErrror("Invalid ice proxy")
        result = hello.SayHello("World!")
        print(f"Reply from server: {result}")
    finally:
        communicator.destroy()
```

To test the setup, we can [run the docker image interactively](https://github.com/mcai4gl2/ice-play/tree/main/ice-helloworld) with:
```bash
docker run -it --rm mcai4gl2/ice-helloworld:latest /bin/bash
root@6ecdd4ac9c63:/app# python server.py &
[1] 12
root@6ecdd4ac9c63:/app# python client.py
Reply from server: Hello World!
```

In this minimal example, we are leveraging Ice mainly for serialization. We are self-managing the service discovery and service placement. Leveraging Ice for IO can be especially useful in a multi languages project. As an example, in [this Dockerfile](https://github.com/mcai4gl2/ice-play/blob/main/ice-helloworld-cpp-client/Dockerfile), we have extended the helloworld application with C++ client but using the same python server implementation.

Instead of using `slice2py`, we use `slice2cpp` to generate required code. The `client.cpp` is as follows:
```cpp
#include <Ice/Ice.h>
#include <Hello.h>

using namespace std;
using namespace Demo;

int main(int argc, char* argv[])
{
        int status = 0;
        Ice::CommunicatorPtr ic;
        try
        {
                ic = Ice::initialize(argc, argv);
                Ice::ObjectPrx base = ic->stringToProxy("hello:default -p 10000");
                HelloPrx hello = HelloPrx::checkedCast(base);
                if (!hello)
                {
                        throw "Invalid proxy";
                }
                string result = "";
                result = hello->SayHello("test");
                cout << "client's result: " << result << endl;
        }
        catch (const Ice::Exception& ex)
        {
                cerr << ex << endl;
                status = 1;
        }
        catch (const char* msg)
        {
                cerr << msg << endl;
                status = 1;
        }

        if (ic)
        {
                ic->destroy();
        }

        return status;
}
```

To test this setup, we can [run the docker image interactively](https://github.com/mcai4gl2/ice-play/tree/main/ice-helloworld-cpp-client) with:
```bash
docker run -it -v --rm mcai4gl2/ice-helloworld-cpp-client:latest /bin/bash
root@10ec86155d14:/app# python server.py &
[1] 11
root@10ec86155d14:/app# ./client
client's result: Hello test
root@10ec86155d14:/app#
```

Next time, we will extend this demo application to use IceGrid to manage both.
