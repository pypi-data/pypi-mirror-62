# CBee - C/C++ build tools and package manager 🌻 🐝

CBee is a toolchain to build and package C/C++ applications and libraries.

## Installing cbee

> NOTE: this project requires Python 3.6+

```sh
python3 -m venv env
source env/bin/activate
```

```sh
pip install -U cbee
```

## Using cbee

### Running a basic C/C++ application

First, create a C or C++ file with a main function.

```c
// say-hello.c
#include <stdio.h>

int main() {
  printf("Hello!\n");
  return 0;
}
```

To run it, simply use the `cbee run` command.

```sh
cbee run say-hello.c
```

## Contributing

Contributions are welcome! For instructions on how to contribute,
please check the [Contribution](CONTRIBUTING.md) guide.
