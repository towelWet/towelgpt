# towelgpt Golang bindings

The golang bindings have been tested on:
- MacOS
- Linux

### Usage

```
import (
	"github.com/nomic-ai/gpt4all/towelgpt-bindings/golang"
)

func main() {
	// Load the model
	model, err := towelgpt.New("model.bin", towelgpt.SetModelType(towelgpt.GPTJType))
	if err != nil {
		panic(err)
	}
	defer model.Free()

	model.SetTokenCallback(func(s string) bool {
		fmt.Print(s)
		return true
	})

	_, err = model.Predict("Here are 4 steps to create a website:", towelgpt.SetTemperature(0.1))
	if err != nil {
		panic(err)
	}
}
```

## Building

In order to use the bindings you will need to build `libtowelgpt.a`:

```
git clone https://github.com/nomic-ai/gpt4all
cd towelgpt/towelgpt-bindings/golang
make libtowelgpt.a
```

To use the bindings in your own software:

- Import `github.com/nomic-ai/gpt4all/towelgpt-bindings/golang`;
- Compile `libtowelgpt.a` (you can use `make libtowelgpt.a` in the bindings/go directory);
- Link your go binary by setting the environment variables `C_INCLUDE_PATH` and `LIBRARY_PATH` to point to the `binding.h` file directory and `libtowelgpt.a` file directory respectively.
- Note: you need to have *.so/*.dynlib/*.dll files of the implementation nearby the binary produced by the binding in order to make this to work

## Testing

To run tests, run `make test`:

```
git clone https://github.com/nomic-ai/gpt4all
cd towelgpt/towelgpt-bindings/golang
make test
```
