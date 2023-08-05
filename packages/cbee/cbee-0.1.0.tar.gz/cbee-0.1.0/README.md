# CBee - C/C++ build tools and package manager

CBee is a toolchain to build and package C/C++ applications and libraries.

## Installing cbee

```sh
python3 -m venv env
source env/bin/activate
```

```sh
pip install -U cbee
```

> ```sh
> pip install -e .
> ```

## Using cbee

### Running a basic C/C++ application

```c
// say-hello.c
#include <stdio.h>

int main() {
  printf("Hello!\n");
  return 0;
}
```

```sh
cbee run

./app
```

```sh
cbee build

./app
```

### Installing libraries

```sh
cbee install eigen
```

```sh
cbee update
```

### Managing dependencies

```txt
# libs.txt
- stdlib
- m
```
