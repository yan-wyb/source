## 1.export GPIO

Export你选中的GPIO,

```shell
root@root# echo xxx > /sys/class/gpio/export
```

## 2. 编译

```shell
root@root# gcc -o gpio-irq gpio-irq.c
```

## 3.命令参数格式

```shell
root@root# ./gpio-irq <edge> [pull]
```

## 4.例子

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
