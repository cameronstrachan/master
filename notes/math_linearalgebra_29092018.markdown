

## Vectors

**There are 3 perspectives**

* Physics perspective:
  - Length and direction, can move it anywhere.
* Computer science:
  - Ordered list of numbers. 2 dimentional vector contains 2 numbers.
* Math:
  - Vector can be anything with the notion of adding and multiplying the vectors.

When thinking of a vector as an arrow on a coordinate system, 2 numbers can define how to get from the origin to it's tip ($x$ and $y$). If there is a $z$ axis, then you have a triplet of numbers ($x$, $y$ and $z$).

**Adding vectors**

* Put tail of one vector on the tip of the other. This effectively represents the steps in space from the origin.
* Can simply add the two matched numbers.

**Multiplication by a number**

* Extends or contracts the vectors (and reverses the direction if negative), this is why its called scaling.
* A scalar is just a number.
* To multiply by a scaler, simply multiply both numbers.

## Span

* Think of a vector as scaling two "basis vectors", $\hat{\imath}$ ($y$ direction) and $\hat{\jmath}$ ($x$ direction).
* Any time you add two vectors and scale them, it is called a linear combination of those vectors.

```math
a\vec{v} + b \vec{w}
```

* If both basis vectors can be scaled freely, with a pair of vectors you can each every possible point in the plane.
* The "span" of $\vec{v}$ and $\vec{w}$ is the set of all of their _linear combinations_, or everywhere you can reach using only two fundamental operations: vector addition and scaler multiplication.
* The span of most 2D vectors is all of 2D space.
* But when they line up, its all vectors whose tip sits on a certain line.
* If a vector is alone, think of an error. If you are thinking of a collection of vectors, think about points in space.
* The span of a linear combination of 2 vectors in 3D space is essentially a flat plane that cuts through the space.
* A linear combination of 3 vectors can capture all 3D space ($a\vec{v} + b \vec{w} + c\vec{u}$).
* If vectors a redundant (line up), if you can remove one without changing the span, it is said that they are _linearly dependant_.

 > The basis of a vector space is a set of linearly independant vectors that span the full space.

### Linear transformation

_To be a linear transformation, lines must remain lines and the origin must remain at the origin_

* Linear transformations to a grid keeps the grid lines parrallel and evenly spaced.
* The nice property of linear transformation is that if you start out with a linear combination of $\hat{\imath}$ and $\hat{\jmath}$, the basis vectors, (a vector, ex. $-1\hat{\imath} + 2 \hat{\jmath}$) and perform some linear transformation, then where that vector landed is still just the linear combination of $\hat{\imath}$ and $\hat{\jmath}$.
* The coordinates of the newly transformed vector will therefore land on $x$ times the vector  where$\hat{\imath}$ lands plus $y$ times the vector where $\hat{\jmath}$ lands.

```math
 \begin{bmatrix} x \\ y \end{bmatrix} = x\begin{bmatrix} 1 \\ -2 \end{bmatrix} + y\begin{bmatrix} 3 \\ 0 \end{bmatrix}
=  \begin{bmatrix} 1x + 3y \\ -2x + 0y \end{bmatrix}
```

* This is just taken the component vectors and moving one vectors tail to the tip of the other (standard vector addition). Otherwise known as scaling the two component (basic) vectors and adding them.
* The formula above there can tell you where any single vector lands after the transformation by only knowing what happend to $\hat{\imath}$ and $\hat{\jmath}$.
* $\hat{\imath}$ and $\hat{\jmath}$ are often packaged as a 2 by 2 matrix, where the columns are these base vectors.

```math
\begin{bmatrix} a & b \\ c & d \end{bmatrix}
```

* If you have one of the above matrices describing a trasformation and a specific vector, and you want to find out where that transformation takes that vector, you can mulyiply the first value of the vector by the first column, and the second value by the second value, the add together what you get.

```math
x\begin{bmatrix} a \\ c \end{bmatrix} + y\begin{bmatrix} b \\ d \end{bmatrix} = \begin{bmatrix} xa + xb \\ xc + yd \end{bmatrix}
```

* Overall, this is simply a language to communicate linear transformations of space.

### Matrix multiplication

* Imagine that you wanted to apply a linear rotation and then shear to a vector space. The resulting composition matrix is called the product matrix.
* When multiplying two matrices, do not forgot that it is essentially.
* These matrices are read from right to left.
* When doing the matrix multiplication, remember that you are essentially multiplying and adding out $\hat{\imath}$ and $\hat{\jmath}$.
* Think of it as essentially taking $\hat{\imath}$ from the right matrix and multiplying by each column of the left and then adding them.
* In the end, you get the following.


```math
\begin{bmatrix} a & b \\ c & d \end{bmatrix}\begin{bmatrix} e & f \\ g & h \end{bmatrix} = \begin{bmatrix} ae + bg & af + bh\\ ce + dg & cf + dh\end{bmatrix}
```

* This is where you get this algoritmic way of multiplying rows and columns.
