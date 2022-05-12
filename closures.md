# Closures

## Einleitung

Eine `Closure` wird benötigt, wenn man innerhalb einer Funktion eine weitere Funktion definieren will. Dazu folgendes Beispiel in Python:

```python
def makeAdder(x):
    def sub(y):
        return x + y
    return sub

plusFive = makeAdder(5)
```

```python
plusFive(10)
>>> 15

```

Die Funktion `makeAdder` dient dazu Funktionen zu erstellen, welche eine Zahl annehmen. Zu dieser Zahl wird dann der Wert addiert welcher angegeben wurde, als die Funktion durch `makeAdder` erstellt wurde.  
Im obigen Beispiel wurde durch Aufrufen von `makeAdder(5)` eine neue Funktion unter dem Namen `plusFive` erstellt, welche beim Aufruf `plusFive(10)` die Zahl 15 zurückgibt.

Damit dies funktioniert, muss `plusFive` "wissen", welche Zahl der übergeordneten Funktion `makeAdder` angegeben wurde, da sie ja diese zu der erhaltenen Zahl addieren muss.

Dazu wird beim Erstellen der Funktion `makeAdder` (und auch bei allen anderen Funktionen) im Hintergrund die Umgebung (Environment) mit abgespeichert. In dieser Umgebung ist die lokale Variable `x` und ihr Wert abgespeichert.

Dies bezeichnet man als Closure.

## Umsetzung
Um diese Funktionalität in unserer Programmiersprache zu erhalten, müssen wir nur an zwei Zeilen Änderungen vornehmen:  
1. Beim Abspeichern von eigenen Funktionen muss die momentane Umgebung auch abgespeichert werden.

    ```python
    case ['func', name, [params, body]]:
            env[name] = [params, body, env]             # !
            ...
    ```

2. Beim Abrufen von eigenen Funktionen muss die mitgegebene Umgebung eingelesen werden.

    ```python
    case [operator, *args]:
            func = env[operator]
            args = [evaluate(arg, env) for arg in args]

            match func:
                case [params, body, parentEnv]:         # !
                    newEnv = ChainMap({}, parentEnv)    # !
                    ...
    ```

Nun kann das obige Beispiel in unserer Sprache umgesetzt werden:

```scheme
> (func makeAdder (
      (x) 
      (block 
          (func inner (
              (y) 
              (+ x y)
          )) 
          inner
      )
  ))
```

```scheme
> (var plusFive (makeAdder 5))
```

```scheme
> (plusFive 10)
15
```