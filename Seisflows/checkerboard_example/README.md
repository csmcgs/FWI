# A checkboard example

This folder contains a checkboard example which uses waveform misfit
and the whole trace instead of automated window selection. Both with
`pyatoa` and `default` preprocessor steps.


## 1. Link the specfem binary folder

Laptop/Workstation:

```console
$ ln -s /your/specfem2d/folder/bin .
```

Container:
```console
$ ln -s /home/scoped/specfem2d/bin .
```

## 2. Copy relevant parameters file

If you want to use `pyatoa` preprocess:

```console
$ cp parameters.yaml.pyaflowa_preprocess parameters.yaml
```

If you want to use `default` preprocess:

```console
$ cp parameters.yaml.default_preprocess parameters.yaml
```

## 3. Setup working directory

```console
$ ./setup_folder_paths.sh
```

## 4. Start the workflow

```console
$ seisflows submit
```


