# Numpy: Creating an Array

Code:
```
a = numpy.array([0,1,2])
print(a)
```

Output:
```
[0 1 2]
```

# Numpy: Creating a Matrix

Code:
```
m = numpy.array([[0,1,2],[2,3,4]])
print(m)
```

Output:
```
[[0 1 2]
 [2 3 4]]
```

# Boost: Optional

## Boiler Plate

Code:
```
#include<iostream>
#include<boost/optional.hpp>
#include<boost/optional/optional_io.hpp>

using namespace boost;

optional<double> calculate( double x )
{
  if( x > 10 )
    return 10*x;
}

```

## Usage

Code:
```
  auto y = calculate( 5 );
  auto z = calculate( 15 );

  std::cout << "y: " << y << std::endl;
  std::cout << "z: " << z << std::endl;
```

Output:
```
y: --
z:  150
```
