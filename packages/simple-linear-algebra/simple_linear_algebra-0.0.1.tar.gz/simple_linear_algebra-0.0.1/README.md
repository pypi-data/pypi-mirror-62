# linear_algebra

## Motivation

- Review linear algebraby implementing concenpts in Python code
- Learn OOP in Python

## Installation

```bash
pip install
```

## Features

---

### Completed

- Vector
  
  ```python
  # Initialize vector 
  v_1 = Vector(1, 2, 3)
  v_2 = Vector(4, 5, 6)
  ```

- Add (+)

- ```python
  [in]: Vector(1, 2, 3) + Vector(4, 5, 6)
  [out]: Vecotr(5, 7, 9)
  ```

- Subtract (-)

- ```python
  [in]: Vector(3, 2, 1) - Vector(1, 1, 1)
  [out]: Vector(2, 1, 0) 
  ```

- Multiply (*)

- ```python
  # scaler
  [in]: 2 * Vector(1, 2, 3)
  [out]: Vector(2, 4, 6)
  
  # inner product
  [in]: Vector(1, 2, 3) * Vector(1, 1, 1)
  [out]: 6
  ```

- .norm

- ```python3
  # .norm attribute of the vector is the length or magnitude of the 
  # vector
  [in]: Vector(1, 2, 3).norm
  [out]: 3.7419573
  ```

### To be Implemented

- Matrix
