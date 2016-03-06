# docker_dcflush
Ever been frustrated by the fact that you named some docker-container "db" a couple of hundred Docker-containers back? 
I wrote this utility to get rid of all those dead containers to free up available container names. 
Activity is logged to ./docker_dcflush.log

MIT-license, use at your own risk.
To complete the flush, restart the docker daemon after running docker_dcflush.py.

# python docker_dcflush.py

Docker dead container flush utility

The MIT License (MIT)
Copyright (c) 2016 Areusecure AB
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Do you accept the license stated above? (yes/no) yes

1. Started: 2016-03-05T22:21:16.045651629Z
Name: deb
Image: debian
Running: True
Exit code: 0 (Success)
Manually stopped: False
Exposed ports: 80/tcp
Uptime: [unknown] minutes and [unknown] seconds

Warning! Will not remove running containers, please stop them before removing their directories!


# docker stop deb
# python docker_dcflush.py

[omitted license-text etc]

1. Started: 2016-03-05T22:21:16.045651629Z
Name: deb
Image: debian
Running: False
Exit code: 0 (Success)
Manually stopped: True
Exposed ports: 80/tcp
Uptime: 686 minutes and 14 seconds

You are about to Remove "deb" (/var/lib/docker/containers/f9be6dff054f553e2d55cfd3cea1f136b8d26d602fb7d649e0442a13f379ed11), are you sure you want to remove db? (y)es/(n)o/(a)ll)y
Removing deb
Directory: /var/lib/docker/containers/f9be6dff054f553e2d55cfd3cea1f136b8d26d602fb7d649e0442a13f379ed11

1 container-directories were removed.
Docker dead-container flush has finished.
Author: Jonathan James <jj@areusecure.se>

# service docker restart

--- Now you are all set! (you may use the name "deb" again)
