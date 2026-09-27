(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
  )
  (:init
    (ontable d)
    (ontable f)
    (on a d)
    (on b c)
    (on c g)
    (on e f)
    (on g e)
    (clear a)
    (clear b)
    (handempty)
  )
  (:goal
    (and
      (on a c)
      (on b f)
      (on c g)
      (on d a)
      (on e b)
      (on f d)
    )
  )
)
