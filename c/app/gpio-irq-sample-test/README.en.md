## 1.export GPIO

Export the selected GPIO to operate the GPIO,

```shell
root@root# echo xxx > /sys/class/gpio/export
```

## 2. compile 

```shell
root@root# gcc -o gpio-irq gpio-irq.c
```

## 3. format

```shell
root@root# ./gpio-irq <edge> [pull]
```

## 4. example

```shell
root@root# ./gpio-irq 433 rising down
.
GPIO 433 interrupt occurred!
..
GPIO 433 interrupt occurred!
.
GPIO 433 interrupt occurred!
.
GPIO 433 interrupt occurred!

```
